import random

from .models import URLMap
from settings import constants


def generate_short_id(short_id_length):
    return ''.join(
        [random.choice(constants.ALLOWED_CHARACTERS)
         for i in range(short_id_length)]
    )


def check_short_id(short_id):
    '''Возвращает True если ссылка уникальна'''
    if not short_id:
        return False
    return not URLMap.query.filter_by(short=short_id).first()


def get_unique_short_id(short_id=None):
    while not check_short_id(short_id):
        short_id = generate_short_id(constants.AUTO_SHORT_ID_LENGTH)
    return short_id
