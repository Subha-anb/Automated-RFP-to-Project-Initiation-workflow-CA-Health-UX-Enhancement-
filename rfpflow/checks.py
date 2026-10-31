"""Deterministic checks of agent outputs against facts already in the data sources.

Shown to the approver at each checkpoint and reused by the evaluation script.
"""

from __future__ import annotations

from dataclasses import dataclass

from .loader import SourceDoc

HOURS_PER_MONTH = 160


@dataclass
class Check:
    name: str
    passed: bool
    detail: str


def _pct(value: str) -> float | None:
    value = value.strip().rstrip("%")
    try:
        return float(value) / 100
    except ValueError:
        return None


def check_stage(stage: int, out: dict, docs: dict[str, SourceDoc]) -> list[Check]:
    fn = {1: _stage1, 2: _stage2, 3: _stage3, 4: _stage4, 5: _stage5, 6: _stage6}.get(stage)
    checks = fn(out, docs) if fn else []
    checks.append(_sourced(out))
    return checks


def _walk_items(obj):
    """Yield every dict that has source_refs."""
    if isinstance(obj, dict):
        if "source_refs" in obj:
            yield obj
        for v in obj.values():
            yield from _walk_items(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk_items(v)


def _sourced(out: dict) -> Check:
    items = list(_walk_items(out))
    bad = [i for i in items if not i.get("source_refs") and not i.get("assumption")]
    return Check("Every item cites a source or is marked an assumption", not bad,
                 f"{len(items) - len(bad)}/{len(items)} items sourced or flagged")


def _stage1(out, docs):
    header = {r["Field"]: r["Value"] for r in docs["rfp"].table_with_header("Field")}
    return [Check("RFP number matches the RFP", out.get("rfp_number") == header["RFP number"],
                  f"{out.get('rfp_number')!r} vs {header['RFP number']!r}")]


def _stage2(out, docs):
    expected = {r["ID"] for r in docs["rfp"].table_with_header("ID") if r["ID"].startswith("R-")}
    got = {r["req_id"] for r in out.get("trace_matrix", [])}
    rules = {r["Rule ID"] for r in docs["compliance"].table_with_header("Rule ID")}
    unknown = {c for r in out.get("trace_matrix", []) for c in r["compliance_rules"]} - rules
    r05 = next((r for r in out.get("trace_matrix", []) if r["req_id"] == "R-05"), None)
    r12_flagged = any(u["req_id"] == "R-12" for u in out.get("unclear_clauses", []))
    return [
        Check("Every RFP requirement is in the trace matrix", expected <= got,
              f"missing: {sorted(expected - got) or 'none'}"),
        Check("Only real compliance rule IDs are cited", not unknown, f"unknown: {sorted(unknown) or 'none'}"),
        Check("R-05 (language access) maps to rule C-11", bool(r05 and "C-11" in r05["compliance_rules"]),
              f"R-05 rules: {r05['compliance_rules'] if r05 else 'row missing'}"),
        Check("Vague requirement R-12 is flagged as unclear", r12_flagged, "flagged" if r12_flagged else "not flagged"),
    ]


def _stage3(out, docs):
    assets = docs["kansas_assets"].table_with_header("ID")
    known = {a["ID"] for a in assets}
    needs_release = {a["ID"] for a in assets if "needs kansas release" in a["IP status"].lower()}
    used = {aid for m in out.get("mappings", []) for aid in m["asset_ids"]}
    listed = set(out.get("ip_clearance_request", {}).get("state_owned_assets", []))
    r05 = next((m for m in out.get("mappings", []) if m["req_id"] == "R-05"), None)
    return [
        Check("Only real Kansas asset IDs are cited", used <= known, f"unknown: {sorted(used - known) or 'none'}"),
        Check(f"All {len(needs_release)} state-owned assets needing release are in the IP request",
              needs_release <= listed, f"missing: {sorted(needs_release - listed) or 'none'}"),
        Check("R-05 (language access) maps to KS-LG-01", bool(r05 and "KS-LG-01" in r05["asset_ids"]),
              f"R-05 assets: {r05['asset_ids'] if r05 else 'row missing'}"),
    ]


def _stage4(out, docs):
    staff = {r["Staff ID"]: r for r in docs["skills_rates"].table_with_header("Staff ID")}
    rates = {r["Role"].lower(): r["Hourly rate (USD)"] for r in docs["skills_rates"].table_with_header("Role")}
    over, months_bad, arith_bad, rate_bad = [], [], [], []
    total = 0.0
    for line in out.get("staffing", []):
        fte = line["fte_by_month"]
        if len(fte) != 6:
            months_bad.append(line["staff_id"])
        avail = _pct(staff[line["staff_id"]]["Availability"]) if line["staff_id"] in staff else None
        if avail is not None and max(fte, default=0) > avail + 1e-9:
            over.append(f"{line['staff_id']} max {max(fte)} > {avail}")
        expected = round(sum(fte) * HOURS_PER_MONTH * line["hourly_rate"], 2)
        if abs(expected - line["labor_cost"]) > 0.5:
            arith_bad.append(f"{line['staff_id']}: {line['labor_cost']} vs {expected}")
        card = next((v for k, v in rates.items() if k.startswith(line["role"].lower()[:12])), None)
        if card and float(card.replace("$", "").replace(",", "")) != line["hourly_rate"]:
            rate_bad.append(f"{line['role']}: {line['hourly_rate']} vs {card}")
        total += expected
    return [
        Check("No staff member exceeds their availability", not over, "; ".join(over) or "all within availability"),
        Check("Every staff line has 6 months", not months_bad, f"bad: {months_bad or 'none'}"),
        Check("Hourly rates match the rate card", not rate_bad, "; ".join(rate_bad) or "all match"),
        Check("Each line's labor cost = FTE-months x 160 x rate", not arith_bad, "; ".join(arith_bad) or "all correct"),
        Check("Total labor cost = sum of staff lines", abs(total - out.get("total_labor_cost", -1)) <= 1,
              f"reported {out.get('total_labor_cost')} vs computed {round(total, 2)}"),
    ]


def _stage5(out, docs):
    clauses = {r["Clause"] for r in docs["contracts"].table_with_header("Clause")}
    got = {c["clause"] for c in out.get("clause_positions", [])}
    return [Check("Every playbook clause has a position", clauses <= got,
                  f"missing: {sorted(clauses - got) or 'none'}")]


def _stage6(out, docs):
    cs = out.get("clock_start", {})
    return [Check("Clock start is backed by a cited source", bool(cs.get("confirmed") is False or cs.get("source_refs")),
                  f"confirmed={cs.get('confirmed')}, refs={cs.get('source_refs')}")]
