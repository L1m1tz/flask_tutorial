from flask import render_template, Blueprint
from auth import login_required
    

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
#@login_required
def root():
    return render_template('home.html')

@main_blueprint.route('/home')
@login_required
def home():
    return render_template('home.html')

@main_blueprint.route('/about')
def about():
    return render_template('about.html')

@main_blueprint.route('/<page>')
@login_required
def user(page):
    return render_template('404.html', url=page)


