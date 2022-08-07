from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)

app.config.from_object(Config)  # loads the configuration for the database
db = SQLAlchemy(app)  # creates the db object using the configuration

from models import Contact
from forms import ContactForm

from models import insults, todo

@app.route('/')
def homepage():  # put application's code here
    return render_template("index.html", title="Ngunnawal Country")


@app.route("/contact.html", methods=["POST", "GET"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        new_contact = Contact(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(new_contact)
        db.session.commit()

    return render_template("contact.html", title="Contact Us", form=form)


@app.route('/todo', methods=["POST", "GET"])
def view_todo():
    all_todo = db.session.query(todo).all()
    if request.method == "POST":
        new_todo = todo(text=request.form['text'])
        new_todo.done = False
        db.session.add(new_todo)
        db.session.commit()
        db.session.refresh(new_todo)
    return render_template("todo.html", todos=all_todo)


