from flask import flash

from yacut.models import URLMap


def get_url_map_by_short_id(short_id):
    """Получние идентификатора короткого кода из базы данных."""
    return URLMap.query.filter_by(short=short_id).first()


def is_custom_id_valid(custom_id):
    """Проверка идентификатора короткой ссылки для web-формы."""
    custom_id = custom_id or ''

    if not custom_id:
        return True

    if not URLMap.validate_short_id(custom_id):
        flash(
            'Недопустимые символы в названии короткой ссылки.', 'danger'
        )
        return False

    if get_url_map_by_short_id(custom_id) or custom_id == 'files':
        flash(
            'Предложенный вариант короткой ссылки уже существует.', 'danger'
        )
        return False

    return True
