from flask import render_template, Blueprint

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def root():
    return render_template('home.html')

@main_blueprint.route('/home')
def home():
    return render_template('home.html')

@main_blueprint.route('/about')
def about():
    return render_template('about.html')

@main_blueprint.route('/<page>')
def user(page):
    return render_template('404.html', url=page)


