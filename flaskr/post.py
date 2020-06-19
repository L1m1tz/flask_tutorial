from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.auth import login_required
from flaskr.db import get_db
from markupsafe import escape
from auth import login_required
from werkzeug.exceptions import abort

post_blueprint = Blueprint('post', __name__, url_prefix='/post')

@post_blueprint.route('/')
def list():
    db = get_db()
    posts = db.execute(
        'SELECT post.id, author_id, created, title, username'
        ' FROM post JOIN user ON post.author_id = user.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('post/post-list.html', posts=posts)


@post_blueprint.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@post_blueprint.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (author_id, title, body)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('post.list'))
    return render_template('post/post-create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT post.id, title, body, created, author_id, username'
        ' FROM post JOIN user ON post.author_id = user.id'
        ' WHERE post.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@post_blueprint.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('post.list'))

    return render_template('post/update.html', post=post)

@post_blueprint.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('post.list'))