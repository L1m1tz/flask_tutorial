from flask import render_template, Blueprint

post_blueprint = Blueprint('post',__name__,url_prefix='/post')

@post_blueprint.route('/create')
def create():
    return render_template('post/post-create.html')

@post_blueprint.route('/')
def list():
    return render_template('post/post-list.html')

@post_blueprint.route('/<postid>')
def view(postid):
    # resolve post data
    # fetch post from database using postid
    return render_template('post/post-view.html', post=post )



