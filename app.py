from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, LoginManager, logout_user, login_required

import random

app = Flask(__name__)
app.config.from_object(Config)  # loads the configuration for the database
db = SQLAlchemy(app)  # creates the db object using the configuration
login = LoginManager(app)
login.login_view = 'login'
from models import insults, todo, Contact, User
from forms import ContactForm, RegistrationForm, LoginForm, ResetPasswordForm

@app.route('/')
def homepage():  # put application's code here
    return render_template("index.html", title="Ngunnawal Country", user=current_user)


@app.route('/todo', methods=["POST", "GET"])
def view_todo():
    all_todo = db.session.query(todo).all()
    if request.method == "POST":
        new_todo = todo(text=request.form['text'])
        new_todo.done = False
        db.session.add(new_todo)
        db.session.commit()
        db.session.refresh(new_todo)
    return render_template("todo.html", todos=all_todo, user=current_user)


@app.route("/todoedit/<todo_id>", methods=["POST", "GET"])
def edit_note(todo_id):
    if request.method == "POST":
        db.session.query(todo).filter_by(id=todo_id).update({
            "text": request.form['text'],
            "done": True if request.form['done'] == "on" else False
        })
        db.session.commit()
    elif request.method == "GET":
        db.session.query(todo).filter_by(id=todo_id).delete()
        db.session.commit()
    return redirect("/todo", code=302)


@app.route("/contact.html", methods=["POST", "GET"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        new_contact = Contact(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(new_contact)
        db.session.commit()

    return render_template("contact.html", title="Contact Us", form=form, current_user)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(email_address=form.email_address.data, name=form.name.data,
                        user_level=1)  # defaults to regular user
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("homepage"))
    return render_template("registration.html", title="User Registration", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for("homepage"))
    return render_template("login.html", title="Sign In", form=form, user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/reset_password', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=current_user.email_address).first()
        user.set_password(form.new_password.data)
        db.session.commit()
        flash("Your password has been changed")
        return redirect(url_for('homepage'))
    return render_template("passwordreset.html", title='Reset Password', form=form, user=current_user)


# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", user=current_user), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html", user=current_user), 500


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	return render_template("userProfile.html", title="User Profile", user=current_user)

if form.validate_on_submit():
	user = User.query.filter_by(email_address=current_user.email_address).first()
	user.update_details(email_address=form.email_address.data, name=form.name.data)
	db.session.commit()
	flash("Your details have been changed")
	return redirect(url_for("homepage"))