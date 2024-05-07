from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from opinions_app import app, db
from opinions_app.forms import OpinionForm
from opinions_app.models import Opinion


@app.route('/')
def index_view():
    """Главная страница."""
    opinion = random_opinion()
    if opinion:
        return render_template('opinion.html', opinion=opinion)
    abort(404)


@app.route('/add', methods=['GET', 'POST'])
def add_opinion_view():
    """Форма добавления мнения."""
    form = OpinionForm()
    if form.validate_on_submit():
        text = form.text.data
        if Opinion.query.filter_by(text=text).first():
            flash('Такое мнение уже было оставлено ранее!')
            return render_template('add_opinion.html', form=form)
        opinion = Opinion(
            title=form.title.data,
            text=form.text.data,
            source=form.source.data
        )
        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for('opinion_view', id=opinion.id))
    return render_template('add_opinion.html', form=form)


@app.route('/opinions/<int:id>')
def opinion_view(id):
    """Мнение о конкретном фильме."""
    opinion = Opinion.query.get_or_404(id)
    return render_template('opinion.html', opinion=opinion)


def random_opinion():
    """Получение случайного мнения о фильме."""
    quantity = Opinion.query.count()
    if quantity:
        offset_value = randrange(quantity)
        opinion = Opinion.query.offset(offset_value).first()
        return opinion
