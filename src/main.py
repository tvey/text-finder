from flask import Flask
from src.config import config
from src.database import db
from src.celery_worker import make_celery


def create_app(env: str = 'dev'):
    app = Flask(__name__)
    app.config.from_object(config[env])

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from src.ocr.routes import bp

    app.register_blueprint(bp, url_prefix='')

    make_celery(app)

    return app


if __name__ == '__main__':
    app = create_app('dev')
    app.run(host='0.0.0.0')
