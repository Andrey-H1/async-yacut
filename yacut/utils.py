from flask import request
import random

from yacut import db
from yacut.constants import AUTO_ALLOWED_CHARS, AUTO_URL_LENGTH
from yacut.models import URLMap


def get_unique_short_id():
    """Функция формирования короткого идентификатора ссылки."""
    while True:
        short_link = ''.join(
            random.choice(AUTO_ALLOWED_CHARS) for _ in range(AUTO_URL_LENGTH)
        )
        if not URLMap.query.filter_by(short=short_link).first():
            return short_link


def create_url_map(original_link, short_id):
    """Функция создания объекта базы данных."""
    url_map = URLMap(
        original=original_link,
        short=short_id
    )
    db.session.add(url_map)
    return request.host_url + short_id
