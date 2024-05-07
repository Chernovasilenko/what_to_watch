from flask import jsonify, render_template

from opinions_app import app, db


@app.errorhandler(404)
def page_not_found(error):
    """Обработка ошибки 404."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Обработка ошибки 500."""
    db.session.rollback()
    return render_template('500.html'), 500


class InvalidAPIUsage(Exception):
    """Класс обработки некорректных запросов."""

    status_code = 400

    def __init__(self, message, status_code=None):
        """Инициализация."""
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """Преобразование сообщения об ошибке в словарь."""
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    """Обработка некорректных запросов."""
    return jsonify(error.to_dict()), error.status_code
