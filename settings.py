import os
from string import ascii_letters, digits


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')


class Constants:
    __slots__ = ()
    ALLOWED_CHARACTERS = ascii_letters + digits
    AUTO_SHORT_ID_LENGTH = 6
    MAX_ORIGINAL_LENGTH = 256
    MAX_SHORT_LENGTH = 16
    SHORT_PATTERN = r'^[a-zA-Z0-9]{1,16}$'


constants = Constants()