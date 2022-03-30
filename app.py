from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from model import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def show_users():
    """show list of all users in db"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('base.html', users = users)

@app.route('/', methods=["POST"])
def create_user():
    """create new user"""

    fname = request.form['fname']
    lname = request.form['lname']
    image = request.form['image'] 

    new_user = User(first_name=fname, last_name=lname, image_url=image or None)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/')

@app.route('/<int:user_id>')
def show_user(user_id):
    """show user details"""

    user = User.query.get_or_404(user_id)

    return render_template('details.html', user=user, user_id=user_id)

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

    return redirect('/')

@app.route('/<int:user_id>/delete', methods =["POST"])
def delete_user(user_id):
    """handle form submission for deleting existing user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')
    