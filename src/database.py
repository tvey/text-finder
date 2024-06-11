import datetime
from typing import Annotated

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class OcrResult(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str]
    file_path: Mapped[str]
    txt_path: Mapped[str]
    docx_path: Mapped[str]
    original_filename: Mapped[str | None]
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __repr__(self):
        return f'OcrResult({self.filename})'


def save_ocr_result(data: dict):  # meh
    ocr_result = OcrResult(**data)
    db.session.add(ocr_result)
    db.session.commit()
