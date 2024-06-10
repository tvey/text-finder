import os

from celery import shared_task
from flask import current_app

from src.database import db, OcrResult
from src.ocr.utils import get_text, save_result, ALLOWED_EXT, TEXTS as txt


@shared_task(name='celery_tasks.process_file')
def process_file(upload_path, uuid_filename, original_filename, upload_folder):
    with current_app.app_context():
        try:
            if upload_path.rsplit('.', 1)[1].lower() in ALLOWED_EXT:
                text = get_text(upload_path)
            else:
                return txt.type_not_supported

            txt_path, docx_path = save_result(uuid_filename, text, upload_folder)
            ocr_result_data = {
                'filename': os.path.basename(upload_path),
                'file_path': upload_path,
                'txt_path': txt_path,
                'docx_path': docx_path,
                'original_filename': original_filename,
            }
            ocr_result = OcrResult(**ocr_result_data)
            db.session.add(ocr_result)
            db.session.commit()

            return {'txt_path': txt_path, 'docx_path': docx_path}
        except Exception as e:
            return {'error': str(e)}
