from flask import jsonify
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column('userId', db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    todos = db.relationship('Todo', backref='agent')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "User <{} - {}>".format(self.id, self.username)


class Todo(db.Model):
    userId = db.Column('userId', db.Integer, db.ForeignKey(User.id))
    todoId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    due_date = db.Column(db.Date, nullable=False)

    def getJson(self):
        return {
            'title': self.title,
            'category': self.category,
            'description': self.description,
            'due_date': self.due_date
        }

    def __repr__(self):
        return {
            'title': self.title,
            'category': self.category,
            'description': self.description,
            'due_date': self.due_date
        }
