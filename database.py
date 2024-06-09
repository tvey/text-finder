from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class OcrResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), nullable=False)
    txt_path = db.Column(db.String(256), nullable=False)
    docx_path = db.Column(db.String(256), nullable=False)
    original_filename = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'OcrResult({self.filename})'
