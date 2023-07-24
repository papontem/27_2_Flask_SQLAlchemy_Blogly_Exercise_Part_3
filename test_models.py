from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for User."""

    def setUp(self):
        """Add sample test User and sample test post."""
        db.drop_all()
        db.create_all()

        #making sure user and post tables are empty!!
        User.query.delete()
        Post.query.delete()

        test_user = User(first_name="TestUser",last_name="Tattertot",img_url="")
        test_user_2 = User(first_name="TestUser2",last_name="FrenchFry",img_url="") 
        
        db.session.add_all([test_user,test_user_2])
        db.session.commit()

        
        self.user_id = test_user.id
        self.user = test_user
        
        self.user_2_id = test_user_2
        self.user_2 = test_user_2

        # test_post_data = {"title":"TestPostTitle", "content":"Test Post Content"}
        # test_post_2_data = {"title":"TestPostTitle version 2", "content":"Test Post Content version 2"}
        # test_post = Post.create_post(test_user,test_post_data["title"],test_post_data["content"])
        # test_post_2 = Post.create_post(test_user_2,test_post_2_data["title"],test_post_2_data["content"])
        
        # db.session.add_all([test_post,test_post_2])
        # db.session.commit()

        # self.post_id = test_post.id
        # self.post = test_post

        # self.post_2_id = test_post_2.id
        # self.post_2 = test_post_2

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_greet(self):
        
        self.assertEqual(self.user.greet(), "I'm TestUser Tattertot")
        self.assertEqual(self.user_2.greet(), "I'm TestUser2 FrenchFry")


    def test_get_all_first_name(self): 

        query_result1 = User.get_all_first_name('TestUser')
        query_result2 = User.get_all_first_name('TestUser2')

        
        self.assertEqual(query_result1,[self.user])
        self.assertEqual(query_result2,[self.user_2])
    
    
    def test_get_all_last_name(self):

        query_result1 = User.get_all_last_name('Tattertot')
        query_result2 = User.get_all_last_name('FrenchFry')

        
        self.assertEqual(query_result1,[self.user])
        self.assertEqual(query_result2,[self.user_2])

    
    def test_get_all_Users(self):

        query_result = User.get_all_users()

        # ADD THE ASSERT
        self.assertEqual(query_result,[self.user, self.user_2])
    
class PostModelTestCase(TestCase):
    """Tests for model for Posts."""

    def setUp(self):
        """Add sample test User and sample test post."""
        db.drop_all()
        db.create_all()

        #making sure user and post tables are empty!!
        User.query.delete()
        Post.query.delete()

        test_user = User(first_name="TestUser",last_name="Tattertot",img_url="")
        test_user_2 = User(first_name="TestUser2",last_name="FrenchFry",img_url="") 
        
        db.session.add_all([test_user,test_user_2])
        db.session.commit()

        
        self.user_id = test_user.id
        self.user = test_user
        
        self.user_2_id = test_user_2
        self.user_2 = test_user_2

        self.test_post_data = {"title":"TestPostTitle", "content":"Test Post Content"}
        self.test_post_2_data = {"title":"TestPostTitle version 2", "content":"Test Post Content version 2"}

        # test_post = Post.create_post(test_user,test_post_data["title"],test_post_data["content"])
        # test_post_2 = Post.create_post(test_user_2,test_post_2_data["title"],test_post_2_data["content"])
        
        # db.session.add_all([test_post,test_post_2])
        # db.session.commit()

        # self.post_id = test_post.id
        # self.post = test_post

        # self.post_2_id = test_post_2.id
        # self.post_2 = test_post_2

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_create_post(self):

        test_post   = Post.create_post(  self.user,   self.test_post_data["title"],   self.test_post_data["content"])
        test_post_2 = Post.create_post(self.user_2, self.test_post_2_data["title"], self.test_post_2_data["content"])

        self.assertEqual(test_post, Post.query.filter_by(title=test_post.title).first())
        self.assertEqual(test_post_2, Post.query.filter_by(title=test_post_2.title).first())
