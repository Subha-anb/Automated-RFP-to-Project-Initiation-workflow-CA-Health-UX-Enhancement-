"""Publish the stage 6 sign-off checklist as an Excel workbook.

  python -m rfpflow.checklist_xlsx            latest run
  python -m rfpflow.checklist_xlsx --run 2
"""

from __future__ import annotations

import argparse
import json
from datetime import date

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

from . import store
from .config import OUTPUT_DIR, STAGES

FONT = "Arial"
HEAD_FILL = PatternFill("solid", fgColor="1F3864")
INPUT_FILL = PatternFill("solid", fgColor="FFFF00")
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def _header(ws, row, labels, widths):
    for col, (label, width) in enumerate(zip(labels, widths), start=1):
        c = ws.cell(row=row, column=col, value=label)
        c.font = Font(name=FONT, bold=True, color="FFFFFF")
        c.fill = HEAD_FILL
        c.alignment = Alignment(vertical="center", wrap_text=True)
        c.border = BOX
        ws.column_dimensions[get_column_letter(col)].width = width


def build(conn, run_id: int):
    row = store.get_stage(conn, run_id, 6)
    if not row or not row["output_json"]:
        raise SystemExit(f"Run {run_id} has no stage 6 output yet.")
    out = json.loads(row["output_json"])
    gate_state = "approved at H6" if row["status"] == "approved" else f"DRAFT - {STAGES[6].gate} not yet approved"
    items = out["checklist"]

    wb = Workbook()
    ws = wb.active
    ws.title = "Checklist"
    ws["A1"] = "Contract Sign-off Checklist - SAMPLE-CA-HUX-2026-014"
    ws["A1"].font = Font(name=FONT, bold=True, size=14)
    ws["A2"] = f"Run {run_id}, stage 6 attempt {row['attempt']} ({gate_state}). Generated {date.today():%b %d, %Y}."
    ws["A2"].font = Font(name=FONT, italic=True, color="595959")
    ws["A3"] = "Edit the yellow Status cells (Outstanding / Done); days to due and the Summary sheet update automatically."
    ws["A3"].font = Font(name=FONT, color="595959")

    labels = ["#", "Item", "Owner", "Due date", "Status", "Days to due", "Sources", "Assumption", "Assumption note"]
    _header(ws, 5, labels, [5, 62, 18, 12, 13, 11, 34, 12, 50])
    first = 6
    for i, it in enumerate(items):
        r = first + i
        values = [i + 1, it["item"], it["owner"], date.fromisoformat(it["due"]), it["status"].capitalize(),
                  f'=IF(E{r}="Done","",D{r}-TODAY())', ", ".join(it["source_refs"]),
                  "Yes" if it["assumption"] else "No", it["assumption_reason"]]
        for col, v in enumerate(values, start=1):
            c = ws.cell(row=r, column=col, value=v)
            c.font = Font(name=FONT)
            c.border = BOX
            c.alignment = Alignment(vertical="top", wrap_text=col in (2, 7, 9))
        ws.cell(row=r, column=4).number_format = "mmm d, yyyy"
        ws.cell(row=r, column=6).number_format = "0;[Red]-0"
        ws.cell(row=r, column=5).fill = INPUT_FILL
    last = first + len(items) - 1

    status_dv = DataValidation(type="list", formula1='"Outstanding,Done"', allow_blank=False)
    ws.add_data_validation(status_dv)
    status_dv.add(f"E{first}:E{last}")
    rng = f"A{first}:I{last}"
    ws.conditional_formatting.add(rng, FormulaRule(formula=[f'$E{first}="Done"'],
                                                   fill=PatternFill("solid", fgColor="E2EFDA")))
    ws.conditional_formatting.add(rng, FormulaRule(formula=[f'AND($E{first}="Outstanding",$D{first}<TODAY())'],
                                                   fill=PatternFill("solid", fgColor="FCE4E4")))
    ws.freeze_panes = f"C{first}"
    ws.auto_filter.ref = f"A5:I{last}"
    ws["F5"].comment = Comment("Due date minus today; negative (red) means overdue. Blank once done.", "rfpflow")

    s = wb.create_sheet("Summary")
    s.column_dimensions["A"].width = 38
    s.column_dimensions["B"].width = 70
    s["A1"] = "Sign-off Summary"
    s["A1"].font = Font(name=FONT, bold=True, size=14)
    rows = [
        ("Checklist items", f"=COUNTA(Checklist!B{first}:B{last})"),
        ("Done", f'=COUNTIF(Checklist!E{first}:E{last},"Done")'),
        ("Outstanding", f'=COUNTIF(Checklist!E{first}:E{last},"Outstanding")'),
        ("Overdue (outstanding, past due)", f'=COUNTIFS(Checklist!E{first}:E{last},"Outstanding",Checklist!D{first}:D{last},"<"&TODAY())'),
        ("Next due date (outstanding)", f'=IF(B5=0,"",_xlfn.MINIFS(Checklist!D{first}:D{last},Checklist!E{first}:E{last},"Outstanding"))'),
    ]
    for i, (label, formula) in enumerate(rows, start=3):
        s.cell(row=i, column=1, value=label).font = Font(name=FONT, bold=True)
        c = s.cell(row=i, column=2, value=formula)
        c.font = Font(name=FONT)
        c.alignment = Alignment(horizontal="left")
    s["B7"].number_format = "mmm d, yyyy"

    cs = out["clock_start"]
    s["A9"] = "Delivery clock start"
    s["A9"].font = Font(name=FONT, bold=True)
    s["B9"] = ("Confirmed: " if cs["confirmed"] else "Not confirmed: ") + cs["basis"]
    s["B10"] = "Sources: " + ", ".join(cs["source_refs"])
    s["A12"] = "Approvals still outstanding"
    s["A12"].font = Font(name=FONT, bold=True)
    for i, a in enumerate(out["outstanding_approvals"], start=12):
        s.cell(row=i, column=2, value=a)
    r = 13 + len(out["outstanding_approvals"])
    s.cell(row=r, column=1, value="Open questions").font = Font(name=FONT, bold=True)
    for i, q in enumerate(out["open_questions"], start=r):
        s.cell(row=i, column=2, value=q["question"])
    for row_cells in s.iter_rows(min_row=9):
        for c in row_cells:
            c.font = Font(name=FONT, bold=c.font.bold)
            c.alignment = Alignment(wrap_text=True, vertical="top")
    s["A2"] = "Counts are formulas over the Checklist sheet."
    s["A2"].font = Font(name=FONT, italic=True, color="595959")

    wb.calculation.fullCalcOnLoad = True
    path = OUTPUT_DIR / f"run-{run_id}" / "sign-off-checklist.xlsx"
    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)
    store.audit("checklist_published", run_id=run_id, path=str(path), gate_state=gate_state)
    return path


def main(argv=None):
    p = argparse.ArgumentParser(prog="rfpflow.checklist_xlsx")
    p.add_argument("--run", type=int)
    args = p.parse_args(argv)
    conn = store.connect()
    print(f"Wrote {build(conn, args.run or store.latest_run(conn))}")


if __name__ == "__main__":
    main()
