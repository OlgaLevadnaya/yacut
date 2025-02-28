from http import HTTPStatus
import re

from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id
from settings import constants


@app.route('/api/id/', methods=['POST'])
def get_short_link():
    try:
        data = request.get_json()
    except Exception:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    custom_id = data.get('custom_id', '')
    if custom_id:
        if URLMap.query.filter_by(short=custom_id).first() is not None:
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )
        if not re.match(constants.SHORT_PATTERN, custom_id):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
    else:
        data['custom_id'] = get_unique_short_id()
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return (
        jsonify(
            {
                'url': data['url'],
                'short_link': url_for(
                    'redirect_url', short_id=data['custom_id'], _external=True
                )
            }
        ),
        HTTPStatus.CREATED,
    )


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_redirect_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url:
        return jsonify({'url': url.original})
    raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
