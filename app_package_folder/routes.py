from flask import Blueprint
from flask import render_template, request, abort, render_template_string, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from app_package_folder import db
from app_package_folder.models import Users
import sqlalchemy

users = Blueprint('users', __name__)

@users.route("/")
def home():
    if 'users' in sqlalchemy.inspect(db.engine).get_table_names():
        print('db already exists')
    else:
        db.create_all()
        print('db created')
    return "Home Page"

@users.route('/messages/<idx>')
@login_required
def message(idx):
    idx=int(idx)
    messages = ['Message Zero', 'Message One', 'Message Two']
    # return render_template_string("<h1> Messages: {{ messages }}</h1>", messages=messages[idx])
    try:
        return render_template_string("<h1> Messages: {{ messages }}</h1>", messages=messages[idx])
    except IndexError:
        abort(500)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    if request.method == 'POST':
        formDict = request.form.to_dict()
        print('formDict:::',formDict)
        user = Users(email=formDict.get('email'),password=formDict.get('password'))
        db.session.add(user)
        db.session.commit()
    return render_template('register.html')

@users.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    if request.method == 'POST':
        formDict = request.form.to_dict()
        # user = Users(email=formDict.get('email'),password=formDict.get('password'))
        user = Users.query.filter_by(email=formDict.get('email')).first()
        if user:
            print(user)
            print('user.id:::',user.id)
            login_user(user)
            return redirect(url_for('users.message',idx=1))
    return render_template('login.html')


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.home'))