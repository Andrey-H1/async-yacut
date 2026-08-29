from datetime import datetime
import re

from yacut import db
from yacut.constants import (
    AUTO_ALLOWED_CHARS, ORIGINAL_URL_LENGTH,
    SHORT_URL_LENGTH
)


class URLMap(db.Model):
    """Модель ссылки."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_URL_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_URL_LENGTH), unique=True)
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=datetime.now
    )

    @staticmethod
    def validate_short_id(custom_id):
        """Проверяет на наличие запрещенных символов."""
        if not re.fullmatch(f'[{AUTO_ALLOWED_CHARS}]+', custom_id):
            return False
        return True
