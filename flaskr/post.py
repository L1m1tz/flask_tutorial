from flask import render_template, Blueprint 
from markupsafe import escape

post_blueprint = Blueprint('post',__name__,url_prefix='/post')

@post_blueprint.route('/create')
def create():
    return render_template('post/post-create.html')

@post_blueprint.route('/')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall(); 
   return render_template("list.html",rows = rows)


@post_blueprint.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id



