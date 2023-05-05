"""Forms for feedback app."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email

class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username", validators=[InputRequired()],)
    password = PasswordField("Password", validators=[InputRequired()],)
    email = StringField("Email address", validators=[InputRequired(), Email()],)
    f_name = StringField("First name", validators=[InputRequired()],)
    l_name = StringField("Last name", validators=[InputRequired()],)

class LoginForm(FlaskForm):
    """Form for logging in a user."""

    username = StringField("Username", validators=[InputRequired(), Length(min=6, max=20)],)
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=20)],)

class DeleteForm(FlaskForm):
    """Form for deleting a user."""

class FeedbackForm(FlaskForm):
    """Form for user feedback."""

    title = StringField("Title", validators=[InputRequired()])
    content = StringField("Content", validators=[InputRequired()])
    
