import pandas as pd

from . import data_sec
from .models import Favourite
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .search_recipes import search_for_recipe_by_ingredients_TFIDF, search_recipe_from_favourite, recommendedWord, \
    search_for_recipe_by_name_TFIDF, getdetails

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/ingredients', methods=['POST'])
@login_required
def ingredients():
    query = request.form.get('ingredients')
    recommendWord = request.form.get("recommendWord")
    if recommendWord != "":
        query = recommendWord
    data_ingredients = ""
    if query != "":
        data_ingredients = search_for_recipe_by_ingredients_TFIDF(data_sec, query)
    recommendWordReturn = ""
    if query != recommendedWord(query):
        recommendWordReturn = recommendedWord(query)
    # print(recommendWordReturn)

    return render_template('search_ingredients_list.html', user_id=current_user.id, data=data_ingredients,
                           recommendWord=recommendWordReturn, query=query)


@main.route('/favourite')
@login_required
def favourite():
    favourite = Favourite.query.filter(Favourite.userid == current_user.id).all()
    return render_template('favouritelist.html', data=favourite, userid=current_user.id, recommendWord="")


@main.route('/details', methods=['POST'])
@login_required
def details():
    query = request.form.get('food_name')
    data = getdetails(data_sec, query)
    data_ingredients = search_for_recipe_by_ingredients_TFIDF(data_sec, data['Ingredients'])
    data_ingredients = data_ingredients[1:5]
    return render_template('details.html', data=data, data2= data_ingredients)


@main.route('/name', methods=['POST', 'GET'])
@login_required
def nameFood():
    query = request.form.get('name')
    recommendWord = request.form.get("recommendWord")
    if recommendWord != "":
        query = recommendWord
    data_name = ""
    if query != "":
        data_name = search_for_recipe_by_name_TFIDF(data_sec, query)
    # checking correct spelling word
    recommendWordReturn = ""
    if query != recommendedWord(query):
        recommendWordReturn = recommendedWord(query)

    return render_template('search_ingredients_list.html', user_id=current_user.id, data=data_name,
                           recommendWord=recommendWordReturn)


@main.route('/searchFavourite', methods=['POST'])
@login_required
def search_favourite():
    search_fav = request.form.get("searchFavourite")
    recommendWord = request.form.get("recommendWord")
    if recommendWord != "":
        search_fav = recommendWord

    favourite = Favourite.query.filter(Favourite.userid == current_user.id).all()
    favourite_list = []
    for fav in favourite:
        favourite_list.append([fav.id, fav.title, fav.image])
    df = pd.DataFrame(favourite_list, columns=['id', 'title', 'image'])
    data_favourite = search_recipe_from_favourite(df, search_fav)

    # checking correct spelling word
    recommendWordReturn = ""
    if search_fav != recommendedWord(search_fav):
        recommendWordReturn = recommendedWord(search_fav)

    return render_template('favouritelist.html', data=data_favourite, userid=current_user.id,
                           recommendWord=recommendWordReturn, searchFavourite=search_fav)
