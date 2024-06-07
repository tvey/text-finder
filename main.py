from flask import Flask

from config import config


def create_app(env):
    app = Flask(__name__)
    app.config.from_object(config[env])

    from ocr.db import db

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from ocr.routes import bp

    app.register_blueprint(bp, url_prefix='/ocr/')
    
    return app


if __name__ == '__main__':
    app = create_app('dev')
    app.run()
