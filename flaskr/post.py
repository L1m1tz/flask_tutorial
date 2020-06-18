from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from markupsafe import escape
from db import get_db
from auth import login_required

post_blueprint = Blueprint('post',__name__,url_prefix='/post')



@post_blueprint.route('/')
def list():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, author_id, created, title, u.id, username'
        'FROM post p JOIN user u ON p.author_id = u.id'
        'ORDER BY created DESC'
    ).fetchall()
    return render_template('post-list.html', posts=posts)


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

    return render_template('blog/create.html')
    return render_template('post/post-create.html')
