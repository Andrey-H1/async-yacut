import os


class Config(object):
    """Конфигурационные данные проекта."""

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY', default='SECRET_KEY')
    DISK_TOKEN = os.getenv('DISK_TOKEN')
