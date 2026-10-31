"""Data-source layer: read the sample Word documents into text the agents can cite.

Paragraphs and tables are kept in document order. Headings become Markdown headings and
tables become pipe tables, so every ID (R-05, KS-LG-01, C-11 ...) survives intact.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "Data Sources"
RAD_TRACKER = ROOT / "Risk-Assumption-Dependency-Tracker.docx"

# Short keys the agents and prompts use for each source.
SOURCES = {
    "rfp": DATA_DIR / "Sample - 1 California RFP.docx",
    "kansas_assets": DATA_DIR / "Sample - 2 Kansas UX assets.docx",
    "compliance": DATA_DIR / "Sample - 3 Compliance rules.docx",
    "skills_rates": DATA_DIR / "Sample - 4 Skills and rates.docx",
    "contracts": DATA_DIR / "Sample - 5 Contract library.docx",
    "past_bids": DATA_DIR / "Sample - 6 Past bids.docx",
    "rad_tracker": RAD_TRACKER,
}


@dataclass
class SourceDoc:
    key: str
    path: Path
    text: str
    tables: list[list[list[str]]] = field(default_factory=list)  # table -> rows -> cells

    def table_with_header(self, first_header: str) -> list[dict[str, str]]:
        """Rows of the first table whose first header cell matches, as dicts keyed by header."""
        for table in self.tables:
            if table and table[0] and table[0][0].strip().lower() == first_header.lower():
                header = table[0]
                return [dict(zip(header, row)) for row in table[1:]]
        raise KeyError(f"{self.key}: no table starting with header {first_header!r}")


def _cell_text(cell) -> str:
    return " ".join(p.text.strip() for p in cell.paragraphs if p.text.strip())


def _read(path: Path) -> tuple[str, list[list[list[str]]]]:
    doc = Document(str(path))
    lines: list[str] = []
    tables: list[list[list[str]]] = []
    for child in doc.element.body.iterchildren():
        tag = child.tag.rsplit("}", 1)[-1]
        if tag == "p":
            para = Paragraph(child, doc)
            text = para.text.strip()
            if not text:
                continue
            style = (para.style.name or "").lower() if para.style is not None else ""
            if style.startswith("heading") or style == "title":
                level = 1 if style == "title" else int(style.split()[-1]) if style.split()[-1].isdigit() else 2
                lines.append(f"{'#' * level} {text}")
            elif "list" in style:
                lines.append(f"- {text}")
            else:
                lines.append(text)
        elif tag == "tbl":
            rows = [[_cell_text(c) for c in row.cells] for row in Table(child, doc).rows]
            tables.append(rows)
            if rows:
                lines.append("| " + " | ".join(rows[0]) + " |")
                lines.append("| " + " | ".join("---" for _ in rows[0]) + " |")
                lines.extend("| " + " | ".join(r) + " |" for r in rows[1:])
        lines.append("")
    return "\n".join(lines).strip() + "\n", tables


def load_sources() -> dict[str, SourceDoc]:
    docs = {}
    for key, path in SOURCES.items():
        if not path.exists():
            raise FileNotFoundError(f"Missing data source: {path}")
        text, tables = _read(path)
        docs[key] = SourceDoc(key=key, path=path, text=text, tables=tables)
    return docs


def sources_block(docs: dict[str, SourceDoc], keys: list[str]) -> str:
    """The data-source text for a prompt, each document wrapped in a tagged block."""
    parts = []
    for key in keys:
        d = docs[key]
        parts.append(f'<document key="{key}" file="{d.path.name}">\n{d.text}</document>')
    return "\n\n".join(parts)
