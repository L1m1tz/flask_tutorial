from functools import wraps
import gc
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, 
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@auth_blueprint.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        error = None

        if not firstname:
            error = 'First Name is required'
        elif not lastname:
            error = 'Last Name is required'
        elif not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required'
        elif not password:
            error = 'Password is required.'

        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'The username {} is already registered.'.format(username)

        elif db.execute(
            'SELECT id FROM user WHERE email = ?', (email,)
        ).fetchone() is not None:
            error = 'The email {} is already registered.'.format(email)

        if error is None:
            db.execute(
                'INSERT INTO user (firstname, lastname, username, email, password) VALUES (?, ?, ?, ?, ?)',
                (firstname, lastname, username, email,
                 generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)
    return render_template('auth/register.html')


@auth_blueprint.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'That email address could not be found on our system'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['id'] = user['id']
            g.user = user
            return redirect(url_for('main.home'))

        flash(error)

    return render_template('auth/login.html')

@auth_blueprint.before_app_request
def load_logged_in_user():
    id = session.get('id')

    if id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (id,)
        ).fetchone()


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('You need to be Logged in')
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view

@auth_blueprint.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('auth.login'))