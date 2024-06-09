from environs import Env

env = Env()
env.read_env()


class Config:
    SECRET_KEY = env.str('SECRET_KEY', default='verysecret')
    SQLALCHEMY_DATABASE_URI = env.str('DATABASE_URL')
    UPLOAD_FOLDER = env.str('UPLOAD_FOLDER')


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False


config = {
    'dev': DevConfig,
    'prod': ProdConfig,
}
