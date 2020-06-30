from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.auth import login_required
from flaskr.db import get_db
from markupsafe import escape
from auth import login_required
from werkzeug.exceptions import abort

profile_blueprint = Blueprint('profile', __name__, url_prefix='/profile')

@profile_blueprint.route('/<int:id>')
def view(id):
    user = get_user(id, False)

    return render_template('profile/profile-view.html', user=user)

def get_user(id, check_author=True):
    user = get_db().execute(
        'SELECT id, firstname, lastname, username, email, password'
        ' FROM user'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if user is None:
        abort(404, "User id {0} doesn't exist.".format(id))

    if check_author and user['id'] != g.user['id']:
        abort(403)

    return user

@profile_blueprint.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    user = get_user(id)

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE user SET firstname = ?, lastname = ?, email = ?'
                ' WHERE id = ?',
                (firstname, lastname, email, id)
            )
            db.commit()
            return redirect(url_for('profile.view', id=id))

    return render_template('profile/profile-update.html', id=id, user=user)

@profile_blueprint.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_user(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('profile.view'))