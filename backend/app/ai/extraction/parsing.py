from __future__ import annotations

"""
Layout-aware PDF parsing.

Plain `page.get_text()` throws away exactly the things that matter most
in an official notification:

  * struck-through text (superseded dates in a revised notification
    look identical to current dates),
  * table structure (column-wise text extraction scrambles which date
    belongs to which label),
  * headings (needed to split the document into meaningful sections),
  * running headers/footers (noise repeated on every page).

This module rebuilds clean, ordered, page-aware text that keeps all of
that information, and records what it removed so a reviewer can see it.
"""

import os
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pymupdf

from app.ai.document_models import DocumentPage, ParsedDocument


_BULLETS = {"•", "◦", "▪", "■", "●", "○", "–", "-", "*", "·", "➢", "➤", "»"}

_HEADER_BAND = 0.09   # top 9 % of the page
_FOOTER_BAND = 0.91   # bottom 9 % of the page

# Marker prefix used in page text for detected headings.
HEADING_MARK = "#"

# A raw text line that would be mistaken for one of our heading markers.
_HEADING_LOOKALIKE = re.compile(r"^#{1,4}\s")

_ROMAN_PAGE_NO = re.compile(r"^[ivxlcdm]{1,7}$", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Internal structures
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class _Line:
    text: str                      # visible (non-struck) text
    struck: str                    # struck-out text on this line
    x0: float
    y0: float
    x1: float
    y1: float
    size: float
    bold: bool
    block: int


@dataclass(slots=True)
class _Table:
    bbox: pymupdf.Rect
    rows: list[list[str]]


@dataclass(slots=True)
class _PageLayout:
    number: int
    width: float
    height: float
    lines: list[_Line] = field(default_factory=list)
    tables: list[_Table] = field(default_factory=list)
    image_count: int = 0


# ---------------------------------------------------------------------------
# Small text helpers
# ---------------------------------------------------------------------------

def _clean(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u00a0", " ").replace("\u200b", "")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def _norm_key(text: str) -> str:
    """Key used to recognise the same header/footer on different pages."""
    text = _clean(text).lower()
    text = re.sub(r"\d+", "#", text)
    text = re.sub(r"\s+", " ", text)
    return text


def _is_bold(span: dict) -> bool:
    return bool(span.get("flags", 0) & 16) or "bold" in span.get("font", "").lower()


# ---------------------------------------------------------------------------
# Strikethrough detection
# ---------------------------------------------------------------------------

def _strike_rects(
    page: pymupdf.Page,
    drawings: list[dict] | None = None,
) -> list[pymupdf.Rect]:
    """
    Thin horizontal strokes/rectangles drawn on the page, plus explicit
    StrikeOut annotations. Word draws "strikethrough" as a vector line
    over the text, so it is only visible through the drawing commands.
    """

    rects: list[pymupdf.Rect] = []

    try:
        for drawing in (drawings if drawings is not None else page.get_drawings()):
            rect = drawing.get("rect")
            if rect is None:
                continue
            if rect.height <= 2.0 and rect.width >= 4.0:
                rects.append(pymupdf.Rect(rect))
    except Exception:
        pass

    try:
        for annot in page.annots() or []:
            if annot.type[0] == pymupdf.PDF_ANNOT_STRIKE_OUT:
                rects.append(pymupdf.Rect(annot.rect))
    except Exception:
        pass

    return rects


def _span_is_struck(bbox: pymupdf.Rect, strokes: list[pymupdf.Rect]) -> bool:
    """
    A span is struck when a thin horizontal stroke runs through the
    middle of it (not along the baseline = underline, not along an edge
    = table border) and covers most of its width.
    """

    if not strokes or bbox.width <= 0 or bbox.height <= 0:
        return False

    lo = bbox.y0 + 0.30 * bbox.height
    hi = bbox.y0 + 0.72 * bbox.height
    covered = 0.0

    for stroke in strokes:
        middle = (stroke.y0 + stroke.y1) / 2
        if lo <= middle <= hi:
            overlap = min(bbox.x1, stroke.x1) - max(bbox.x0, stroke.x0)
            if overlap > 0:
                covered += overlap

    return covered / bbox.width >= 0.6


# ---------------------------------------------------------------------------
# Page layout extraction
# ---------------------------------------------------------------------------

def _extract_layout(
    page: pymupdf.Page,
    *,
    strike: bool,
    tables: bool,
) -> _PageLayout:
    layout = _PageLayout(
        number=page.number + 1,
        width=page.rect.width,
        height=page.rect.height,
    )

    try:
        drawings = page.get_drawings() if (strike or tables) else []
    except Exception:
        drawings = []

    strokes = _strike_rects(page, drawings) if strike else []

    data = page.get_text("dict")

    for block_index, block in enumerate(data.get("blocks", [])):
        if block.get("type") == 1:
            layout.image_count += 1
            continue

        for line in block.get("lines", []):
            visible: list[str] = []
            struck: list[str] = []
            size = 0.0
            bold_chars = 0
            total_chars = 0

            for span in line.get("spans", []):
                text = span.get("text", "")
                if not text.strip():
                    visible.append(text)
                    continue

                bbox = pymupdf.Rect(span["bbox"])

                if _span_is_struck(bbox, strokes):
                    struck.append(text)
                    continue

                visible.append(text)
                size = max(size, float(span.get("size", 0.0)))
                total_chars += len(text.strip())
                if _is_bold(span):
                    bold_chars += len(text.strip())

            visible_text = _clean("".join(visible))
            struck_text = _clean("".join(struck))

            if not visible_text and not struck_text:
                continue

            x0, y0, x1, y1 = line["bbox"]

            layout.lines.append(
                _Line(
                    text=visible_text,
                    struck=struck_text,
                    x0=x0,
                    y0=y0,
                    x1=x1,
                    y1=y1,
                    size=size,
                    bold=bool(total_chars) and bold_chars / total_chars >= 0.9,
                    block=block_index,
                )
            )

    # Tables need ruling lines; pages without vector graphics have none.
    if tables and len(drawings) >= 4:
        layout.tables = _extract_tables(
            page,
            layout,
            _thin_horizontal(drawings),
        )

    return layout


def _thin_horizontal(drawings: list[dict]) -> list[pymupdf.Rect]:
    rects: list[pymupdf.Rect] = []

    for drawing in drawings:
        rect = drawing.get("rect")
        if rect is not None and rect.height <= 2.0 and rect.width >= 4.0:
            rects.append(pymupdf.Rect(rect))

    return rects


def _column_edges(table: Any, bbox: pymupdf.Rect) -> list[float]:
    """
    X positions of the column boundaries, taken from the cells that the
    table finder produced (edges that occur in a good share of rows).
    """

    counter: Counter[int] = Counter()
    total_rows = 0

    for row in table.rows:
        total_rows += 1
        for cell in row.cells:
            if cell is not None:
                counter[round(cell[0])] += 1
                counter[round(cell[2])] += 1

    if not total_rows:
        return []

    needed = max(2, int(0.25 * total_rows))
    edges = sorted(x for x, count in counter.items() if count >= needed)

    # Merge edges closer than 4pt (double borders).
    merged: list[float] = []
    for x in edges:
        if not merged or x - merged[-1] > 4:
            merged.append(float(x))

    if not merged or merged[0] - bbox.x0 > 4:
        merged.insert(0, bbox.x0)
    if bbox.x1 - merged[-1] > 4:
        merged.append(bbox.x1)

    return merged


def _row_edges(bbox: pymupdf.Rect, strokes: list[pymupdf.Rect]) -> list[float]:
    """
    Y positions of the rules that run across (nearly) the full table
    width. These are the real row separators; the table finder's own
    row list is often much noisier than what the reader sees.
    """

    ys: list[float] = []

    # Word draws each rule as one segment per column, so group segments
    # that sit on (nearly) the same y and add up their covered width.
    inside = sorted(
        (
            ((stroke.y0 + stroke.y1) / 2, stroke)
            for stroke in strokes
            if bbox.y0 - 2 <= (stroke.y0 + stroke.y1) / 2 <= bbox.y1 + 2
        ),
        key=lambda item: item[0],
    )

    groups: list[list[pymupdf.Rect]] = []
    last_y = None

    for y, stroke in inside:
        if last_y is None or y - last_y > 1.5:
            groups.append([])
        groups[-1].append(stroke)
        last_y = y

    for group in groups:
        spans = sorted((max(s.x0, bbox.x0), min(s.x1, bbox.x1)) for s in group)
        covered = 0.0
        cursor = None
        for start, end in spans:
            if end <= start:
                continue
            if cursor is None or start > cursor:
                covered += end - start
                cursor = end
            elif end > cursor:
                covered += end - cursor
                cursor = end
        if covered >= 0.85 * bbox.width:
            ys.append(sum((s.y0 + s.y1) / 2 for s in group) / len(group))

    ys.sort()

    merged: list[float] = []
    for y in ys:
        if not merged or y - merged[-1] > 3:
            merged.append(y)

    if not merged or merged[0] - bbox.y0 > 3:
        merged.insert(0, bbox.y0)
    if bbox.y1 - merged[-1] > 3:
        merged.append(bbox.y1)

    return merged


def _join_cell_lines(lines: list[_Line], cell_right: float) -> str:
    """
    Join the lines of one table cell: soft-wrapped text is joined with a
    space, separate stacked values with "; ".
    """

    lines = sorted(lines, key=lambda line: (round(line.y0), line.x0))
    text = ""

    for index, line in enumerate(lines):
        if index == 0:
            text = line.text
            continue

        previous = lines[index - 1]
        wrapped = previous.x1 >= cell_right - 10 and not previous.text.endswith(
            (".", ":", ";")
        )
        text += (" " if wrapped else "; ") + line.text

    return text.strip()


def _extract_tables(
    page: pymupdf.Page,
    layout: _PageLayout,
    strokes: list[pymupdf.Rect],
) -> list[_Table]:
    """
    Detect ruled tables and rebuild each cell from the page's own lines
    (so struck-out text stays out of cells).
    """

    try:
        finder = page.find_tables()
    except Exception:
        return []

    result: list[_Table] = []

    for table in finder.tables:
        bbox = pymupdf.Rect(table.bbox)

        try:
            columns = _column_edges(table, bbox)
            rows_y = _row_edges(bbox, strokes)
        except Exception:
            continue

        rows: list[list[str]] = []

        if len(columns) >= 3 and len(rows_y) >= 3:
            # Grid built from column edges x row rules.
            inside = [
                line
                for line in layout.lines
                if line.text
                and bbox.contains(
                    pymupdf.Point(
                        (line.x0 + line.x1) / 2,
                        (line.y0 + line.y1) / 2,
                    )
                )
            ]

            for r in range(len(rows_y) - 1):
                top, bottom = rows_y[r], rows_y[r + 1]
                row_values: list[str] = []

                for c in range(len(columns) - 1):
                    left, right = columns[c], columns[c + 1]
                    cell_lines = [
                        line
                        for line in inside
                        if top <= (line.y0 + line.y1) / 2 < bottom
                        and left <= (line.x0 + line.x1) / 2 < right
                    ]
                    row_values.append(_join_cell_lines(cell_lines, right))

                if any(row_values):
                    rows.append(row_values)

        else:
            # Fallback: the table finder's own rows.
            for row in table.rows:
                row_values = []

                for cell in row.cells:
                    if cell is None:
                        row_values.append("")
                        continue

                    rect = pymupdf.Rect(cell)
                    cell_lines = [
                        line
                        for line in layout.lines
                        if line.text
                        and rect.contains(
                            pymupdf.Point(
                                (line.x0 + line.x1) / 2,
                                (line.y0 + line.y1) / 2,
                            )
                        )
                    ]
                    row_values.append(_join_cell_lines(cell_lines, rect.x1))

                if any(row_values):
                    rows.append(row_values)

        non_empty = sum(1 for row in rows for value in row if value)

        # Ignore banners/decorations: needs a real grid with content.
        if len(rows) < 2 or non_empty < 3:
            continue
        if max(len(row) for row in rows) < 2:
            continue

        result.append(_Table(bbox=bbox, rows=rows))

    return result


# ---------------------------------------------------------------------------
# Document-level statistics
# ---------------------------------------------------------------------------

def _body_font_size(layouts: list[_PageLayout]) -> float:
    counter: Counter[float] = Counter()

    for layout in layouts:
        for line in layout.lines:
            if line.text and line.size:
                counter[round(line.size, 1)] += len(line.text)

    if not counter:
        return 10.0

    return counter.most_common(1)[0][0]


def _repeated_margin_lines(layouts: list[_PageLayout]) -> set[str]:
    """
    Keys of lines that repeat in the header/footer band of many pages.
    """

    if len(layouts) < 4:
        return set()

    counter: Counter[str] = Counter()

    for layout in layouts:
        seen: set[str] = set()

        for line in layout.lines:
            if not line.text:
                continue
            in_band = (
                line.y1 <= layout.height * _HEADER_BAND
                or line.y0 >= layout.height * _FOOTER_BAND
            )
            if in_band:
                seen.add(_norm_key(line.text))

        counter.update(seen)

    threshold = max(3, int(0.25 * len(layouts)))

    return {key for key, count in counter.items() if count >= threshold}


# ---------------------------------------------------------------------------
# Headings and paragraphs
# ---------------------------------------------------------------------------

def _looks_like_heading(line: _Line, body_size: float) -> bool:
    text = line.text

    if not (3 <= len(text) <= 120):
        return False
    if text in _BULLETS:
        return False
    if not re.search(r"[A-Za-z]", text):
        return False
    if text.endswith((",", ";")):
        return False
    # Sentences are not headings.
    if text.endswith(".") and len(text.split()) > 8:
        return False
    if len(text.split()) > 16:
        return False

    larger = line.size >= body_size * 1.15
    return larger or (line.bold and len(text.split()) <= 14)


def _heading_level(text: str, size: float, body_size: float) -> int:
    numbered = re.match(r"^(\d+(?:\.\d+)*)[.)]?\s", text)

    if numbered:
        return min(4, numbered.group(1).count(".") + 1)

    if size >= body_size * 1.6:
        return 1
    if size >= body_size * 1.3:
        return 2
    return 3


def _page_text(
    layout: _PageLayout,
    *,
    body_size: float,
    margin_keys: set[str],
    strip_margins: bool,
) -> tuple[str, dict[str, Any]]:
    """
    Turn one page's layout into clean text with heading markers and
    table blocks, in reading order.
    """

    meta: dict[str, Any] = {
        "struck": [],
        "tables": len(layout.tables),
        "headings": [],
        "removed_margin_lines": [],
    }

    table_boxes = [table.bbox for table in layout.tables]

    def in_table(line: _Line) -> int | None:
        centre = pymupdf.Point((line.x0 + line.x1) / 2, (line.y0 + line.y1) / 2)
        for index, box in enumerate(table_boxes):
            if box.contains(centre):
                return index
        return None

    out: list[str] = []
    emitted_tables: set[int] = set()

    paragraph: list[_Line] = []

    def flush() -> None:
        if not paragraph:
            return

        pieces: list[str] = []
        block_right = max(line.x1 for line in paragraph)
        pending_bullet = False

        for index, line in enumerate(paragraph):
            text = line.text

            if text in _BULLETS:
                pending_bullet = True
                continue

            if pending_bullet:
                text = f"• {text}"
                pending_bullet = False

            pieces.append(text)

            following = paragraph[index + 1] if index + 1 < len(paragraph) else None
            if following is None:
                continue

            # Soft-wrapped line: reaches the right edge and the next
            # line does not start a new bullet / numbered item.
            full_width = line.x1 >= block_right - 14
            starts_item = bool(
                re.match(r"^(•|\d+[.)]\s|\([a-z0-9]+\)\s|[a-z][.)]\s)", following.text)
            ) or following.text in _BULLETS

            if full_width and not starts_item and not text.endswith(":"):
                if re.search(r"[A-Za-z]-$", text) and following.text[:1].islower():
                    pieces[-1] = text[:-1]
                    pieces.append("\x00")      # join without space
                else:
                    pieces.append("\x01")      # join with space
            else:
                pieces.append("\n")

        joined = ""
        for piece in pieces:
            if piece == "\x00":
                continue
            if piece == "\x01":
                joined += " "
            elif piece == "\n":
                joined += "\n"
            else:
                joined += piece

        joined = re.sub(r"[ ]{2,}", " ", joined)
        for row in joined.split("\n"):
            row = row.strip()
            if row:
                out.append("\\" + row if _HEADING_LOOKALIKE.match(row) else row)

        paragraph.clear()

    previous_block = None

    for line in layout.lines:
        if line.struck:
            meta["struck"].append(line.struck)

        if not line.text:
            continue

        table_index = in_table(line)

        if table_index is not None:
            flush()
            if table_index not in emitted_tables:
                emitted_tables.add(table_index)
                out.append(_render_table(layout.tables[table_index]))
            previous_block = None
            continue

        in_band = (
            line.y1 <= layout.height * _HEADER_BAND
            or line.y0 >= layout.height * _FOOTER_BAND
        )

        if strip_margins and in_band and _norm_key(line.text) in margin_keys:
            meta["removed_margin_lines"].append(line.text)
            continue

        if (
            in_band
            and strip_margins
            and (
                re.fullmatch(r"\d{1,4}", line.text)
                or _ROMAN_PAGE_NO.match(line.text)
            )
        ):
            continue

        if _looks_like_heading(line, body_size):
            flush()
            level = _heading_level(line.text, line.size, body_size)
            out.append(f"{HEADING_MARK * level} {line.text}")
            meta["headings"].append(line.text)
            previous_block = None
            continue

        if previous_block is not None and line.block != previous_block:
            flush()

        previous_block = line.block
        paragraph.append(line)

    flush()

    return "\n".join(out).strip(), meta


def _render_table(table: _Table) -> str:
    rendered = []

    for row in table.rows:
        cells = [cell for cell in row if cell]
        if cells:
            rendered.append(" | ".join(cells))

    return "[TABLE]\n" + "\n".join(rendered) + "\n[/TABLE]"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def parse_pdf(
    source: bytes | bytearray | str | os.PathLike,
    *,
    source_url: str = "",
    document_hash: str = "",
    file_path: str | None = None,
    detect_strikethrough: bool = True,
    extract_tables: bool = False,
    strip_margins: bool = True,
) -> ParsedDocument:
    """
    Parse a PDF into a page-aware ParsedDocument with clean text.

    Table detection is the slowest step (roughly 0.15 s per page), so by
    default it is skipped here and applied afterwards, only to the pages
    that retrieval actually selects (see `add_tables_to_pages`).
    """

    if isinstance(source, (bytes, bytearray)):
        document = pymupdf.open(stream=bytes(source), filetype="pdf")
        file_path = file_path
    else:
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"PDF file not found: {path}")
        document = pymupdf.open(path)
        file_path = file_path or str(path)

    try:
        layouts = [
            _extract_layout(
                page,
                strike=detect_strikethrough,
                tables=extract_tables,
            )
            for page in document
        ]
        pdf_metadata = dict(document.metadata or {})
    finally:
        document.close()

    body_size = _body_font_size(layouts)
    margin_keys = _repeated_margin_lines(layouts) if strip_margins else set()

    pages: list[DocumentPage] = []
    struck_total: list[dict[str, Any]] = []
    scanned_pages: list[int] = []
    margin_counter: Counter[str] = Counter()

    for layout in layouts:
        text, meta = _page_text(
            layout,
            body_size=body_size,
            margin_keys=margin_keys,
            strip_margins=strip_margins,
        )

        if not text and layout.image_count:
            scanned_pages.append(layout.number)
            meta["scanned"] = True

        for removed in meta["removed_margin_lines"]:
            margin_counter[removed] += 1

        for struck in meta["struck"]:
            struck_total.append({"page": layout.number, "text": struck})

        pages.append(
            DocumentPage(
                page_number=layout.number,
                text=text,
                metadata=meta,
            )
        )

    running_header = ""
    if margin_counter:
        running_header = margin_counter.most_common(1)[0][0]

    return ParsedDocument(
        source_url=source_url,
        document_hash=document_hash,
        file_path=file_path,
        pages=pages,
        metadata={
            "parser": "nexstep-layout-v2",
            "body_font_size": body_size,
            "pdf_metadata": pdf_metadata,
            "superseded_text": struck_total,
            "scanned_pages": scanned_pages,
            "running_header": running_header,
            "table_count": sum(len(layout.tables) for layout in layouts),
            "tables_extracted_pages": (
                [layout.number for layout in layouts] if extract_tables else []
            ),
            # Document-level statistics reused by add_tables_to_pages().
            "_margin_keys": sorted(margin_keys),
            "_detect_strikethrough": detect_strikethrough,
            "_strip_margins": strip_margins,
        },
    )


def add_tables_to_pages(
    document: ParsedDocument,
    source: bytes | bytearray | str | os.PathLike,
    page_numbers: list[int],
) -> list[int]:
    """
    Re-render the given pages with table structure and replace their text
    in `document` (in place). Returns the pages that were changed.
    """

    already = set(document.metadata.get("tables_extracted_pages", []))
    wanted = sorted({n for n in page_numbers if n not in already})

    if not wanted:
        return []

    if isinstance(source, (bytes, bytearray)):
        pdf = pymupdf.open(stream=bytes(source), filetype="pdf")
    else:
        pdf = pymupdf.open(Path(source))

    body_size = float(document.metadata.get("body_font_size") or 10.0)
    margin_keys = set(document.metadata.get("_margin_keys", []))
    strike = bool(document.metadata.get("_detect_strikethrough", True))
    strip = bool(document.metadata.get("_strip_margins", True))

    changed: list[int] = []

    try:
        for number in wanted:
            if not (1 <= number <= len(pdf)):
                continue

            layout = _extract_layout(pdf[number - 1], strike=strike, tables=True)

            text, meta = _page_text(
                layout,
                body_size=body_size,
                margin_keys=margin_keys,
                strip_margins=strip,
            )

            page = document.get_page(number)
            if page is None:
                continue

            if layout.tables:
                page.text = text
                page.metadata = {**page.metadata, **meta}
                changed.append(number)

            already.add(number)
    finally:
        pdf.close()

    document.metadata["tables_extracted_pages"] = sorted(already)
    document.metadata["table_count"] = int(
        document.metadata.get("table_count", 0)
    ) + len(changed)

    return changed


def parse_text_pages(
    pages: list[str],
    *,
    source_url: str = "",
    document_hash: str = "",
    file_path: str | None = None,
) -> ParsedDocument:
    """
    Fallback for callers that only have plain per-page text (no layout).
    Headings are found later by pattern instead of by font.
    """

    return ParsedDocument(
        source_url=source_url,
        document_hash=document_hash,
        file_path=file_path,
        pages=[
            DocumentPage(page_number=index, text=_clean_plain(text))
            for index, text in enumerate(pages, start=1)
        ],
        metadata={"parser": "plain-text"},
    )


def _clean_plain(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "")
    text = text.replace("\u00a0", " ")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)
