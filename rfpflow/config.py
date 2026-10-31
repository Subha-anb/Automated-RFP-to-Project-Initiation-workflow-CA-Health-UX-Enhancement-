"""Per-stage configuration: agent effort, checkpoint, approvers and SLA. Tune effort here."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = ROOT / "state"
OUTPUT_DIR = ROOT / "output"
INBOX_DIR = ROOT / "inbox"  # file agent backend: prompts out, agent JSON in
DB_PATH = STATE_DIR / "runs.db"
AUDIT_LOG = STATE_DIR / "audit.jsonl"

MODEL = "claude-opus-5-5"
FALLBACK_BETA = "server-side-fallback-2026-07-01"
MAX_TOKENS = 64000  # streamed, so a large ceiling is safe

# Claude Opus 5.5 list prices, USD per million tokens (cache write = 1.25x input, 5-minute TTL).
PRICE_INPUT = 4.00
PRICE_OUTPUT = 20.00
PRICE_CACHE_WRITE = 5.00
PRICE_CACHE_READ = 0.20


@dataclass(frozen=True)
class Stage:
    number: int
    agent: str
    effort: str  # low | medium | high | xhigh | max
    gate: str
    approvers: tuple[str, ...]  # every listed approver must approve
    sla_hours: int


STAGES: dict[int, Stage] = {
    1: Stage(1, "RFP intake", "medium", "H1 Go/no-go", ("Bid committee", "Finance", "Legal"), 48),
    2: Stage(2, "Requirements and compliance", "high", "H2 Requirements sign-off", ("Solution architect", "Compliance officer"), 48),
    3: Stage(3, "Kansas reuse", "high", "H3 Reuse baseline", ("UX lead", "Legal"), 48),
    4: Stage(4, "Plan and cost", "high", "H4 Plan and price", ("PMO lead", "Finance"), 48),
    5: Stage(5, "Contract", "high", "H5 Negotiation positions", ("Legal",), 48),
    6: Stage(6, "Sign-off tracker", "low", "H6 Contract sign-off", ("Executive sponsor", "State"), 72),
}
