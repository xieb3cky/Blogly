from unittest import TestCase

from app import app
from model import db, User,Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_user_db'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']



class UserModelTestcase(TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()

        user1  = User(first_name="Adam", 
                    last_name="Am", 
                    image_url="https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")
        db.session.add(user1)
        db.session.commit()

        post1 = Post(title="First Post", content="This is my first post in a long time!", user_id=1)
        db.session.add(post1)
        db.session.commit()
        
    def tearDown(self):
        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<li><a href="/1"> Adam Am </a></li>', html)
            self.assertIn('<h4>Add new user!</h4>', html)
    def test_add_user_form(self):
        with app.test_client() as client:
            res = client.post('/',data={'fname':'Becky','lname':'Be','image':'www.google.com'},follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<li><a href="/2"> Becky Be </a></li>', html) 
    def test_user_details(self):
        with app.test_client() as client:
            res = client.get('/1')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn(' <h2>Name: Adam Am</h2>', html) 
    def test_show_post_form(self):
        with app.test_client() as client:
            res = client.get('/1/posts/new')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Add Post for Adam Am</h1>', html) 
            self.assertIn('<form action="/1/posts/new"', html) 
    def test_post_form(self):
        with app.test_client() as client:
            res = client.post('/1/posts/new',data={'title':'new post','content':'new post for user'}, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<a href="/1/posts/2">new post</a>', html) 



        