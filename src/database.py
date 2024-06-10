import datetime
from typing import Annotated

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# User


class OcrResult(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str]
    file_path: Mapped[str]
    txt_path: Mapped[str]
    docx_path: Mapped[str]
    original_filename: Mapped[str | None]
    created_at = Annotated[
        datetime.datetime,
        mapped_column(server_default=text("TIMEZONE('utc', now())")),
    ]

    def __repr__(self):
        return f'OcrResult({self.filename})'


def save_ocr_result(data: dict):  # meh
    pass
