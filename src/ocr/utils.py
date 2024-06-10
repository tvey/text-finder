import os
from types import SimpleNamespace

import pymupdf
import pytesseract
from docx import Document
from PIL import Image

from src.config import MAX_FILE_SIZE

TEXTS = SimpleNamespace(
    type_not_supported='Такой тип файла не поддерживается',
    no_file='Нужно выбрать файл',
    file_too_large=f'Файл может быть не больше {MAX_FILE_SIZE} МБ',
    processing_file='Файл обрабатывается, скоро придёт уведомление о завершении'
)
ALLOWED_EXT = ['pdf', 'png', 'jpg', 'jpeg']
IMAGE_EXT = ['png', 'jpg', 'jpeg']


def is_allowed(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


def ocr_image(image_path: str) -> str:
    image = Image.open(image_path)
    text = pytesseract.image_to_string(
        image,
        lang='eng+rus',
        config='--psm 6 --oem 3',
    )
    return text


def ocr_pdf(pdf_path: str) -> str:
    text = ''
    doc = pymupdf.open(pdf_path)

    for page in doc:
        text += page.get_textpage_ocr(language='rus').extractText() + '\n'

    return text


def get_text(file_path: str) -> str:
    """Get OCR text result."""
    text = ''
    ext = file_path.rsplit('.', 1)[1].lower()

    if ext in IMAGE_EXT:
        text = ocr_image(file_path)
    elif ext == 'pdf':
        text = ocr_pdf(file_path)

    return text


def text_to_docx(text: str, output_path: str) -> None:
    """Write text to docx."""
    doc = Document()
    doc.add_paragraph(text)
    doc.save(output_path)


def save_result(
    filename: str, text: str, upload_folder: str
) -> tuple[str, str]:
    """Save text to txt and docx files."""
    txt_path = os.path.join(upload_folder, f'{filename}.txt')
    docx_path = os.path.join(upload_folder, f'{filename}.docx')

    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(text)

    text_to_docx(text, docx_path)

    return txt_path, docx_path
