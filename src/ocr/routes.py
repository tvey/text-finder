import json
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

from .utils import is_allowed, TEXTS as txt

bp = Blueprint(
    'ocr',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@bp.route('/status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = current_app.celery.AsyncResult(task_id)
    if task.state == 'SUCCESS':
        result = task.result
        print(result)
    else:
        result = None

    response = {'state': task.state, 'result': result}
    return json.dumps(response)


@bp.route('/', methods=['GET', 'POST'])
def index():
    upload_folder = current_app.config['UPLOAD_FOLDER']

    if request.method == 'POST':
        if 'file' not in request.files:
            flash(txt.no_file, 'info')
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

            task = current_app.celery.send_task(
                'celery_tasks.process_file',
                args=[
                    upload_path,
                    uuid_filename,
                    original_filename,
                    upload_folder,
                ],
            )
            flash(txt.processing_file, 'info')
            return render_template('index.html', task_id=task.id)

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
