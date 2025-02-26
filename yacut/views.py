from http import HTTPStatus
from flask import abort, flash, redirect, render_template, url_for


from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .utils import (
    get_unique_short_id,
    check_short_id,
)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short = form.custom_id.data
    if short:
        if not check_short_id(short):
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
    else:
        short = get_unique_short_id()

    url_map = URLMap(
        original=form.original_link.data,
        short=short
    )
    db.session.add(url_map)
    db.session.commit()

    flash('Ваша новая ссылка готова:')
    return render_template(
        'index.html',
        form=form,
        link_text=url_for(
            'redirect_url',
            short_id=short,
            _external=True
        )
    )


@app.route('/<string:short_id>', methods=['GET'])
def redirect_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url:
        return redirect(url.original, code=HTTPStatus.FOUND.value)
    abort(404)
