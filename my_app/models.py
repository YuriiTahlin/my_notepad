from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Subtask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    is_complete = db.Column(db.Boolean)
    todo_id = db.Column(db.Integer, db.ForeignKey('to_do.id'), nullable=False)


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    is_complete = db.Column(db.Boolean)
    subtasks = db.relationship('Subtask', backref='todo', cascade='all, delete-orphan')
