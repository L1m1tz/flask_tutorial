from flask import render_template, Blueprint

profile_blueprint = Blueprint('profile', __name__, url_prefix='/profile')


@profile_blueprint.route('/update/<id>')
def update(id):
    return render_template('profile/profile-update.html')


@profile_blueprint.route('/<id>')
def view(id):
    return render_template('profile/profile-view.html')
