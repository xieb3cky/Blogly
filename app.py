from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from model import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

#user route

@app.route('/')
def show_users():
    """show list of all users in db"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('home.html', users = users)

@app.route('/', methods=["POST"])
def create_user():
    """create new user"""

    fname = request.form['fname']
    lname = request.form['lname']
    image = request.form['image'] 

    new_user = User(first_name=fname, last_name=lname, image_url=image or None)
    db.session.add(new_user)
    db.session.commit()
    flash(f'{new_user.first_name} {new_user.last_name} was added!')
    return redirect('/')

@app.route('/<int:user_id>')
def show_user(user_id):
    """show user details"""

    user = User.query.get_or_404(user_id)
    user_posts = Post.query.filter_by(user_id=user_id).all()

    return render_template('details.html', user=user, user_id=user_id, user_posts=user_posts)

@app.route('/<int:user_id>/edit')
def edit_user(user_id):
    """show edit user form"""

    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/<int:user_id>/edit', methods =["POST"])
def update_user(user_id):
    """handle form submission for updating existing user"""

    user = User.query.get_or_404(user_id)

    user.first_name = request.form['fname']
    user.last_name = request.form['lname']
    user.image_url = request.form['image']

    db.session.add(user)
    db.session.commit()

    return redirect(f'/{user_id}')

@app.route('/<int:user_id>/delete', methods =["POST"])
def delete_user(user_id):
    """handle form submission for deleting existing user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')

#post route 

@app.route('/<int:user_id>/posts/new')
def show_post_form(user_id):
    """show create new post form"""
    user = User.query.get_or_404(user_id)
    return render_template('post.html', user=user)

@app.route('/<int:user_id>/posts/new', methods =["POST"])
def new_post(user_id):
    """handle form submission for creating new post"""
    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user_id=user.id)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/{user_id}')

@app.route('/<int:user_id>/posts/<int:post_id>')
def show_posts(user_id, post_id):
    """show specific user's all posts"""

    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(user_id)
    return render_template('post-show.html', post=post, user=user)

@app.route('/<int:user_id>/posts/<int:post_id>/edit')
def show_edit_form(user_id,post_id):
    """show edit post form"""
    post = Post.query.get_or_404(post_id)
    return render_template('edit-post.html', user_id=user_id ,post=post)

@app.route('/<int:user_id>/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(user_id,post_id):
    """handle form submission for updating a post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/{post.user_id}")

@app.route('/<int:user_id>/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(user_id,post_id):
    """delete post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/{user_id}')
    
