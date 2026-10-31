"""Output schemas for the six agents (structured outputs via Pydantic).

Every finding carries `source_refs` (IDs from the data sources). Anything the documents do
not support is marked `assumption=True` with a reason, or raised in `open_questions`.
Every output lists `rad_impacts` against the risk/assumption/dependency tracker.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class Sourced(BaseModel):
    source_refs: list[str] = Field(description="IDs this item is based on, e.g. ['R-05', 'KS-LG-01', 'C-11'].")
    assumption: bool = Field(description="True if the documents do not directly support this item.")
    assumption_reason: str = Field(description="Why this is an assumption; empty string when assumption is false.")


class RadImpact(BaseModel):
    item_id: str = Field(description="Tracker ID (R-xx risk, A-xx assumption, D-xx dependency) or 'NEW'.")
    action: Literal["raises", "changes", "closes", "new"]
    note: str
    source_refs: list[str]


class OpenQuestion(BaseModel):
    question: str
    why_it_matters: str
    source_refs: list[str]


class StageCommon(BaseModel):
    open_questions: list[OpenQuestion]
    rad_impacts: list[RadImpact]


# ---------- Stage 1: RFP intake ----------

class KeyDate(Sourced):
    milestone: str
    date: str


class Factor(Sourced):
    factor: str
    assessment: str
    effect: Literal["positive", "negative", "neutral"]


class IntakeOutput(StageCommon):
    rfp_number: str
    title: str
    issuer: str
    contract_type: str
    term: str
    budget_ceiling: str
    key_dates: list[KeyDate]
    fit_score: int = Field(description="0-100: how well the RFP fits our Kansas experience and capacity.")
    fit_factors: list[Factor]
    risk_score: int = Field(description="0-100: higher means riskier to bid.")
    risk_factors: list[Factor]
    recommendation: Literal["go", "go-with-conditions", "no-go"]
    conditions: list[str]
    go_no_go_brief: str = Field(description="One-page brief in Markdown for the bid committee.")


# ---------- Stage 2: Requirements and compliance ----------

class TraceRow(Sourced):
    req_id: str
    requirement: str
    category: str
    priority: Literal["Must", "Should", "Could"]
    compliance_rules: list[str] = Field(description="Applicable rule IDs, e.g. ['C-01', 'C-03'].")
    notes: str


class UnclearClause(Sourced):
    req_id: str
    issue: str
    drafted_question: str = Field(description="Written question to submit in the RFP Q&A window.")


class RuleCoverage(Sourced):
    rule_id: str
    applies_to: list[str] = Field(description="Requirement IDs the rule applies to.")
    checkpoint: str


class RequirementsOutput(StageCommon):
    trace_matrix: list[TraceRow]
    unclear_clauses: list[UnclearClause]
    rule_coverage: list[RuleCoverage]


# ---------- Stage 3: Kansas reuse ----------

class ReuseRow(Sourced):
    req_id: str
    asset_ids: list[str] = Field(description="Kansas asset IDs (KS-*); empty when the verdict is 'new'.")
    verdict: Literal["reuse", "enhance", "new"]
    reason: str
    ip_status: str


class IpClearanceRequest(BaseModel):
    state_owned_assets: list[str] = Field(description="Kansas asset IDs that need a written release.")
    request_text: str
    source_refs: list[str]


class ReuseOutput(StageCommon):
    mappings: list[ReuseRow]
    ip_clearance_request: IpClearanceRequest


# ---------- Stage 4: Plan and cost ----------

class StaffLine(Sourced):
    role: str
    staff_id: str = Field(description="EMP-*/CTR-* ID, or 'TO-SOURCE' for an unfilled role.")
    availability_fte: float = Field(description="Maximum FTE this person is available, from the inventory.")
    fte_by_month: list[float] = Field(description="Exactly 6 values, months 1-6 (Feb-Jul 2027).")
    hourly_rate: float
    labor_cost: float = Field(description="sum(fte_by_month) * 160 * hourly_rate")


class Milestone(Sourced):
    deliverable_id: str
    name: str
    month: int
    payment_pct: float
    labor_cost: float = Field(description="Labor cost of the month this deliverable is due.")


class StaffingGap(Sourced):
    gap: str
    mitigation: str


class BenchmarkCheck(Sourced):
    work_item: str
    planned_hours: float
    benchmark_range: str
    within_range: bool


class PlanOutput(StageCommon):
    staffing: list[StaffLine]
    milestones: list[Milestone]
    total_labor_cost: float
    staffing_gaps: list[StaffingGap]
    benchmark_checks: list[BenchmarkCheck]


# ---------- Stage 5: Contract ----------

class ClausePosition(Sourced):
    clause: str
    state_position: str
    proposed_position: str
    playbook_fallback: str
    status: Literal["within_fallback", "escalate"]
    approver: str
    rationale: str


class DraftSection(Sourced):
    heading: str
    text: str


class ContractOutput(StageCommon):
    clause_positions: list[ClausePosition]
    draft_sections: list[DraftSection]


# ---------- Stage 6: Sign-off tracker ----------

class ChecklistItem(Sourced):
    item: str
    owner: str
    due: str
    status: Literal["outstanding", "done"]


class ClockStart(Sourced):
    confirmed: bool
    basis: str


class SignoffOutput(StageCommon):
    checklist: list[ChecklistItem]
    clock_start: ClockStart
    outstanding_approvals: list[str]


SCHEMAS: dict[int, type[StageCommon]] = {
    1: IntakeOutput,
    2: RequirementsOutput,
    3: ReuseOutput,
    4: PlanOutput,
    5: ContractOutput,
    6: SignoffOutput,
}
