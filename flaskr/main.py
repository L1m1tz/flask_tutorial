from flask import render_template, Blueprint

main_blueprint = Blueprint('main', __name__,)

@main_blueprint.route('/')
def home():
    return render_template('home.html')

@main_blueprint.route('/post')
def list_posts():
    return render_template('post-list.html')

@main_blueprint.route('/home')
def about():
    return render_template('home.html')

@main_blueprint.route('/<page>')
def user(page):
    return render_template('404.html', url=page)
