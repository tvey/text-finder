from celery import Celery
from src.config import Config


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND'],
        include=['src.celery_tasks'],
    )
    celery.conf.update(app.config)
    app.celery = celery

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


from src.main import create_app

flask_app = create_app()
celery = make_celery(flask_app)
