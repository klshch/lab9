#!/usr/bin/python3

from flask import flash, redirect, render_template, url_for, make_response, request, session
from flask_login import login_user, current_user, logout_user, login_required

from app import app, db
from app.models import Feedback, Todo, User
from app.saver import save_picture

import os
from datetime import datetime

from data import skills
import json

from forms import LoginForm
from forms import ChangePassword
from forms import FeedbackForm
from forms import TodoForm
from forms import RegistrationForm
from forms import LoginForms
from forms import UpdateAccountForm

def get_system_info():
    os_info = os.uname()
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return os_info, user_agent, current_time

json_file_path = os.path.join(os.path.dirname(__file__), 'static', 'json', 'users.json')
with open(json_file_path, 'r') as users_file:
    users = json.load(users_file)


@app.route('/')
def home():
    os_info, user_agent, current_time = get_system_info()
    return render_template('home.html', os_info=os_info, user_agent=user_agent, current_time=current_time)

@app.route('/page1')
def page1():
    os_info, user_agent, current_time = get_system_info()
    return render_template('page1.html', os_info=os_info, user_agent=user_agent, current_time=current_time)

@app.route('/page2')
def page2():
    os_info, user_agent, current_time = get_system_info()
    return render_template('page2.html', os_info=os_info, user_agent=user_agent, current_time=current_time)

@app.route('/page3')
@app.route('/page3/<int:idx>')
def page3(idx=None):
    os_info, user_agent, current_time = get_system_info()
    if idx is not None:
        if 0 <= idx < len(skills):
            skill = skills[idx]
            return render_template('page3.html', skill=skill, os_info=os_info, user_agent=user_agent, current_time=current_time)
        else:
            total_skills = len(skills)
            return render_template('page3.html', skills=skills, total_skills=total_skills, os_info=os_info, user_agent=user_agent, current_time=current_time)
    else:
        total_skills = len(skills)
        return render_template('page3.html', skills=skills, total_skills=total_skills, os_info=os_info, user_agent=user_agent, current_time=current_time)


#lab5

@app.route('/form', methods=["GET", "POST"])
def form():
    
    form = LoginForm()  

    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data

        if name in users and users[name] == password:
            if form.remember.data == True:
                flash("Вхід виконано. Інформація збережена.", category="success")
                session["username"] = name

                return redirect(url_for("info"))
                
            else:
                flash("Вхід виконано. Інформація не збережена", category="success")

                return redirect(url_for("home"))

        else:
            flash("Вхід не виконано", category="warning")
            return redirect(url_for("form"))

    return render_template('form.html', form=form)



@app.route('/info', methods=["GET", "POST"])
def info():

    form = ChangePassword()

    if session.get("username"):
        cookies = get_cookies_data()
        if request.method == "POST":
 
            cookie_key = request.form.get("cookie_key")
            cookie_value = request.form.get("cookie_value")
            cookie_expiry = request.form.get("cookie_expiry")
            delete_cookie_key = request.form.get("delete_cookie_key")

            if cookie_key and cookie_value and cookie_expiry:
                add_cookie(cookie_key, cookie_value, int(cookie_expiry))
            if delete_cookie_key:
                delete_cookie(delete_cookie_key)

            cookies = get_cookies_data()  
        return render_template('info.html', cookies=cookies, form=form)
    else:
        return redirect(url_for('form'))


def get_cookies_data():
    cookies = []
    for key, value in request.cookies.items():
        expiry = request.cookies.get(key + "_expires")
        created = request.cookies.get(key + "_created")

        cookies.append((key, value, expiry, created))
    return cookies

@app.route('/clearsession', methods=["GET"])
def clear_session():
    session.pop("username", None)
    return redirect(url_for("form"))

@app.route('/add_cookie', methods=["POST"])
def add_cookie():
    if session.get("username"):
        cookie_key = request.form.get("cookie_key")
        cookie_value = request.form.get("cookie_value")
        cookie_expiry = request.form.get("cookie_expiry")

        response = make_response(redirect(url_for("info")))
        response.set_cookie(cookie_key, cookie_value, max_age=int(cookie_expiry) * 3600) 
        flash("Куки додано.", category="success")
        return response
    else:
        return redirect(url_for('form'))

@app.route('/delete_cookie', methods=["POST"])
def delete_cookie():
    if session.get("username"):
        cookie_key_to_delete = request.form.get("cookie_key_to_delete")
        response = make_response(redirect(url_for("info")))
        response.delete_cookie(cookie_key_to_delete)
        flash("Куки видалено.", category="success")
        return response
    else:
        return redirect(url_for('form'))

@app.route('/delete_all_cookies', methods=["POST"])
def delete_all_cookies():
    if session.get("username"):
        response = make_response(redirect(url_for("info")))
        for key in request.cookies:
            response.delete_cookie(key)
        flash("Куки видалено.", category="success")
        return response
    else:
        flash("Куки не видалено.", category="warning")
        return redirect(url_for('form'))


@app.route('/change_password', methods=["POST"])
def change_password():

    form = ChangePassword()

    if form.validate_on_submit():

        if session.get("username"):
            current_password = form.current_password.data
            new_password = form.new_password.data
            username = session["username"]

            json_file_path = os.path.join(os.path.dirname(__file__), 'static', 'json', 'users.json')

            with open(json_file_path, 'r') as users_file:
                users = json.load(users_file)

            if users.get(username) == current_password:
                users[username] = new_password

                with open(json_file_path, 'w') as users_file:
                    json.dump(users, users_file)

                flash("Пароль змінено.", category="success")
                
                return redirect(url_for("info"))
            
            else:
                flash("Пароль не змінено.", category="warning")

                return redirect(url_for("info"))
        
        else:
            return redirect(url_for('form'))
        
    return render_template('info.html', form=form)


#самостійна робота

@app.route('/reviews', methods=["GET", "POST"])
def reviews():
    
    reviews = FeedbackForm()

    if request.method == 'POST' and reviews.validate_on_submit():
        name = reviews.name.data
        content = reviews.content.data
        feedback_entry = Feedback(name=name, content=content)
        db.session.add(feedback_entry)
        db.session.commit()
        flash('Ваш відгук було успішно збережено', 'success')
        return redirect(url_for('reviews'))

    feedback_entries = Feedback.query.all() 

    return render_template('reviews.html', reviews=reviews, feedback_entries=feedback_entries)

#lab6

@app.route('/todo', methods=['GET', 'POST'])
def todo():

    form = TodoForm()

    todo_list = Todo.query.all()

    return render_template("todo.html", form=form, todo_list=todo_list)


@app.route('/add', methods=["POST"])
def add():

    form = TodoForm()

    if form.validate_on_submit():
        title = form.title.data
        new_todo = Todo(title=title, complete=False)
        db.session.add(new_todo)
        db.session.commit()

        flash('Додано.', 'success')
    else:
        flash('Не додано.', 'danger')

    return redirect(url_for("todo"))


@app.route('/update/<int:todo_id>')
def update(todo_id):

    todo = db.get_or_404(Todo, todo_id)
    todo.complete = not todo.complete
    db.session.commit()

    flash('Оновлено.', 'success')

    return redirect(url_for('todo'))


@app.route('/delete/<int:todo_id>')
def delete(todo_id):

    todo = db.get_or_404(Todo, todo_id)
    db.session.delete(todo)
    db.session.commit()

    flash('Видалено.', 'success')

    return redirect(url_for('todo'))


#lab 7/lab 8

@app.route("/register", methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()

        if existing_user:
            flash('Username already taken. Please choose a different username.', 'danger')

            if existing_email:
                flash('Email already taken. Please choose a different email.', 'danger')

        else:

            new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Account successfully created for {form.username.data}!', 'success')
            return redirect(url_for('login'))
    
        flash(f'Something went wrong', 'warning')
    return render_template('register.html', form=form, title='Register')


@app.route("/login", methods=['GET', 'POST'])
def login():   

    if current_user.is_authenticated:
        return redirect(url_for('home'))
     
    form = LoginForms()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', category='success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your email and password.', category='danger')
                
    return render_template("login.html", form=form, title='Login')


@app.route('/users')
def users():
    all_users = User.query.all()
    total_users = len(all_users)
    return render_template("users.html", all_users=all_users, total_users=total_users)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.username.data != current_user.username or form.email.data != current_user.email:
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.about_me = form.about_me.data
            current_user.last_seen = form.last_seen.data
            db.session.commit()

        if form.image_file.data:
            current_user.image_file = save_picture(form.image_file.data)
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('account'))
        else:
            flash('No changes were made to your account.', 'info')

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data =  current_user.about_me
        form.last_seen.data = current_user.last_seen

    return render_template('account.html', title='Account', form=form)


