import requests
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from .models import Favourite
from .search_recipes import search_for_recipe_by_ingredients_TFIDF
from . import data_sec

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/ingredients', methods=['POST', 'GET'])
@login_required
def ingredients():
    query = request.form.get('ingredients')
    data_ingredients = search_for_recipe_by_ingredients_TFIDF(data_sec, query)
    return render_template('search_ingredients_list.html', user_id=current_user.id, data=data_ingredients)


@main.route('/favourite')
@login_required
def favourite():
    favourite = Favourite.query.filter(Favourite.userid == current_user.id).all()
    return render_template('favouritelist.html', data=favourite, userid=current_user.id)

