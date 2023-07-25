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
    # assignments = db.relationship('EmployeeProject', backref='employee')


    # hash_tags = db.relationship('Tag', secondary="posts_tags", backref="posts")
    # projects = db.relationship('Project', secondary="employees_projects", backref="employees")

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
    # tagged_posts = db.relationship('PostTag', backref="tags")

class PostTag(db.Model):
    """ 
        Post Tags table
        two primary keys made into one. realation table from posts to tags
    """
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey(
        'tags.id'), primary_key=True)
    
