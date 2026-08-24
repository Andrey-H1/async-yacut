from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from yacut.constants import MIN_LENGTH, ORIGINAL_URL_LENGTH, SHORT_URL_LENGTH


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
            Optional()
        ]
    )

    submit = SubmitField('Создать')


class UploadForm(FlaskForm):
    """Форма для загрузки файлов на сайт."""

    files = MultipleFileField(
        validators=[DataRequired(message='Обязательное поле!')]
    )

    submit = SubmitField('Загрузить')
