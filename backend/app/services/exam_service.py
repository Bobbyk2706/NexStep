from app.database.session import SessionLocal
from app.models.conducting_body import ConductingBody
from app.models.exam import Exam
from sqlalchemy import select


def create_exam(
    body_id,
    exam_name,
    exam_type,
    exam_description,
    official_exam_page,
    status
):
    with SessionLocal() as s:

        body=s.scalar(select(ConductingBody).where (ConductingBody.body_id==body_id))

        
        exam=Exam(
            name=exam_name,
            type=exam_type,
            description=exam_description,
            off_exam_page=official_exam_page,
            status=status
        )
        body.exams.append(exam)
        s.add(exam)
        s.commit()

        return exam.exam_id