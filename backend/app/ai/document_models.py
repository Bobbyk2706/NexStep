from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class DocumentPage:
    """
    Represents one physical page of the source document.

    Page numbers are 1-based because they correspond directly to
    the page numbers an administrator sees in a PDF viewer.
    """

    page_number: int
    text: str

    @property
    def has_text(self) -> bool:
        return bool(self.text.strip())

    @property
    def character_count(self) -> int:
        return len(self.text)


@dataclass(slots=True)
class DocumentSection:
    """
    Represents a logical section detected across one or more PDF pages.

    A section is intentionally independent from the physical PDF page.
    One logical section can span multiple pages.
    """

    section_id: str
    title: str
    pages: list[DocumentPage] = field(default_factory=list)

    heading_level: int | None = None
    start_page: int | None = None
    end_page: int | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def text(self) -> str:
        return "\n\n".join(
            page.text
            for page in self.pages
            if page.text.strip()
        )

    @property
    def page_numbers(self) -> list[int]:
        return [
            page.page_number
            for page in self.pages
        ]

    @property
    def character_count(self) -> int:
        return len(self.text)

    @property
    def has_text(self) -> bool:
        return bool(self.text.strip())


@dataclass(slots=True)
class ParsedDocument:
    """
    Page-aware representation of an official source document.

    The original page boundaries are preserved deliberately.
    They are required later for evidence, validation and admin review.
    """

    source_url: str
    document_hash: str
    file_path: str | None

    pages: list[DocumentPage] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def page_count(self) -> int:
        return len(self.pages)

    @property
    def text(self) -> str:
        return "\n\n".join(
            page.text
            for page in self.pages
            if page.text.strip()
        )

    @property
    def character_count(self) -> int:
        return len(self.text)

    @property
    def non_empty_pages(self) -> list[DocumentPage]:
        return [
            page
            for page in self.pages
            if page.has_text
        ]

    def get_page(
        self,
        page_number: int,
    ) -> DocumentPage | None:
        """
        Return a page using its 1-based PDF page number.
        """

        for page in self.pages:
            if page.page_number == page_number:
                return page

        return None


@dataclass(slots=True)
class SectionedDocument:
    """
    Result of logical section detection.

    The original ParsedDocument is retained so downstream processing
    can always recover physical page provenance.
    """

    document: ParsedDocument
    sections: list[DocumentSection] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def section_count(self) -> int:
        return len(self.sections)

    def get_section(
        self,
        section_id: str,
    ) -> DocumentSection | None:
        for section in self.sections:
            if section.section_id == section_id:
                return section

        return None