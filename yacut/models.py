from datetime import datetime, timezone

from . import db
from settings import constants


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(constants.MAX_ORIGINAL_LENGTH), nullable=False)
    short = db.Column(
        db.String(constants.MAX_SHORT_LENGTH), unique=True, nullable=False
    )
    timestamp = db.Column(
        db.DateTime, index=True,
        default=datetime.now(timezone.utc)
    )

    def to_dict(self):
        return dict(
            original=self.original,
            short=self.short,
        )

    def from_dict(self, data):
        self.original = data['url']
        self.short = data['custom_id']
