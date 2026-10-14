import re

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from app.database.session import SessionLocal
from app.models.conducting_body import ConductingBody
from app.models.exam import Exam
from app.models.official_notification import OfficialNotification


def create_exam(
    body_id,
    exam_name,
    exam_type,
    exam_description,
    official_exam_page,
    status,
):
    with SessionLocal() as s:
        body = s.scalar(
            select(ConductingBody).where(
                ConductingBody.body_id == body_id
            )
        )

        if body is None:
            raise ValueError("Conducting body not found.")

        exam = Exam(
            name=exam_name,
            type=exam_type,
            description=exam_description,
            off_exam_page=official_exam_page,
            status=status,
        )

        body.exams.append(exam)
        s.add(exam)
        s.commit()

        return exam.exam_id


def get_all_exams(db: Session | None = None):
    """
    Returns all exams that have an approved notification, with their
    conducting body.

    The function accepts an optional Session so callers such as
    FastAPI routes and tests can control the transaction/session.
    """
    owns_session = db is None

    if owns_session:
        db = SessionLocal()

    try:
        statement = (
            select(Exam)
            .join(
                OfficialNotification,
                OfficialNotification.exam_id == Exam.exam_id,
            )
            .where(
                OfficialNotification.approval_status == "APPROVED"
            )
            .options(selectinload(Exam.body))
            .distinct()
            .order_by(Exam.name.asc())
        )

        return list(db.scalars(statement).all())

    finally:
        if owns_session:
            db.close()


def get_exam_by_id(
    exam_id: int,
    db: Session | None = None,
):
    """
    Returns one exam with its conducting body and approved
    official notifications.
    """
    owns_session = db is None

    if owns_session:
        db = SessionLocal()

    try:
        statement = (
            select(Exam)
            .options(
                selectinload(Exam.body),
                selectinload(Exam.official_notifications),
            )
            .where(Exam.exam_id == exam_id)
        )

        return db.scalar(statement)

    finally:
        if owns_session:
            db.close()


def search_exams(
    query: str,
    db: Session | None = None,
):
    """
    Searches exams (with an approved notification) by name or
    description.
    """
    owns_session = db is None

    if owns_session:
        db = SessionLocal()

    try:
        search_term = f"%{query.strip()}%"

        statement = (
            select(Exam)
            .join(
                OfficialNotification,
                OfficialNotification.exam_id == Exam.exam_id,
            )
            .where(
                OfficialNotification.approval_status == "APPROVED",
                or_(
                    Exam.name.ilike(search_term),
                    Exam.description.ilike(search_term),
                ),
            )
            .options(selectinload(Exam.body))
            .distinct()
            .order_by(Exam.name.asc())
        )

        return list(db.scalars(statement).all())

    finally:
        if owns_session:
            db.close()


# ============================================================
# CATALOG: EVERY EXAM IN THE DATABASE
# ============================================================

_FILLER_WORDS = {"in", "of", "for", "and", "the", "a", "an", "to", "on"}


def acronym_tokens(name: str | None) -> set[str]:
    """
    Initial-letter abbreviations of an exam name, so a student can
    search "GATE" for "Graduate Aptitude Test in Engineering 2027".

    "Graduate Aptitude Test in Engineering" -> {"gat", "gate"}
    """

    words = [
        word
        for word in re.findall(r"[A-Za-z]+", name or "")
        if word.lower() not in _FILLER_WORDS
    ]

    initials = "".join(word[0].lower() for word in words)

    return {
        initials[:length]
        for length in range(3, 7)
        if len(initials) >= length
    }


def has_approved_notification(exam: Exam) -> bool:
    return any(
        notification.approval_status == "APPROVED"
        for notification in exam.official_notifications
    )


def _matches_query(exam: Exam, query: str) -> bool:
    query = query.casefold().strip()

    if not query:
        return True

    haystack = " ".join(
        part
        for part in (
            exam.name,
            exam.description,
            exam.type,
            exam.body.name if exam.body else None,
        )
        if part
    ).casefold()

    if query in haystack:
        return True

    tokens = re.findall(r"[a-z0-9]+", query)

    if not tokens:
        return False

    acronyms = acronym_tokens(exam.name)

    return all(
        token in haystack or token in acronyms
        for token in tokens
    )


def get_exam_catalog(
    query: str | None = None,
    db: Session | None = None,
):
    """
    Every exam in the database, including those whose notification is
    still waiting for administrator approval, optionally filtered by
    a search query (name, description, category, organization, or an
    abbreviation such as "GATE").

    Callers use has_approved_notification() to tell which exams have
    reviewed details.
    """
    owns_session = db is None

    if owns_session:
        db = SessionLocal()

    try:
        statement = (
            select(Exam)
            .options(
                selectinload(Exam.body),
                selectinload(Exam.official_notifications),
            )
            .order_by(Exam.name.asc())
        )

        exams = list(db.scalars(statement).all())

        if query and query.strip():
            exams = [
                exam
                for exam in exams
                if _matches_query(exam, query)
            ]

        return exams

    finally:
        if owns_session:
            db.close()