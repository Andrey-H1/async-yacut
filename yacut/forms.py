from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from yacut.constants import (
    AUTO_ALLOWED_CHARS, MIN_LENGTH,
    ORIGINAL_URL_LENGTH, SHORT_URL_LENGTH
)


class URLMapForm(FlaskForm):
    """Форма для модели URLMap."""

    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле!'),
            Length(MIN_LENGTH, ORIGINAL_URL_LENGTH)
        ],
    )

    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(MIN_LENGTH, SHORT_URL_LENGTH),
            Optional(),
            Regexp(
                f'^[{AUTO_ALLOWED_CHARS}]+$',
                message='Указано недопустимое имя для короткой ссылки'
            )
        ]
    )

    submit = SubmitField('Создать')


class UploadForm(FlaskForm):
    """Форма для загрузки файлов на сайт."""

    files = MultipleFileField(
        validators=[DataRequired(message='Обязательное поле!')]
    )

    submit = SubmitField('Загрузить')
