"""Models for Feedback app."""
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    db.app = app 
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key = True, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    f_name = db.Column(db.String(30), nullable = False)
    l_name = db.Column(db.String(30), nullable = False)

    feedback = db.relationship('Feedback', backref='user', cascade='all')

    @classmethod
    def register(cls, username, password, email, f_name, l_name):
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(username=username, password=hashed_utf8, email=email, f_name=f_name, l_name=l_name)

        db.session.add(user)
        return user

    @classmethod
    def auth(cls, username, password):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else: 
            return False


class Feedback(db.Model):
    """Feedback model."""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    username = db.Column(db.Text, db.ForeignKey('users.username'), nullable=False)

