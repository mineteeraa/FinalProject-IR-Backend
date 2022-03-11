import pandas as pd

from . import data_sec
from .models import Favourite
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .search_recipes import search_for_recipe_by_ingredients_TFIDF, search_recipe_from_favourite, recommendedNameWord, \
    recommendedIngredientWord, search_for_recipe_by_name_TFIDF, getdetails, pagination, currentPage

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if current_user.is_authenticated:
        return render_template("index.html", name=current_user.name)
    else:
        return render_template("login.html")


@main.route('/ingredients', methods=['POST'])
@login_required
def ingredients():
    query = request.form.get('ingredients')
    recommendWord = request.form.get("recommendWord")
    page = int(request.form.get('inputPage'))
    if recommendWord != "":
        query = recommendWord

    data_ingredients = ""
    recommendWordReturn = ""
    if query != "":
        # checking correct spelling word
        if query != recommendedIngredientWord(query):
            recommendWordReturn = recommendedIngredientWord(query)
            # keep correct word that not effect to main query
            temp = recommendWordReturn
            data_ingredients = search_for_recipe_by_ingredients_TFIDF(data_sec, temp)
        else:
            data_ingredients = search_for_recipe_by_ingredients_TFIDF(data_sec, query)

    result = len(data_ingredients)
    data = pagination(data_ingredients)
    allPages = len(data)
    hasOtherPage = currentPage(page, allPages)
    data = data[page]

    return render_template('search_ingredients.html', user_id=current_user.id, data=data,
                           recommendWord=recommendWordReturn, name=current_user.name, query=query,
                           hasOtherPage=hasOtherPage, page=page, allPages=allPages, result=result)


@main.route('/name', methods=['POST', 'GET'])
@login_required
def nameFood():
    query = request.form.get('name')
    recommendWord = request.form.get("recommendWord")
    page = int(request.form.get('inputPage'))
    if recommendWord != "":
        query = recommendWord

    data_name = ""
    recommendWordReturn = ""
    if query != "":
        # checking correct spelling word
        if query != recommendedNameWord(query):
            recommendWordReturn = recommendedNameWord(query)
            # keep correct word that not effect to main query
            temp = recommendWordReturn
            data_name = search_for_recipe_by_name_TFIDF(data_sec, temp)
        else:
            data_name = search_for_recipe_by_name_TFIDF(data_sec, query)

    result = len(data_name)
    data = pagination(data_name)
    allPages = len(data)
    hasOtherPage = currentPage(page, allPages)
    data = data[page]

    return render_template('search_nameFood.html', user_id=current_user.id, data=data,
                           recommendWord=recommendWordReturn, name=current_user.name, query=query,
                           hasOtherPage=hasOtherPage, page=page, allPages=allPages, result=result)


@main.route('/favourite')
@login_required
def favourite():
    favourite = Favourite.query.filter(Favourite.userid == current_user.id).all()
    totalFavourite = len(favourite)
    return render_template('favouritelist.html', data=favourite, userid=current_user.id, recommendWord="",
                           name=current_user.name, result=None, totalFavourite=totalFavourite)


@main.route('/details', methods=['POST'])
@login_required
def details():
    query = request.form.get('food_name')
    data = getdetails(data_sec, query)
    data_ingredients = search_for_recipe_by_ingredients_TFIDF(data_sec, data['Ingredients'])
    data_ingredients = data_ingredients[1:5]
    return render_template('details.html', data=data, data2=data_ingredients, name=current_user.name,
                           user_id=current_user.id)


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

    data_favourite = ""
    recommendWordReturn = ""
    if search_fav != "":
        # checking correct spelling word
        if search_fav != recommendedNameWord(search_fav):
            recommendWordReturn = recommendedNameWord(search_fav)
            # keep correct word that not effect to main query
            temp = recommendWordReturn
            data_favourite = search_recipe_from_favourite(df, temp)
        else:
            data_favourite = search_recipe_from_favourite(df, search_fav)

    result = len(data_favourite)

    return render_template('favouritelist.html', data=data_favourite, userid=current_user.id,
                           recommendWord=recommendWordReturn, searchFavourite=search_fav, name=current_user.name,
                           result=result, totalFavourite=0)
