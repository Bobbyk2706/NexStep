
from app.models.base import Base
from sqlalchemy.orm import Mapped,mapped_column, relationship

class ConductingBody(Base):
    __tablename__='conducting_body'
    body_id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column()
    main_website:Mapped[str]=mapped_column()
    description:Mapped[str| None]=mapped_column()
    logo_url:Mapped[str| None]=mapped_column()
    exams:Mapped[list['Exam']]=relationship(
        back_populates='body'
    )