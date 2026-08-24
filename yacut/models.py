from datetime import datetime, timezone

from yacut import db
from yacut.constants import ORIGINAL_URL_LENGTH, SHORT_URL_LENGTH


class URLMap(db.Model):
    """Модель ссылки."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_URL_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_URL_LENGTH), unique=True)
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=lambda: datetime.now(timezone.utc)
    )
