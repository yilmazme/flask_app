from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    opA = db.Column(db.String(1000))
    opB = db.Column(db.String(1000))
    opC = db.Column(db.String(1000))
    opD = db.Column(db.String(1000))
    correctOp = db.Column(db.String(3))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("members.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    def __init__(self, data, opA, opB, opC, opD, correctOp, user_id, category_id):
        self.data = data
        self.opA = opA
        self.opB = opB
        self.opC = opC
        self.opD = opD
        self.correctOp = correctOp
        self.user_id = user_id
        self.category_id = category_id
        

class User(db.Model, UserMixin):
    __tablename__ = "members"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    notes = db.relationship("Note")

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name
     
class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    categoryName = db.Column(db.String(150))
    notes = db.relationship("Note")

    def __init__(self, categoryName):
        self.categoryName = categoryName