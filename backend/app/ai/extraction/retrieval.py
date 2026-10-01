from __future__ import annotations

"""
Topic-focused retrieval.

Instead of sending the whole document to the LLM in chunks, each kind
of information (identity, dates, eligibility) gets a small "context
pack": the few passages most likely to contain it, sized to fit the
provider's token budget. Deterministic, no LLM, no dependencies.
"""

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum

from app.ai.extraction.dates import count_dates
from app.ai.extraction.structure import Passage
from app.ai.token_budget import estimate_text_tokens


class Facet(str, Enum):
    IDENTITY = "identity"
    DATES = "dates"
    ELIGIBILITY = "eligibility"


_TERMS: dict[Facet, dict[str, float]] = {
    Facet.IDENTITY: {
        "notification": 2, "advertisement": 2, "bulletin": 1.5, "brochure": 1.5,
        "information": 1, "conducted": 2, "organised": 2, "organized": 2,
        "organising": 2, "organizing": 2, "institute": 1, "commission": 1.5,
        "board": 1, "authority": 1, "agency": 1.5, "council": 1,
        "university": 1, "revised": 1.5, "version": 1, "issued": 1.5,
        "released": 1.5, "examination": 1, "exam": 1, "test": 0.5,
    },
    Facet.DATES: {
        "date": 2, "dates": 2, "schedule": 2, "deadline": 2.5, "last": 1,
        "application": 2, "registration": 2, "opening": 2, "closing": 2,
        "closes": 2, "opens": 2, "commencement": 1.5, "examination": 1,
        "exam": 1, "portal": 1, "extended": 1, "important": 1.5,
        "online": 0.5, "apply": 1, "till": 0.7, "between": 0.7,
        "announced": 0.7, "admit": 0.5, "result": 0.5,
    },
    Facet.ELIGIBILITY: {
        "eligibility": 4, "eligible": 3, "criteria": 2, "age": 2.5,
        "limit": 2, "qualification": 3, "qualifying": 2.5, "degree": 2,
        "nationality": 3, "citizen": 3, "citizens": 3, "indian": 1,
        "minimum": 1.5, "maximum": 1.5, "marks": 1, "percentage": 2,
        "cgpa": 2, "experience": 2, "relaxation": 1, "graduate": 2,
        "diploma": 1, "born": 2, "birth": 2, "pursuing": 1.5,
        "completed": 1, "year": 0.4, "domicile": 2, "residents": 1,
    },
}

_PATTERNS: dict[Facet, list[tuple[re.Pattern[str], float]]] = {
    Facet.IDENTITY: [
        (re.compile(r"\b(?:organi[sz]ed|conducted|issued|released) by\b", re.I), 3),
        (re.compile(r"\b(?:revised|version|notification|advertisement)\b.{0,40}\bdate\b", re.I), 2),
    ],
    Facet.DATES: [
        (re.compile(r"\b(?:last date|closing date|opening|commence)", re.I), 2),
        (re.compile(r"\b(?:to be announced|tba)\b", re.I), 1),
    ],
    Facet.ELIGIBILITY: [
        (re.compile(r"\b(?:age|aged)\b.{0,50}\b\d{2}\b", re.I), 2.5),
        (re.compile(r"\b(?:citizen|national)s? of india|indian national", re.I), 3),
        (re.compile(r"\b(?:must|should|shall)\s+(?:have|be|possess|hold|not)\b", re.I), 1),
        (re.compile(r"\b(?:currently|already)\b.{0,40}\b(?:year|completed|pursuing)\b", re.I), 1.5),
        (re.compile(r"\bnot (?:be )?(?:more|less|below|above|older|younger)\b", re.I), 2),
    ],
}

_TITLE_TERMS: dict[Facet, tuple[str, ...]] = {
    Facet.IDENTITY: ("highlight", "about", "introduction", "overview", "notification"),
    Facet.DATES: ("date", "schedule", "calendar", "important"),
    Facet.ELIGIBILITY: ("eligib", "qualification", "criteria", "who can"),
}

_NEGATIVE_TITLE = re.compile(
    r"syllabus|question paper|sample|model paper|declaration|undertaking|"
    r"format of|proforma|certificate|annexure|abbreviation",
    re.I,
)

_FEEDBACK_HINTS: dict[Facet, tuple[str, ...]] = {
    Facet.IDENTITY: ("name", "body", "organi", "conduct", "authority", "release"),
    Facet.DATES: ("date", "deadline", "last", "start", "end", "open", "close", "schedule"),
    Facet.ELIGIBILITY: (
        "eligib", "age", "qualif", "nationality", "degree", "experience",
        "marks", "percentage", "cgpa", "rule",
    ),
}

_STOP = {
    "the", "and", "for", "with", "that", "this", "from", "are", "was",
    "were", "not", "but", "has", "have", "been", "should", "please",
    "incorrect", "wrong", "check", "again", "document",
}

_WORD = re.compile(r"[a-z0-9]+")


def _tokens(text: str) -> list[str]:
    return _WORD.findall(text.lower())


@dataclass(slots=True)
class ContextPack:
    facet: Facet
    passages: list[Passage]
    scores: dict[str, float] = field(default_factory=dict)
    tokens: int = 0

    @property
    def pages(self) -> list[int]:
        return sorted({p for passage in self.passages for p in passage.pages})

    @property
    def text(self) -> str:
        return self.render()

    def render(self) -> str:
        return "\n\n".join(passage.tagged() for passage in self.passages)

    def describe(self) -> dict:
        return {
            "facet": self.facet.value,
            "passages": [p.id for p in self.passages],
            "pages": self.pages,
            "tokens": self.tokens,
        }


def facets_from_feedback(feedback: str | None) -> set[Facet]:
    if not feedback:
        return set()
    text = feedback.lower()
    return {
        facet
        for facet, hints in _FEEDBACK_HINTS.items()
        if any(hint in text for hint in hints)
    }


class PassageIndex:
    """BM25 index over a document's passages."""

    def __init__(self, passages: list[Passage]) -> None:
        self.passages = passages
        self._tf: list[Counter[str]] = []
        self._len: list[int] = []
        df: Counter[str] = Counter()

        for passage in passages:
            tokens = _tokens(passage.text) + _tokens(passage.section) * 2
            counts = Counter(tokens)
            self._tf.append(counts)
            self._len.append(len(tokens))
            df.update(counts.keys())

        n = max(1, len(passages))
        self._avg = (sum(self._len) / n) or 1.0
        self._idf = {
            term: math.log(1 + (n - freq + 0.5) / (freq + 0.5))
            for term, freq in df.items()
        }

    def bm25(self, index: int, weights: dict[str, float]) -> float:
        k1, b = 1.2, 0.75
        tf = self._tf[index]
        norm = k1 * (1 - b + b * self._len[index] / self._avg)
        score = 0.0
        for term, weight in weights.items():
            freq = tf.get(term, 0)
            if freq:
                score += weight * self._idf.get(term, 0.0) * (
                    freq * (k1 + 1) / (freq + norm)
                )
        return score

    def score_all(
        self,
        facet: Facet,
        extra_terms: dict[str, float] | None = None,
    ) -> list[float]:
        weights = dict(_TERMS[facet])
        if extra_terms:
            for term, weight in extra_terms.items():
                weights[term] = max(weights.get(term, 0.0), weight)

        raw = [self.bm25(i, weights) for i in range(len(self.passages))]
        top = max(raw) if raw else 0.0
        scores = [value / top * 10 if top else 0.0 for value in raw]

        for i, passage in enumerate(self.passages):
            text = passage.text
            bonus = 0.0

            for pattern, weight in _PATTERNS[facet]:
                if pattern.search(text):
                    bonus += weight

            section = passage.section.lower()
            if any(term in section for term in _TITLE_TERMS[facet]):
                bonus += 3

            if facet is Facet.DATES:
                dates = count_dates(text)
                bonus += min(dates, 6) * 0.7
                if dates == 0:
                    scores[i] *= 0.4

            if facet is Facet.IDENTITY:
                # Front matter states who is issuing the notification.
                if passage.page_start <= 3:
                    bonus += 4 - passage.page_start

            scores[i] += bonus

            if _NEGATIVE_TITLE.search(passage.section):
                scores[i] *= 0.4

        return scores


def build_pack(
    index: PassageIndex,
    facet: Facet,
    *,
    token_budget: int,
    feedback: str | None = None,
    min_relative_score: float = 0.25,
) -> ContextPack:
    extra: dict[str, float] = {}
    if feedback and facet in facets_from_feedback(feedback):
        for token in _tokens(feedback):
            if len(token) > 3 and token not in _STOP:
                extra[token] = 2.0

    scores = index.score_all(facet, extra)
    passages = index.passages
    order = sorted(range(len(passages)), key=lambda i: -scores[i])

    if not order or scores[order[0]] <= 0:
        return ContextPack(facet=facet, passages=[])

    top = scores[order[0]]
    chosen: set[int] = set()
    used = 0

    def cost(i: int) -> int:
        return estimate_text_tokens(passages[i].tagged()) + 4

    for i in order:
        if scores[i] < top * min_relative_score:
            break
        c = cost(i)
        if used + c > token_budget:
            continue
        chosen.add(i)
        used += c

    # Continuity: neighbours of selected passages in the same section
    # (a table or list often continues in the next passage).
    for i in sorted(chosen, key=lambda j: -scores[j]):
        for j in (i - 1, i + 1):
            if not (0 <= j < len(passages)) or j in chosen:
                continue
            if passages[j].section != passages[i].section:
                continue
            c = cost(j)
            if scores[j] > 0 and used + c <= token_budget:
                chosen.add(j)
                used += c

    selected = [passages[i] for i in sorted(chosen)]

    return ContextPack(
        facet=facet,
        passages=selected,
        scores={passages[i].id: round(scores[i], 2) for i in sorted(chosen)},
        tokens=used,
    )


# ---------------------------------------------------------------------------
# Convenience API used by the pipeline
# ---------------------------------------------------------------------------

def build_index(passages: list[Passage]) -> PassageIndex:
    return PassageIndex(passages)


def retrieve(
    passages: list[Passage],
    facet: Facet,
    *,
    token_budget: int,
    feedback: str | None = None,
    index: PassageIndex | None = None,
) -> ContextPack:
    return build_pack(
        index or PassageIndex(passages),
        facet,
        token_budget=token_budget,
        feedback=feedback,
    )
