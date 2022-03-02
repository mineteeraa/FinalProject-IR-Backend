from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Favourite
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user and not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists.')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/add-favourite', methods=['POST', 'GET'])
def add_favourite():
    food_name = request.form.get('food_name')
    food_image = request.form.get('food_image')
    user = request.form.get('user')

    favourite = Favourite.query.filter_by(title=food_name, userid=user).first()
    if favourite:
        flash(0)
        return redirect(url_for('main.favourite'))

    new_favourite = Favourite(title=food_name, image=food_image, userid=user)
    db.session.add(new_favourite)
    db.session.commit()
    flash(1)
    return render_template('search_ingredients_list.html')


@auth.route('/delete-favourite/<id>')
def delete_favourite(id):
    delete_favourite = Favourite.query.get(id)
    db.session.delete(delete_favourite)
    db.session.commit()
    return redirect(url_for('main.favourite'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
