from flask import jsonify, request

from opinions_app import app, db
from opinions_app.error_handlers import InvalidAPIUsage
from opinions_app.models import Opinion
from opinions_app.views import random_opinion


@app.route('/api/get-random-opinion/', methods=['GET'])
def get_random_opinion():
    """Получение случайного мнения о фильме."""
    opinion = random_opinion()
    if opinion:
        return jsonify({'opinion': opinion.to_dict()}), 200
    raise InvalidAPIUsage('В базе данных нет мнений', 404)


@app.route('/api/opinions/<int:id>/', methods=['GET'])
def get_opinion(id):
    """Получение мнения о фильме по id."""
    opinion = Opinion.query.get(id)
    if opinion is None:
        # Тут код ответа нужно указать явным образом
        raise InvalidAPIUsage('Мнение с указанным id не найдено', 404)
    return jsonify({'opinion': opinion.to_dict()}), 200


@app.route('/api/opinions/<int:id>/', methods=['PATCH'])
def update_opinion(id):
    """Обновление мнения о фильме по id."""
    data = request.get_json()
    if (
        'text' in data and
        Opinion.query.filter_by(text=data['text']).first() is not None
    ):
        raise InvalidAPIUsage('Такое мнение уже существует')
    opinion = Opinion.query.get(id)
    if Opinion.query.get(id) is None:
        raise InvalidAPIUsage('Мнение с указанным id не найдено', 404)
    opinion.title = data.get('title', opinion.title)
    opinion.text = data.get('text', opinion.text)
    opinion.source = data.get('source', opinion.source)
    opinion.added_by = data.get('added_by', opinion.added_by)
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 201


@app.route('/api/opinions/<int:id>/', methods=['DELETE'])
def delete_opinion(id):
    """Удаление мнения о фильме по id."""
    opinion = Opinion.query.get(id)
    if opinion is None:
        raise InvalidAPIUsage('Мнение с указанным id не найдено', 404)
    db.session.delete(opinion)
    db.session.commit()
    return '', 204


@app.route('/api/opinions/', methods=['GET'])
def get_opinions():
    """Получение списка мнений о фильмах."""
    opinions = Opinion.query.all()
    opinions_list = [opinion.to_dict() for opinion in opinions]
    return jsonify({'opinions': opinions_list}), 200


@app.route('/api/opinions/', methods=['POST'])
def add_opinion():
    """Добавление мнения о фильме."""
    data = request.get_json()
    if 'title' not in data:
        raise InvalidAPIUsage('Отсутствует поле title')
    if 'text' not in data:
        raise InvalidAPIUsage('Отсутствует поле text')
    if Opinion.query.filter_by(text=data['text']).first() is not None:
        raise InvalidAPIUsage('Такое мнение уже существует')
    opinion = Opinion()
    opinion.from_dict(data)
    db.session.add(opinion)
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 201
