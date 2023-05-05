"""Flask app for Feedback"""
from flask import Flask, render_template, jsonify, request, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Feedback, User
from forms import RegisterForm, LoginForm, DeleteForm, FeedbackForm
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'hey'
app.debug = True

toolbar = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    """Display home page."""

    return redirect("/register")

@app.route("/register", methods=['GET', 'POST'])
def register():

    if "username" in session:
        redirect(f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        f_name = form.f_name.data
        l_name = form.l_name.data

        new_user = User.register(username, password, email, f_name, l_name)

        db.session.commit()

        session['username'] = new_user.username

        return redirect(f"/users/{new_user.username}")
    
    else:
        return render_template('users/register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit(): 
        username = form.username.data
        password = form.password.data

        user = User.auth(username, password)

        if user:
            return redirect(f"/users/{user.username}")
        else: 
            return render_template("users/login.html", form=form)
        
    return render_template("users/login.html", form=form)

@app.route("/logout")
def logout(username):

    session.pop("username")

    flash("You are now logged out")

    return redirect("/login")

@app.route("/users/<username>")
def display_user(username):

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()

    return render_template("users/display.html", user=user, form=form)


@app.route("/users/<username>/delete")
def delete(username):

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    session.delete(user)
    session.commit()

    session.pop("username")

    flash("Account deleted")

    return redirect("/login")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add(username):

    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    form = FeedbackForm()

    if form.validate_on_submit():

        title= form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    else:
        return render_template("feedback/new.html", form=form)
    

@app.route("/feedback/<feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")


    return render_template("feedback/edit.html", form=form, feedback=feedback)

@app.route("/feedback/<feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")
