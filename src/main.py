from flask import Flask

from celery_worker import make_celery

from src.config import config


def create_app(env: str = 'dev'):
    app = Flask(__name__)
    app.config.from_object(config[env])

    from database import db

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from ocr.routes import bp

    app.register_blueprint(bp, url_prefix='')

    celery = make_celery()
    app.celery = celery

    return app


if __name__ == '__main__':
    app = create_app('dev')
    app.run(host='0.0.0.0')