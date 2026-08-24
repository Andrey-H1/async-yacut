from flask import flash

from yacut.constants import AUTO_ALLOWED_CHARS, SHORT_URL_LENGTH
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap


def get_url_map_or_404(short_id):
    """Проверка налияия идентификатора короткого кода в базе данных."""
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage(
            'Указанный id не найден', 404
        )

    return url_map


def validate_request_payload(data):
    """Проверяет, что запрос не пустой и содержит обязательное поле 'url'."""
    if data is None:
        raise InvalidAPIUsage(
            'Отсутствует тело запроса'
        )

    if 'url' not in data:
        raise InvalidAPIUsage(
            '"url" является обязательным полем!'
        )


def validate_custom_id(custom_id):
    """Проверка допустимости имени короткой ссылки."""
    is_too_long = len(custom_id) > SHORT_URL_LENGTH
    invalid_chars = any(char not in AUTO_ALLOWED_CHARS for char in custom_id)
    if is_too_long or invalid_chars:
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки'
        )


def validate_unique_short_id(short_id):
    """Проверка уникальности имени короткой ссылки."""
    if URLMap.query.filter_by(short=short_id).first():
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )


def is_custom_id_valid(custom_id):
    """Проверка идентификатора короткой ссылки для web-формы."""
    if not custom_id:
        return True

    if any(char not in AUTO_ALLOWED_CHARS for char in custom_id):
        flash(
            'Недопустимые символы в названии короткой ссылки.', 'danger'
        )
        return False

    if URLMap.query.filter_by(short=custom_id).first() or custom_id == 'files':
        flash(
            'Предложенный вариант короткой ссылки уже существует.', 'danger'
        )
        return False

    return True
