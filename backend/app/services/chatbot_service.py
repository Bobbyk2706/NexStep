from __future__ import annotations

import re
from dataclasses import dataclass, field

from sqlalchemy.orm import Session

from app.ai.provider_manager import (
    AIProviderManager,
    AllAIProvidersFailedError,
)
from app.models.exam import Exam
from app.models.student import Student
from app.services.eligibility_service import (
    evaluate_eligibility,
    get_exam_rule_groups,
)
from app.services.exam_service import get_all_exams

# ============================================================
# STUDENT-FACING AI CHATBOT ("Ask NexStep")
# ============================================================
#
# This is intentionally a thin, retrieval-grounded layer on top of
# the AI infrastructure that already exists in this codebase
# (AIProviderManager: Groq -> OpenRouter -> Local). It does NOT ask
# the LLM to recall exam facts from its own training data - it
# looks up the exam(s) the student is asking about in NexStep's own
# database (approved notification, dates, eligibility rules, and,
# when the student is logged in, their own computed eligibility),
# builds a short factual CONTEXT block from that, and asks the model
# to answer using only that context. If nothing in the database
# matches the question, the model is instructed to say so rather
# than guess - this matters a lot for an eligibility assistant,
# where a plausible-sounding wrong cutoff date is worse than no
# answer at all.

_MAX_HISTORY_MESSAGES = 6
_MAX_MATCHED_EXAMS = 3

_STOPWORDS = {
    "the", "a", "an", "is", "am", "are", "for", "of", "in", "on",
    "to", "and", "or", "do", "does", "can", "i", "my", "me", "you",
    "what", "when", "where", "how", "which", "will", "be", "eligible",
    "eligibility", "exam", "exams", "apply", "application", "about",
    "tell", "please", "hi", "hello", "hey",
}


def _tokenize(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if token not in _STOPWORDS and len(token) > 1
    }


@dataclass
class ChatbotSource:
    exam_id: int
    exam_name: str
    notification_title: str | None = None
    official_url: str | None = None


@dataclass
class ChatbotAnswer:
    answer: str
    sources: list[ChatbotSource] = field(default_factory=list)
    grounded: bool = True


# ============================================================
# EXAM MATCHING
# ============================================================


def _find_relevant_exams(
    db: Session,
    message: str,
) -> list[Exam]:
    """
    Find exams whose name/description share tokens with the
    student's message. Deliberately simple (no embeddings/vector
    search infrastructure exists in this project yet) but effective
    for exam-name-driven questions such as "Am I eligible for GATE
    2027?" or "When does JEE Mains registration close?".
    """

    message_tokens = _tokenize(message)

    if not message_tokens:
        return []

    all_exams = get_all_exams(db=db)

    scored: list[tuple[int, Exam]] = []

    for exam in all_exams:
        exam_tokens = _tokenize(exam.name or "")
        overlap = len(message_tokens & exam_tokens)

        if overlap == 0 and exam.description:
            # Weaker signal: description-only match still counts,
            # but less than a name match.
            desc_tokens = _tokenize(exam.description)
            if message_tokens & desc_tokens:
                overlap = 1

        if overlap > 0:
            scored.append((overlap, exam))

    scored.sort(key=lambda pair: pair[0], reverse=True)

    return [exam for _, exam in scored[:_MAX_MATCHED_EXAMS]]


# ============================================================
# CONTEXT BUILDING
# ============================================================


def _describe_rule_groups(groups, indent: str = "") -> list[str]:
    lines: list[str] = []

    for group in groups:
        rule_texts = [
            f"{rule.attribute.attribute_name} {rule.operator} {rule.value}"
            for rule in group.rules
        ]

        if rule_texts:
            lines.append(
                f"{indent}- ({group.logical_operator}) "
                + f" {group.logical_operator} ".join(rule_texts)
            )

        if group.child_groups:
            lines.extend(
                _describe_rule_groups(
                    group.child_groups,
                    indent=indent + "  ",
                )
            )

    return lines


def _build_exam_context(
    db: Session,
    exam: Exam,
    student: Student | None,
) -> tuple[str, ChatbotSource]:
    approved = [
        n
        for n in exam.official_notifications
        if n.approval_status == "APPROVED"
    ]
    dated = [n for n in approved if n.release_date is not None]
    if dated:
        latest = max(dated, key=lambda n: n.release_date)
    elif approved:
        latest = approved[0]
    else:
        latest = None

    lines = [
        f"EXAM: {exam.name}",
        f"Type: {exam.type}",
    ]

    if exam.description:
        lines.append(f"Description: {exam.description}")

    if exam.off_exam_page:
        lines.append(f"Official page: {exam.off_exam_page}")

    source = ChatbotSource(
        exam_id=exam.exam_id,
        exam_name=exam.name,
        official_url=exam.off_exam_page,
    )

    if latest is None:
        lines.append(
            "No approved official notification is on file for this "
            "exam yet, so specific dates/eligibility rules are not "
            "available."
        )
        return "\n".join(lines), source

    source.notification_title = latest.title

    lines.append(f"Latest official notification: {latest.title}")

    if latest.release_date:
        lines.append(f"Notification release date: {latest.release_date}")
    if latest.application_start_date:
        lines.append(
            f"Application start date: {latest.application_start_date}"
        )
    if latest.application_end_date:
        lines.append(
            f"Application end date: {latest.application_end_date}"
        )

    for exam_date in latest.exam_dates:
        lines.append(
            f"Exam date window: {exam_date.start_date} to "
            f"{exam_date.end_date}"
        )

    if latest.ai_summary:
        lines.append(f"Notification summary: {latest.ai_summary}")

    try:
        rule_groups = get_exam_rule_groups(exam.exam_id, db=db)
        rule_lines = _describe_rule_groups(rule_groups)
        if rule_lines:
            lines.append("Eligibility rules:")
            lines.extend(rule_lines)
    except ValueError:
        pass

    if student is not None:
        try:
            result = evaluate_eligibility(student, exam.exam_id, db=db)
            verdict = "ELIGIBLE" if result.eligible else "NOT ELIGIBLE"
            lines.append(
                f"This specific student's computed eligibility: "
                f"{verdict}. Reasons: {'; '.join(result.reasons)}"
            )
        except ValueError:
            pass

    return "\n".join(lines), source


# ============================================================
# LLM ANSWERING
# ============================================================

_SYSTEM_PROMPT = """You are "Ask NexStep", an in-app assistant that helps \
students understand exam eligibility, deadlines, and notifications on the \
NexStep platform.

Hard rules:
1. Answer using ONLY the facts given to you in the CONTEXT section below. \
Never use outside knowledge about specific exams, dates, or eligibility \
cutoffs, even if you believe you know them - NexStep's own database is the \
single source of truth here, and it can differ from what you'd otherwise \
assume.
2. If the CONTEXT does not contain the information needed to answer, say \
plainly that NexStep doesn't have that information yet, and suggest the \
student check the exam's official notification or ask about a specific \
exam by name. Do not guess or make up a plausible-sounding date, fee, or \
cutoff.
3. If a computed personal eligibility result is present in the CONTEXT, \
you may state it directly, but always mention it is based on the \
student's current saved profile so it stays accurate as that profile \
changes.
4. Keep answers concise and student-friendly. Use plain text, not markdown \
tables.
5. You only discuss exams, eligibility, and NexStep's own features. \
Politely decline anything else and steer back to exam eligibility/tracking.
"""


def answer_question(
    db: Session,
    message: str,
    student: Student | None = None,
    history: list[dict] | None = None,
) -> ChatbotAnswer:
    """
    Answer a student's question about exam eligibility/notifications.

    `history` is an optional list of {"role": "user"|"assistant",
    "content": str} from earlier in the same conversation, most-recent
    last. Only the last _MAX_HISTORY_MESSAGES are used, purely for
    conversational continuity (e.g. "and what about the fee?") - the
    factual grounding always comes fresh from the database on every
    call, never from what the model said earlier.
    """

    message = (message or "").strip()

    if not message:
        return ChatbotAnswer(
            answer="Ask me something about an exam - for example, "
            "\"Am I eligible for GATE 2027?\" or \"When does the JEE "
            "Mains application close?\"",
            grounded=False,
        )

    matched_exams = _find_relevant_exams(db, message)

    sources: list[ChatbotSource] = []
    context_blocks: list[str] = []

    for exam in matched_exams:
        block, source = _build_exam_context(db, exam, student)
        context_blocks.append(block)
        sources.append(source)

    if context_blocks:
        context_text = "\n\n".join(context_blocks)
    else:
        context_text = (
            "No exam in NexStep's database matched this question by "
            "name or description."
        )

    messages: list[dict] = [
        {"role": "system", "content": _SYSTEM_PROMPT},
    ]

    for turn in (history or [])[-_MAX_HISTORY_MESSAGES:]:
        role = turn.get("role")
        content = turn.get("content")
        if role in ("user", "assistant") and content:
            messages.append({"role": role, "content": content})

    messages.append(
        {
            "role": "user",
            "content": (
                f"CONTEXT:\n{context_text}\n\n"
                f"STUDENT QUESTION:\n{message}"
            ),
        }
    )

    manager = AIProviderManager()

    try:
        answer_text = manager.generate(
            messages=messages,
            temperature=0.2,
            max_tokens=600,
        )
    except AllAIProvidersFailedError:
        return ChatbotAnswer(
            answer=(
                "I'm having trouble reaching the AI service right now. "
                "Please try again in a moment."
            ),
            sources=sources,
            grounded=False,
        )

    return ChatbotAnswer(
        answer=answer_text.strip(),
        sources=sources,
        grounded=bool(context_blocks),
    )
