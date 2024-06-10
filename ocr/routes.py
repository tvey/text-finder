import logging
import os
import uuid

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)

from database import OcrResult, db
from ocr.utils import (
    get_text,
    is_allowed,
    save_result,
    TEXTS as txt,
    ALLOWED_EXT,
)

bp = Blueprint(
    'ocr',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@bp.route('/', methods=['GET', 'POST'])
def index():
    upload_folder = current_app.config['UPLOAD_FOLDER']

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash(txt.no_file, 'info')
            return redirect(request.url)

        if file and is_allowed(file.filename):
            original_filename = file.filename
            file_extension = original_filename.rsplit('.', 1)[1].lower()
            uuid_filename = uuid.uuid4().hex
            new_filename = f'{uuid_filename}.{file_extension}'
            upload_path = os.path.join(upload_folder, new_filename)
            file.save(upload_path)

            if file_extension in ALLOWED_EXT:
                text = get_text(upload_path)
            else:
                flash(txt.type_not_supported, 'info')
                return redirect(request.url)

            txt_path, docx_path = save_result(
                uuid_filename, text, upload_folder
            )
            ocr_result = OcrResult(
                filename=new_filename,
                txt_path=txt_path,
                docx_path=docx_path,
                original_filename=original_filename,
            )
            db.session.add(ocr_result)
            db.session.commit()

            return render_template(
                'index.html', txt_file=txt_path, docx_file=docx_path
            )

        flash(txt.type_not_supported, 'info')
        return redirect(request.url)

    return render_template('index.html')


@bp.route('/download/', methods=['GET'])
def download_file():
    file_path = request.args.get('file')
    if not file_path or not os.path.exists(file_path):
        flash('File not found')
        return redirect(url_for('ocr.index'))

    return send_file(file_path, as_attachment=True)


@bp.errorhandler(413)
def handle_large_file(error):
    current_app.logger.info(f'Large file error: {error}')
    flash(txt.file_too_large, 'info')
    return redirect(request.url)
