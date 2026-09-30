from __future__ import annotations

"""
Split a parsed document into retrieval passages that keep their section
title and page provenance.
"""

import re
from dataclasses import dataclass

from app.ai.document_models import ParsedDocument
from app.ai.token_budget import estimate_text_tokens

_HEADING = re.compile(r"^(#{1,4}) (.+)$")
_PLAIN_HEADING = re.compile(r"^\d+(?:\.\d+){0,2}[.)]?\s+[A-Z][^.]{2,90}$")
_TOC_LINE = re.compile(r"\.{4,}\s*\d+\s*$")


@dataclass(slots=True)
class Passage:
    id: str
    index: int
    page_start: int
    page_end: int
    section: str
    text: str
    tokens: int = 0
    is_table: bool = False

    @property
    def pages(self) -> list[int]:
        return list(range(self.page_start, self.page_end + 1))

    def tagged(self) -> str:
        pages = (
            f"p.{self.page_start}"
            if self.page_start == self.page_end
            else f"p.{self.page_start}-{self.page_end}"
        )
        return f"[{self.id} | {pages} | {self.section}]\n{self.text}"


def is_toc_page(text: str) -> bool:
    lines = [line for line in text.splitlines() if line.strip()]
    hits = sum(1 for line in lines if _TOC_LINE.search(line))
    return hits >= 5 and hits >= 0.4 * max(1, len(lines))


def build_passages(
    document: ParsedDocument,
    *,
    max_chars: int = 1400,
) -> list[Passage]:
    passages: list[Passage] = []
    stack: list[tuple[int, str]] = []
    fonts_known = document.metadata.get("parser") != "plain-text"

    buf: list[str] = []
    buf_pages: list[int] = []
    buf_section = ""
    buf_table = False

    def section_title() -> str:
        return " > ".join(title for _, title in stack)[:160] or "Document"

    def flush() -> None:
        nonlocal buf, buf_pages, buf_table
        text = "\n".join(buf).strip()
        if text:
            passages.append(
                Passage(
                    id=f"P{len(passages) + 1}",
                    index=len(passages),
                    text=text,
                    tokens=estimate_text_tokens(text),
                    page_start=min(buf_pages),
                    page_end=max(buf_pages),
                    section=buf_section,
                    is_table=buf_table,
                )
            )
        buf, buf_pages, buf_table = [], [], False

    for page in document.pages:
        if not page.text.strip() or is_toc_page(page.text):
            continue

        in_table = False

        for raw in page.text.splitlines():
            line = raw.rstrip()
            if not line.strip():
                continue

            if line == "[TABLE]":
                flush()
                in_table = True
                buf_section, buf_table = section_title(), True
                continue
            if line == "[/TABLE]":
                flush()
                in_table = False
                continue

            if not in_table:
                heading = _HEADING.match(line)
                if not heading and not fonts_known and _PLAIN_HEADING.match(line):
                    heading = re.match(r"^()(.+)$", line)

                if heading:
                    flush()
                    level = len(heading.group(1)) or 2
                    while stack and stack[-1][0] >= level:
                        stack.pop()
                    stack.append((level, heading.group(2).strip()))
                    continue

            if not buf:
                buf_section = section_title()

            if not in_table and sum(len(x) + 1 for x in buf) + len(line) > max_chars:
                flush()
                buf_section = section_title()

            # Very long table: split by rows, never inside a row.
            if in_table and sum(len(x) + 1 for x in buf) + len(line) > max_chars * 2:
                header = buf[0] if buf else ""
                flush()
                buf_section, buf_table = section_title(), True
                if header:
                    buf.append(header)
                    buf_pages.append(page.page_number)

            buf.append(line)
            buf_pages.append(page.page_number)

        flush()

    return passages
