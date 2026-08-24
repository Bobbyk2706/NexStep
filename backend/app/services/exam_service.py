from app.database.session import SessionLocal
from app.models.conducting_body import ConductingBody
from app.models.exam import Exam


def create_exam(
    body_name,
    main_website,
    body_description,
    logo_url,
    exam_name,
    exam_type,
    exam_description,
    official_exam_page,
    status
):
    with SessionLocal() as s:

        body = ConductingBody(
            name=body_name,
            main_website=main_website,
            description=body_description,
            logo_url=logo_url
        )

        exam = Exam(
            name=exam_name,
            type=exam_type,
            description=exam_description,
            off_exam_page=official_exam_page,
            status=status
        )

        body.exams.append(exam)

        s.add(body)
        s.commit()

        return exam.exam_id