from datetime import datetime

from opinions_app import db


class Opinion(db.Model):
    """Модель мнения о фильме."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    added_by = db.Column(db.String(64))

    def to_dict(self) -> dict:
        """Преобразование объекта модели в словарь."""
        return dict(
            id=self.id,
            title=self.title,
            text=self.text,
            source=self.source,
            timestamp=self.timestamp,
            added_by=self.added_by
        )

    def from_dict(self, data: dict):
        """Преобразование словаря в объект модели."""
        for field in ('title', 'text', 'source', 'added_by'):
            if field in data:
                setattr(self, field, data[field])
