"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# MODELS BELOW:
# All models should subclass db.Model
class User(db.Model):
    """ 
        Users Table

    """
    # Specify the tablename with __tablename__
    __tablename__ = 'users'
    
    #Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=True)
    img_url = db.Column(db.Text(), nullable=False, default='no_url_given')

    # relationships

    @classmethod
    def get_all_first_name(cls, name):
        return cls.query.filter_by(first_name=name).all()
    
    @classmethod
    def get_all_last_name(cls, name):
        return cls.query.filter_by(last_name=name).all()

    @classmethod
    def get_all_users(cls):
        return cls.query.all()

    def __repr__(self):
        u = self
        return f"<User id#={u.id} | first_name={u.first_name} | last_name={u.last_name} | img_url={u.img_url}>"
    
    def greet(self):
        return f"I'm {self.first_name} {self.last_name}"
    
class Post(db.Model):
    """
        Posts Table 

    """
    __tablename__ = 'posts'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # # Relationships
    # # .author_user for a post
    # # and .posts for a user
    author_user = db.relationship( 'User', backref=db.backref('posts', single_parent=True, cascade='all, delete-orphan'))

    # Relationship
    # posttag = db.relationship('PostTag', backref="posts")
    has_tags = db.relationship('Tag', secondary="posts_tags", backref="posts")

    def create_post(author, title, content):
        # Create a new Post object and set its attributes, have sqlalchemy server call its now() function for making datetime values
        new_post = Post(title=title, content=content, created_at=db.func.now())

        # Set the relationship with the author
        new_post.author_user = author

        return new_post
    
    def __repr__(self):
        p = self
        return f"<Post id#={p.id} | title={p.title} | created_at={p.created_at}>"
    
class Tag(db.Model):
    """
        Tags table
    """
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    
    # Relationship
    #a through relation
    has_posts = db.relationship('Post', secondary="posts_tags", backref="tags") #works to get array of posts that are tagged

    def __repr__(self):
        t = self
        return f"<Tag id#={t.id} | tag name={t.name}>"

class PostTag(db.Model):
    """ 
        Post Tags table
        two primary keys made into one. realation table from posts to tags
    """
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id  = db.Column(db.Integer,  db.ForeignKey('tags.id'), primary_key=True)
    
    def __repr__(self):
        pt = self
        return f"<PostTag | post_id={pt.post_id} | tag_id={pt.tag_id} |>"
    

# # ipython manual testing

# In [2]: pam = User.query.get(1)
# 2023-07-25 11:47:02,958 INFO sqlalchemy.engine.base.Engine BEGIN (implicit) 2023-07-25 11:47:02,959 INFO sqlalchemy.engine.base.Engine SELECT users.id AS users_id, users.first_name AS users_first_name, users.last_name AS users_last_name, users.img_url AS users_img_url FROM users WHERE users.id = %(param_1)s 2023-07-25 11:47:02,959 INFO sqlalchemy.engine.base.Engine {'param_1': 1}

# In [3]: pams_post = pam.posts[0]
# 2023-07-25 11:47:20,159 INFO sqlalchemy.engine.base.Engine SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.created_at AS posts_created_at, posts.user_id AS posts_user_id FROM posts WHERE %(param_1)s = posts.user_id 2023-07-25 11:47:20,159 INFO sqlalchemy.engine.base.Engine {'param_1': 1}

# In [4]: hot = pams_post.has_tags[0]
# 2023-07-25 11:47:36,374 INFO sqlalchemy.engine.base.Engine SELECT tags.id AS tags_id, tags.name AS tags_name FROM tags, posts_tags WHERE %(param_1)s = posts_tags.post_id AND tags.id = posts_tags.tag_id 2023-07-25 11:47:36,375 INFO sqlalchemy.engine.base.Engine {'param_1': 1}

# In [5]: hot.has_posts
# 2023-07-25 11:48:01,502 INFO sqlalchemy.engine.base.Engine SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.created_at AS posts_created_at, posts.user_id AS posts_user_id FROM posts, posts_tags WHERE %(param_1)s = posts_tags.tag_id AND posts.id = posts_tags.post_id 2023-07-25 11:48:01,502 INFO sqlalchemy.engine.base.Engine {'param_1': 1}
# Out[5]: [<Post id#=1 | title=HELLOOOOO | created_at=2023-07-24 18:36:50.213201>]