from flask import Blueprint, render_template, request, flash, redirect
from flask.ext.login import (current_user, login_required)

import models

notes_app = Blueprint("notes_app", __name__, template_folder="templates")


@notes_app.route("/")
def index():
    templateData = {
        'notes': models.Note.objects.order_by("-last_updated")
    }
    return render_template('index.html', **templateData)


@notes_app.route("/notes/create", methods=["GET", "POST"])
@login_required
def admin_entry_create():

    if request.method == "POST":
        note = models.Note()
        note.title = request.form.get("title", "")
        note.content = request.form.get("content")

        # associate note to currently logged in user
        note.user = current_user.get_mongo_doc()
        note.save()

        return redirect("/notes/%s" % note.id)

    else:
        template_data = {
            "title": "Create new note",
            "note": None
        }
        return render_template("/note_edit.html", **template_data)


@notes_app.route("/notes/<note_id>/edit", methods=["GET", "POST"])
@login_required
def admin_entry_edit(note_id):
    # get single document returned
    note = models.Note.objects().with_id(note_id)

    if note:
        if note.user.id != current_user.id:
            return "Sorry you do not have permission to edit this note"

        if request.method == "POST":
            note.title = request.form.get("title", "")
            note.content = request.form.get("content")

            note.save()

            flash("Note has been updated")

        template_data = {"title": "Edit note", "note": note}

        return render_template("/note_edit.html", **template_data)

    else:
        return "Unable to find entry %s" % note_id


@notes_app.route("/notes/<note_id>")
def entry_page(note_id):

    # get class notes entry with matching slug
    note = models.Note.objects().with_id(note_id)

    if note:
        templateData = {"note": note}

        return render_template("note_display.html", **templateData)

    else:
        return "not found"
