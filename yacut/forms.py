from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from settings import constants


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, constants.MAX_ORIGINAL_LENGTH),
            URL(message='Введите ссылку')
        ],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(
                1,
                constants.MAX_SHORT_LENGTH,
                message=f'Не более {constants.MAX_SHORT_LENGTH} символов',
            ),
            Regexp(
                constants.SHORT_PATTERN,
                message='Разрешены только латинские буквы и цифры',
            ),
        ],
    )
    submit = SubmitField('Создать')
