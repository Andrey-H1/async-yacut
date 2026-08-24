from flask import jsonify, request

from yacut import app, db
from yacut.utils import create_url_map, get_unique_short_id
from yacut.validators import (
    get_url_map_or_404, validate_custom_id,
    validate_request_payload, validate_unique_short_id
)


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    """Функция получения оригинальной ссылки по короткому идентификатору."""
    url_map = get_url_map_or_404(short_id)
    return jsonify({'url': url_map.original}), 200


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    """Функция создания короткой ссылки."""
    data = request.get_json(silent=True)

    validate_request_payload(data)

    original_link = data['url']

    if 'custom_id' in data:
        custom_id = data['custom_id']

        validate_custom_id(custom_id)
        validate_unique_short_id(custom_id)

        short_id = custom_id

    else:
        short_id = get_unique_short_id()

    short_url_result = create_url_map(original_link, short_id)

    db.session.commit()

    return jsonify({'url': original_link, 'short_link': short_url_result}), 201
