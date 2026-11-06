"""AI agent layer: one structured-output Claude call per stage.

Agent backends, chosen with the RFPFLOW_AGENT environment variable:
  api  (default) - Claude API call with structured output.
  ollama         - free, local model through Ollama (RFPFLOW_OLLAMA_MODEL, default qwen2.5:7b;
                   OLLAMA_HOST, default http://localhost:11434). Output is constrained to the schema.
  file           - no API key: the stage's prompt is written to inbox/run-N/, and the output
                   is read from a JSON file written there by Claude in a Claude Code chat.
  stub           - schema-valid placeholder, for testing the orchestration (also RFPFLOW_STUB=1).
"""

from __future__ import annotations

import copy
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field

from pydantic import BaseModel, ValidationError

from .config import (FALLBACK_BETA, INBOX_DIR, MAX_TOKENS, MODEL, PRICE_CACHE_READ, PRICE_CACHE_WRITE,
                     PRICE_INPUT, PRICE_OUTPUT, STAGES)
from .loader import SOURCES, SourceDoc, sources_block
from .prompts import SHARED_RULES
from .schemas import SCHEMAS, StageEnvelope


@dataclass
class AgentResult:
    output: dict | None
    assistant_content: list[dict] = field(default_factory=list)  # appended to the conversation
    usage: dict = field(default_factory=dict)
    error: str | None = None


def system_blocks(docs: dict[str, SourceDoc]) -> list[dict]:
    text = SHARED_RULES + sources_block(docs, list(SOURCES))
    return [{"type": "text", "text": text, "cache_control": {"type": "ephemeral"}}]


def cost_usd(usage: dict) -> float:
    return round(
        usage.get("input_tokens", 0) * PRICE_INPUT / 1e6
        + usage.get("output_tokens", 0) * PRICE_OUTPUT / 1e6
        + usage.get("cache_creation_input_tokens", 0) * PRICE_CACHE_WRITE / 1e6
        + usage.get("cache_read_input_tokens", 0) * PRICE_CACHE_READ / 1e6,
        4,
    )


def agent_mode() -> str:
    if os.environ.get("RFPFLOW_STUB") == "1":
        return "stub"
    return os.environ.get("RFPFLOW_AGENT", "api").lower()


def run_agent(stage: int, docs: dict[str, SourceDoc], messages: list[dict],
              run_id: int = 0, attempt: int = 1, mode: str | None = None,
              api_key: str | None = None, model: str | None = None) -> AgentResult:
    """`mode` overrides RFPFLOW_AGENT; `api_key` (from the UI) is used for this call only and never stored.
    `model` picks the Ollama model in ollama mode."""
    mode = mode or agent_mode()
    if mode == "stub":
        return _stub(stage)
    if mode == "ollama":
        return _ollama(stage, docs, messages, model or OLLAMA_MODEL)
    if mode == "file":
        return _from_file(stage, messages, run_id, attempt)

    import anthropic  # imported here: the package is slow to load and only API calls need it

    schema = SCHEMAS[stage]
    # Key from the caller, else ANTHROPIC_API_KEY or the `ant auth login` profile.
    client = anthropic.Anthropic(api_key=api_key) if api_key else anthropic.Anthropic()

    def call(output_format):
        with client.beta.messages.stream(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system_blocks(docs),
            messages=messages,
            thinking={"type": "adaptive"},
            output_config={"effort": STAGES[stage].effort},
            output_format=output_format,
            cache_control={"type": "ephemeral"},  # also cache the growing conversation for reruns
            betas=[FALLBACK_BETA],
            fallbacks="default",
        ) as stream:
            return stream.get_final_message()

    try:
        try:
            msg = call(StageEnvelope)  # the same format every stage, so the prompt cache can be reused
        except anthropic.BadRequestError as e:
            if "schema" not in str(e.message).lower():
                raise
            msg = call(schema)  # the API rejected the combined schema: still run, without cache reuse
    except anthropic.APIConnectionError as e:
        return AgentResult(None, error=f"Connection error: {e}")
    except anthropic.RateLimitError as e:
        return AgentResult(None, error=f"Rate limited (retry later): {e}")
    except anthropic.APIStatusError as e:
        return AgentResult(None, error=f"API error {e.status_code}: {e.message}")
    except ValidationError as e:
        return AgentResult(None, error=f"Output failed schema validation: {e}")
    except TypeError as e:  # raised by the SDK when no credential source resolves
        if "authentication" in str(e).lower():
            return AgentResult(None, error="No Claude API credentials: set ANTHROPIC_API_KEY or run `ant auth login`.")
        raise

    usage = msg.usage.model_dump(include={"input_tokens", "output_tokens", "cache_creation_input_tokens",
                                          "cache_read_input_tokens"})
    usage = {k: v or 0 for k, v in usage.items()}
    usage["served_by"] = msg.model
    content = [b.model_dump(mode="json", exclude_none=True) for b in msg.content]

    if msg.stop_reason == "refusal":
        details = getattr(msg, "stop_details", None)
        why = f"{details.category}: {details.explanation}" if details else "no details"
        return AgentResult(None, content, usage, error=f"Model declined this request ({why}).")
    if msg.stop_reason == "max_tokens":
        return AgentResult(None, content, usage, error="Output hit max_tokens before finishing.")

    parsed: BaseModel | None = msg.parsed_output
    if parsed is None:
        return AgentResult(None, content, usage, error="No structured output returned.")
    if isinstance(parsed, StageEnvelope):
        parsed = parsed.stage_output
    if not isinstance(parsed, schema):
        return AgentResult(None, content, usage, error=f"Output failed schema validation: expected "
                                                       f"{schema.__name__}, got {type(parsed).__name__}.")
    return AgentResult(parsed.model_dump(mode="json"), content, usage)


OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
OLLAMA_MODEL = os.environ.get("RFPFLOW_OLLAMA_MODEL", "qwen2.5:7b")
OLLAMA_CTX = 32768  # the prompt (rules + all sources + approved outputs) needs far more than Ollama's default


def ollama_models(host: str = OLLAMA_HOST) -> list[str] | None:
    """Models pulled into the local Ollama, or None if Ollama is not reachable."""
    try:
        with urllib.request.urlopen(f"{host}/api/tags", timeout=3) as r:
            return [m["name"] for m in json.load(r).get("models", [])]
    except (urllib.error.URLError, OSError, ValueError):
        return None


def _inline_refs(schema: dict) -> dict:
    """Inline Pydantic's $defs/$ref so the schema works as an Ollama `format` constraint."""
    defs = schema.get("$defs", {})

    def walk(node):
        if isinstance(node, dict):
            if "$ref" in node:
                return walk(copy.deepcopy(defs[node["$ref"].split("/")[-1]]))
            return {k: walk(v) for k, v in node.items() if k != "$defs"}
        if isinstance(node, list):
            return [walk(v) for v in node]
        return node

    return walk(schema)


def _text_of(content) -> str:
    if isinstance(content, str):
        return content
    return "\n\n".join(b.get("text", "") for b in content if b.get("type") == "text")


def _ollama(stage: int, docs: dict[str, SourceDoc], messages: list[dict], model: str) -> AgentResult:
    """Local model through Ollama's chat API, with output constrained to the stage schema."""
    schema = SCHEMAS[stage]
    system = (SHARED_RULES + sources_block(docs, list(SOURCES))
              + "\n\nReply with a single JSON object that matches the required schema, and nothing else.")
    body = {
        "model": model,
        "messages": [{"role": "system", "content": system}]
                    + [{"role": m["role"], "content": _text_of(m["content"])} for m in messages],
        "format": _inline_refs(schema.model_json_schema()),
        "stream": False,
        "options": {"num_ctx": OLLAMA_CTX, "temperature": 0},
    }
    usage = {"served_by": f"ollama:{model}"}
    req = urllib.request.Request(f"{OLLAMA_HOST}/api/chat", data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=3600) as r:  # local models can take many minutes
            data = json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "ignore")
        if e.code == 404 or "not found" in detail:
            return AgentResult(None, usage=usage, error=f"Ollama model '{model}' is not installed. Run: ollama pull {model}")
        return AgentResult(None, usage=usage, error=f"Ollama error {e.code}: {detail[:300]}")
    except (urllib.error.URLError, OSError) as e:
        return AgentResult(None, usage=usage, error=f"Ollama is not running at {OLLAMA_HOST} ({e}). "
                                                     "Install it from ollama.com and start the Ollama app.")
    usage.update(local_input_tokens=data.get("prompt_eval_count", 0),
                 local_output_tokens=data.get("eval_count", 0),
                 seconds=round(data.get("total_duration", 0) / 1e9, 1))
    content = data.get("message", {}).get("content", "")
    if data.get("done_reason") == "length":
        return AgentResult(None, usage=usage, error="Output hit max_tokens before finishing (Ollama stopped at its length limit).")
    try:
        parsed = schema.model_validate_json(content)
    except ValidationError as e:
        return AgentResult(None, usage=usage, error=f"Output failed schema validation: {e}")
    return AgentResult(parsed.model_dump(mode="json"), [{"type": "text", "text": content}], usage)


def _from_file(stage: int, messages: list[dict], run_id: int, attempt: int) -> AgentResult:
    """File backend: write the prompt, read the agent's JSON output (same schema, same checks)."""
    folder = INBOX_DIR / f"run-{run_id}"
    folder.mkdir(parents=True, exist_ok=True)
    out_path = folder / f"stage-{stage}-attempt-{attempt}.json"
    prompt_path = folder / f"stage-{stage}-attempt-{attempt}.prompt.md"
    if not prompt_path.exists():
        turns = []
        for m in messages:
            content = m["content"] if isinstance(m["content"], list) else [{"type": "text", "text": m["content"]}]
            text = "\n\n".join(b.get("text", "") for b in content if b.get("type") == "text")
            turns.append(f"## {m['role']}\n\n{text}")
        prompt_path.write_text(
            f"# Stage {stage} prompt (attempt {attempt})\n\n"
            f"System prompt: rfpflow/prompts.py SHARED_RULES + all data sources.\n"
            f"Output schema: {SCHEMAS[stage].__name__} in rfpflow/schemas.py.\n"
            f"Write the output to: {out_path.name}\n\n" + "\n\n".join(turns) + "\n",
            encoding="utf-8")
    usage = {"input_tokens": 0, "output_tokens": 0, "served_by": "claude-code (file backend)"}
    if not out_path.exists():
        return AgentResult(None, usage=usage,
                           error=f"Waiting for agent output: {out_path.relative_to(INBOX_DIR.parent)}")
    raw = out_path.read_text(encoding="utf-8")
    try:
        parsed = SCHEMAS[stage].model_validate_json(raw)
    except ValidationError as e:
        return AgentResult(None, usage=usage, error=f"Output failed schema validation: {e}")
    return AgentResult(parsed.model_dump(mode="json"), [{"type": "text", "text": raw}], usage)


def _stub(stage: int) -> AgentResult:
    schema = SCHEMAS[stage].model_json_schema()
    defs = schema.get("$defs", {})

    def fake(node):
        if "$ref" in node:
            return fake(defs[node["$ref"].split("/")[-1]])
        if "enum" in node:
            return node["enum"][0]
        if "const" in node:
            return node["const"]
        t = node.get("type")
        if t == "object":
            return {k: fake(v) for k, v in node.get("properties", {}).items()}
        return {"array": [], "string": f"stub stage {stage}", "integer": 0, "number": 0.0,
                "boolean": False}.get(t)

    out = SCHEMAS[stage].model_validate(fake(schema)).model_dump(mode="json")
    return AgentResult(out, [{"type": "text", "text": "{}"}], {"input_tokens": 0, "output_tokens": 0,
                                                               "served_by": "stub"})
