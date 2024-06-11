from environs import Env

env = Env()
env.read_env()

MAX_FILE_SIZE = 20  # mb


class Config:
    SECRET_KEY = env.str('SECRET_KEY', default='verysecret')
    SQLALCHEMY_DATABASE_URI = env.str('DATABASE_URL')
    UPLOAD_FOLDER = env.str('UPLOAD_FOLDER', '/app/uploads')
    MAX_CONTENT_LENGTH = MAX_FILE_SIZE * 1000 * 1000
    FLASK_DEBUG = env.bool('FLASK_DEBUG')
    CELERY_BROKER_URL = env.str('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND')
    SERVER_NAME = env.str('SERVER_NAME', '0.0.0.0:5000')
    APPLICATION_ROOT = '/'
    PREFERRED_URL_SCHEME = 'http'


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True


class ProdConfig(Config):
    FLASK_ENV = 'production'


config = {
    'dev': DevConfig,
    'prod': ProdConfig,
}
