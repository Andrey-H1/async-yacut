from flask import jsonify, request
from http import HTTPStatus

from yacut.constants import SHORT_URL_LENGTH
from yacut.error_handlers import InvalidAPIUsage
from yacut import app, db
from yacut.models import URLMap
from yacut.utils import create_url_map, get_unique_short_id
from yacut.validators import get_url_map_by_short_id


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    """Функция получения оригинальной ссылки по короткому идентификатору."""
    if get_url_map_by_short_id(short_id) is None:
        raise InvalidAPIUsage(
            'Указанный id не найден',
            status_code=HTTPStatus.NOT_FOUND
        )
    return (
        jsonify({'url': get_url_map_by_short_id(short_id).original}),
        HTTPStatus.OK
    )


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    """Функция создания короткой ссылки."""
    data = request.get_json(silent=True)

    if data is None:
        raise InvalidAPIUsage(
            'Отсутствует тело запроса'
        )

    if 'url' not in data:
        raise InvalidAPIUsage(
            '"url" является обязательным полем!'
        )

    original_link = data['url']
    short_id = None

    if 'custom_id' in data and data['custom_id']:
        custom_id = data['custom_id']

        if (len(custom_id) > SHORT_URL_LENGTH):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )

        if not URLMap.validate_short_id(custom_id):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )

        if get_url_map_by_short_id(custom_id) is not None:
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )

        short_id = custom_id

    else:
        short_id = get_unique_short_id()

    short_url_result = create_url_map(original_link, short_id)

    db.session.commit()

    return (
        jsonify({'url': original_link, 'short_link': short_url_result}),
        HTTPStatus.CREATED
    )
