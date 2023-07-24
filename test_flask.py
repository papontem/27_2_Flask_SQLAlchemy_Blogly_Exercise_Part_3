from unittest import TestCase

from app import app
from models import db, User, Post
import json, sys, traceback

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample test User and sample test post."""
        db.drop_all()
        db.create_all()

        #making sure user and post tables are empty!!
        User.query.delete()
        Post.query.delete()

        test_user = User(first_name="TestUser",last_name="Tasty",img_url="")

        db.session.add(test_user)
        db.session.commit()

        test_post_data = {"title":"TestPostTitle", "content":"Test Post Content"}
        test_post = Post.create_post(test_user,test_post_data["title"],test_post_data["content"])

        db.session.add(test_post)
        db.session.commit()

        self.user_id = test_user.id
        self.user = test_user

        self.post_id = test_post.id
        self.post = test_post

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_home_redirect(self):
        with app.test_client() as client:
            try:
                # Pythons Native Debugger here to help ^_^ !! 
                # import pdb
                # pdb.set_trace()

                resp = client.get("/", follow_redirects=False)
                # html = resp.get_data(as_text=True)

            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error in testing that were being redirected to /users from / ")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 302)
                self.assertEqual(resp.location, 'http://localhost/users')

    def test_home_redirect_followed(self): 
        with app.test_client() as client:
            try:
                resp = client.get("/", follow_redirects=True)
                html = resp.get_data(as_text=True)
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error where we were testing that the redirection from /users to / was sucesfull or not")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 200)
                self.assertIn('TestUser', html)

    def test_list_Users(self):
        with app.test_client() as client:
            try:
                resp = client.get("/users")
                html = resp.get_data(as_text=True)

            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error in getting the users.html page from /users")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 200)
                self.assertIn('TestUser', html)

    def test_details_User(self): 
        with app.test_client() as client:
            try:
                resp = client.get(f"/users/{self.user_id}")
                html = resp.get_data(as_text=True)
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error in trying to show a specific user following /users/self.user_id")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 200)
                self.assertIn('TestUser', html)
                self.assertIn("User Profile <br> Img Url Value <br> will be chosen later?", html)
            
    def test_add_User_redirect(self): 
        with app.test_client() as client:
            try:
                d = {
                        "first_name":"TestUser2",
                        "last_name":"Tasty2",
                        "img_url":""
                     }
                resp = client.post("/users/new", data=d, follow_redirects=False)
                # html = resp.get_data(as_text=True)
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error in testing if were being redirected when adding a new user")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 302)
                self.assertEqual(resp.location, 'http://localhost/users')

    def test_add_User_redirect_followed(self):
        with app.test_client() as client:
            try:
                d = {
                        "first_name": "TestUser2",
                        "last_name":'Tasty2',
                        "img_url":""
                     }
                resp = client.post("/users/new", data=d, follow_redirects=True)
                html = resp.get_data(as_text=True)
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error in testing that we were redirected succesfully after adding a new user")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 200)
                self.assertIn("TestUser2", html)

    def test_delete_user(self):
        with app.test_client() as client:
            try:
                # whoops i had used a $ from js syntax when getting user_id
                resp = client.post(f"/users/{self.user_id}/delete",follow_redirects=True)
                html = resp.get_data(as_text=True)
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error in trying to delete a user")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertNotIn("TestUser",html)
    
    def test_show_user_edit_page(self):
        with app.test_client() as client:
            try:
                resp = client.get(f"/users/{self.user_id}/edit")
                html = resp.get_data(as_text=True)

            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error where we were testing that user was shown the edit page for their profile")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 200)
                self.assertIn('TestUser', html)

    def test_edit_the_user_redirect(self):
        with app.test_client() as client:
            try:
                d = {
                        "first_name": "TestUser1111",
                        "last_name":'Tasty1111',
                        "img_url":""
                     }
                resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=False)
                html = resp.get_data(as_text=True)

            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error where we were testing that user is being redirected after sending a post request to edit a user")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 302)
                self.assertEqual(resp.location, 'http://localhost/users')

    def test_edit_the_user_redirect_followed(self):
        with app.test_client() as client:
            try:
                d = {
                        "first_name": "TestUser1111",
                        "last_name":'Tasty1111',
                        "img_url":""
                     }
                resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
                html = resp.get_data(as_text=True)
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error where we were testing that user was sucessfuly redirected after editing a user")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 200)
                self.assertIn("TestUser1111", html)

class PostViewsTestCase(TestCase):
    """Tests for views for Posts."""

    def setUp(self):
        """Add sample test User and sample test post."""
        db.drop_all()
        db.create_all()

        #making sure user and post tables are empty!!
        User.query.delete()
        Post.query.delete()

        test_user = User(first_name="TestUser",last_name="Tasty",img_url="")

        db.session.add(test_user)
        db.session.commit()

        test_post_data = {"title":"TestPostTitle", "content":"Test Post Content"}
        test_post = Post.create_post(test_user,test_post_data["title"],test_post_data["content"])

        db.session.add(test_post)
        db.session.commit()

        self.user_id = test_user.id
        self.user = test_user

        self.post_id = test_post.id
        self.post = test_post

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_posts(self):
        with app.test_client() as client:
            try:
                resp = client.get("/posts")
                html = resp.get_data(as_text=True)
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error where we were testing that user was correctly sent the list of posts")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 200)
                self.assertIn("<h2>Posts</h2>", html)
                self.assertIn("TestPostTitle", html)

    def test_details_post(self):
        with app.test_client() as client:
            try:
                resp = client.get(f"/posts/{self.post_id}")
                html = resp.get_data(as_text=True)
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error where we tested if user couldsee the page holding the details of a post")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 200)
                self.assertIn("<h2>TestPostTitle</h2>", html)
                self.assertIn("TestUser", html)
                self.assertIn("Tasty", html)
                self.assertIn("<button> &lt; Cancel &lt; </button>", html)
                self.assertIn("<button>Edit</button>", html)
                self.assertIn("<button>X Delete X</button>", html)

    def test_show_edit_post_form(self):
        with app.test_client() as client:
            try:
                resp = client.get(f"/posts/{self.post_id}/edit")
                html = resp.get_data(as_text=True)
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error where we test if user is seeing the page where they can edit their post")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 200)
                self.assertIn("<h1>Edit A Post</h1>", html)
                
                self.assertIn("Title:", html)
                self.assertIn(f"{self.post.title}", html)

                self.assertIn("Content:", html)
                self.assertIn(f"{self.post.content}", html)

                self.assertIn("<button> &lt; Cancel &lt; </button>", html)
                self.assertIn("<button>Save</button>", html)

    def test_show_edit_post_form_redirect(self):
        with app.test_client() as client:
            try:
                d = {
                    "title": "test post title changed",
                    "content": self.post.content + 'changed'
                }
                resp = client.post(f"/posts/{self.post_id}/edit", data=d, follow_redirects=False)
                html = resp.get_data(as_text=True)
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error where we submit a edit post request and see if user is being redirected to the right location")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 302)
                self.assertEqual(resp.location, f"http://localhost/posts/{self.post.id}")

    def test_show_edit_post_form_redirect_followed(self):
        with app.test_client() as client:
            try:
                d = {
                    "title": "test post title changed",
                    "content": self.post.content + ' changed!'
                }
                resp = client.post(f"/posts/{self.post_id}/edit", data=d, follow_redirects=True)
                html = resp.get_data(as_text=True)
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error where we submit a edit post request and see if user is succesfully landing on the redirected location")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 200)
                self.assertIn("<h2>test post title changed</h2>", html)
                self.assertIn(d["content"], html)
                self.assertIn("TestUser", html)
                self.assertIn("Tasty", html)
                self.assertIn("<button> &lt; Cancel &lt; </button>", html)
                self.assertIn("<button>Edit</button>", html)
                self.assertIn("<button>X Delete X</button>", html)

    def test_new_post_form(self):
        with app.test_client() as client:
            try:
                resp = client.get(f"/users/{self.user_id}/posts/new")
                html = resp.get_data(as_text=True)
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error where we test if the user is being presented the new post form correctly")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 200)
                self.assertIn(f"<h2>Add New Post for {self.user.first_name} {self.user.last_name}</h2>", html)
                self.assertIn("<button> &lt; Cancel &lt; </button>", html)
    
    def test_new_post_form_redirect(self):
        with app.test_client() as client:
            try:
                d = {
                        "title":"New Test Post Title",
                        "content":"Content of New Test Post"
                     }
                resp = client.post(f"/users/{self.user_id}/posts/new",data=d, follow_redirects=False)
                html = resp.get_data(as_text=True)
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error where we test if the user is being redirected to the correct location after submitting the add new post form")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 302)
                self.assertEqual(resp.location, f"http://localhost/users/{self.user_id}")
    
    def test_new_post_form_redirect_followed(self):
        with app.test_client() as client:
            try:
                d = {
                        "title":"New Test Post Title",
                        "content":"Content of New Test Post"
                     }
                resp = client.post(f"/users/{self.user_id}/posts/new",data=d, follow_redirects=True)
                html = resp.get_data(as_text=True)
            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error where we test if the user is being redirected to the correct location after submitting the add new post form")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 200)
                self.assertIn(d["title"],html)
                self.assertIn(f"<h2>{self.user.first_name} {self.user.last_name}</h2>",html)
                self.assertIn("<button>Add Post</button>",html)

    def test_delete_post_redirect(self):
        with app.test_client() as client:
            try:
                resp = client.post(f"/posts/{self.post_id}/delete", follow_redirects=False)
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 302)
                self.assertEqual(resp.location, f"http://localhost/users/{self.user_id}")

            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error where we test if user is correctly redirected to the correct location after pressing the delete button on a post")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                

    def test_delete_post_redirect_followed(self):
        
        with app.test_client() as client:
            try:
                # Pythons Native Debugger here to help ^_^ !! 
                # import pdb
                # pdb.set_trace()

                #self.user object instance was becoming dettached from the session after post was deleted.
                # print(self.user)

                resp = client.post(f"/posts/{self.post_id}/delete", follow_redirects=True)
                html = resp.get_data(as_text=True)

                # reputting the user object instance back into the test session
                self.user = User.query.get(self.user_id)
                # print(self.user)

            except Exception as e:
                print("\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
                print("Exception Error where we test if user is correctly landing back at the users detail page after delete route is followed ")
                print("An exception occurred:")
                print("Type:", type(e).__name__)
                print("Value:", str(e))
                print("Traceback:", traceback.format_exc())
                print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            else:
                self.assertEqual(resp.status_code, 200)
                self.assertIn(f"<h2>{self.user.first_name} {self.user.last_name}</h2>",html)
                self.assertIn("<button>Add Post</button>",html)
