from flask_sqlalchemy import SQLAlchemy

Blog_db = SQLAlchemy()

# Blog Post Class
class BlogPost(Blog_db.Model):
    __tablename__ = "blog_posts"
    id = Blog_db.Column(Blog_db.Integer, primary_key=True)
    author = Blog_db.Column(Blog_db.String(250), nullable=False)
    title = Blog_db.Column(Blog_db.String(250), unique=True, nullable=False)
    subtitle = Blog_db.Column(Blog_db.String(250), nullable=False)
    date = Blog_db.Column(Blog_db.String(250), nullable=False)
    body = Blog_db.Column(Blog_db.Text, nullable=False)
    img_url = Blog_db.Column(Blog_db.String(250), nullable=False)