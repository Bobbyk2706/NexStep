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
    Returns all exams with their conducting body.

    The function accepts an optional Session so callers such as
    FastAPI routes and tests can control the transaction/session.
    """
    owns_session = db is None

    if owns_session:
        db = SessionLocal()

    try:
        statement = (
            select(Exam)
            .options(selectinload(Exam.body))
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
    Searches exams by exam name or description.
    """
    owns_session = db is None

    if owns_session:
        db = SessionLocal()

    try:
        search_term = f"%{query.strip()}%"

        statement = (
            select(Exam)
            .options(selectinload(Exam.body))
            .where(
                or_(
                    Exam.name.ilike(search_term),
                    Exam.description.ilike(search_term),
                )
            )
            .order_by(Exam.name.asc())
        )

        return list(db.scalars(statement).all())

    finally:
        if owns_session:
            db.close()