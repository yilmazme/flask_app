from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify

from flask_login import  login_required, current_user

from .models import Category, Note, NoteSchema, User
from . import db
import json
#to split up end points

views = Blueprint("views", __name__)


# profile page for one user, can add, see and delete all their notes
@views.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    categories = db.session.query(Category)
    notes = db.session.query(Note)
    if request.method == "POST":
        note = request.form.get("note")
        opA = request.form.get("opA")
        opB = request.form.get("opB")
        opC = request.form.get("opC")
        opD = request.form.get("opD")
        correctOp = request.form.get("correctOp")
        categoryId = request.form.get("categoryId")
      

        if len(note)<1:
            flash("soru biraz kısa olmadı mı:(", category="error")
        else:
            new_note = Note(data=note,opA=opA, opB=opB, opC=opC, opD=opD, correctOp=correctOp, user_id= current_user.id, category_id=categoryId)
            db.session.add(new_note)
            db.session.commit()
            flash("soru eklendi! ", category="success")
    return render_template("profile.html", user=current_user, categories=categories, notes_len=len(current_user.notes))

#here user can add new category
@views.route("/add", methods=["GET", "POST"])
@login_required
def add_category():
    if request.method == "POST":
        category = request.form.get("category")

        if len(category)<1:
            flash("kategori biraz kısa olmadı mı:(", category="error")
        else:
            new_ca = Category(categoryName=category)
            db.session.add(new_ca)
            db.session.commit()
            flash("Kategori eklendi! ", category="success")
    return render_template("addca.html", user=current_user)

#here a user can see all notes from all users
@views.route("/home", defaults={'id': None})
@views.route("/home/<int:id>")
@login_required
def home(id):
    filtered_note = Note.query.filter(Note.category_id == id).first()
    #notes = db.session.query(Note)
    categories = db.session.query(Category)
    return render_template("home.html", categories=categories, user=current_user, filtered_note=filtered_note)

# api call for a category
# here we i use marshmallow for json serilization
#not used at front end for now
@views.route("/get-set", methods=["POST"])
def get_set():
    body= json.loads(request.data)
    id = body["id"]
    filtered_notes = Note.query.filter(Note.category_id == id).all()
    notes_schema = NoteSchema(many=True) 
    output =  notes_schema.dump(filtered_notes)
    return jsonify({"res":output})


# get choosen op and respond


@views.route("/make-choice", methods=["POST"])
def get_choice():
    answer_obj = json.loads(request.data)
    question_id = answer_obj["questionId"]
    choosen_op = answer_obj["choosenOp"]
    question = Note.query.filter(Note.id == question_id).first()
    if question:
        if question.correctOp==choosen_op:
            return json.dumps({"res":True})
        else:
            return json.dumps({"res":False, "answer":question.correctOp})
    return json.dumps({"res":"no quest find"})
    
# this is the end point for a user delete their notes(request sending by javascript from frontend)
@views.route("/delete-note", methods=["POST"])
def delete_note():
    note= json.loads(request.data)
    id = note["id"]
    note = Note.query.get(id)
    if note:
        if note.user_id==current_user.id:
            db.session.delete(note)
            db.session.commit()
    return json.dumps({})

# deleting account
@views.route("/delete-account", methods=["POST"])
def delete_account():
    body= json.loads(request.data)
    id = body["id"]
    user = User.query.get(id)
    if user:
        if user.id==current_user.id:
            db.session.delete(user)
            db.session.commit()
            flash("Hesap Silindi! ", category="success")
    return json.dumps({})