from flask import Flask, render_template, redirect, request, url_for, flash
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from flask_login import login_user, login_required, current_user, logout_user
# My Files (Classes)
from classes.forms import CreatePostForm
from classes.blogPost import BlogPost
from classes.user_class import User, RegisterForm, LoginForm, db
# My Files (Functions)
from Functions.user_load_func import login_Manager, load_user

# Init Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db' # DB to store blog posts
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init the Flask App with SQL DB
db.init_app(app) # Blog DB

# Init the Flask App with Login Manager
login_Manager.init_app(app)

# Home Route
@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


# Register Route
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    # Validation for request method
    if request.method == "POST" and form.validate_on_submit():
        # Getting the hased and salted password
        hashed_Salted_Password = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=8)
        # Registering the new user
        new_user = User(
                name=form.name.data,
                email=form.email.data,
                password=hashed_Salted_Password, # Hashed and Salted Password Added in DB
            )
        # Validation for Email
        if User.query.filter_by(email=new_user.email).first() is None:
            # Commiting and Adding in DB
            db.session.add(new_user)
            db.session.commit()
            # Returning to main page in case of success
            return redirect(url_for("get_all_posts"))
        else:
            flash("This email is already registered", "error")
    return render_template("register.html", form=form, is_loggedIn=True)


# Login Route
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    # Validation for form
    if form.validate_on_submit() and request.method == "POST":
        # Getting the user details from the HTTP request
        email = form.email.data
        password = form.password.data
        # Getting the user from DB by email
        user = User.query.filter_by(email=email).first()
        # Validation for user
        if user:
            # Checking the password
            if check_password_hash(pwhash=user.password, password=password):
                login_user(user)
                return redirect(url_for("get_all_posts"))
            else:
                flash("Incorrect email or password.", "error")
        else:
            flash("The user with this email does not exist. Register first!", "error")
    return render_template("login.html", form=form, is_loggedIn=True)


# Logout Route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


# About Route
@app.route("/about")
def about():
    return render_template("about.html")


# Contact Route
@app.route("/contact")
def contact():
    return render_template("contact.html")


# Show Post Route
@app.route("/post/<int:post_id>")
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    return render_template("post.html", post=requested_post)


# New Post Route
@app.route("/new-post")
def add_new_post():
    form = CreatePostForm()
    # Validating the form
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        # Adding the post in DB
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


# Edit Post Route
@app.route("/edit-post/<int:post_id>")
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    # Displaying the info in form
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    # Validating the form
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        # Commiting in DB
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)


# Delete Post Route
@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    # Getting the targeted post form DB
    post_to_delete = BlogPost.query.get(post_id)
    # Deleting and commiting
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


# Executing as Script
if __name__ == "__main__":
    # Creating a database with app context
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=5000)
