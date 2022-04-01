from unittest import TestCase

from app import app
from model import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_user_db'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all() 

class UserTestCase(TestCase):

    def setUp(self):
        User.query.delete()

    def tearDown(self):
        db.session.rollback()

    def test_user(self):
        user1  = User(first_name="Adam", 
                    last_name="Am", 
                    image_url="https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")
        self.assertEqual(user1.first_name, "Adam")
        self.assertEqual(user1.last_name, "Am")
        self.assertEqual(user1.image_url, "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")

class PostTestCase(TestCase):
    def setUp(self):
        Post.query.delete()

    def tearDown(self):
        db.session.rollback()
    
    def test_post(self):
        post = Post(title="First Post", content="This is my first post in a long time!", user_id=1)
        self.assertEqual(post.title, "First Post")
        self.assertEqual(post.content, "This is my first post in a long time!")
        self.assertEqual(post.user_id, 1)
        