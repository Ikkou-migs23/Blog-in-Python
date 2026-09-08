from flask import Blueprint, render_template, request, redirect, url_for, flash
from flaskr.db import get_db

bp = Blueprint('blog', __name__)
@bp.route('/')
def index():
    db = get_db()
    # 1. Recupera as postagens do banco trazendo as informações do autor
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
        ).fetchall()
    # 2. Renderiza o template enviando a lista de posts recuperada
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        body = request.form.get('body', '').strip()
        error = None

        if not title:
            error = 'O título do post é obrigatório.'
        elif not body:
            error = 'O conteúdo do post é obrigatório.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, 1)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')