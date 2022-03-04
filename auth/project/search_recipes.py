import string

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


def get_and_clean():
    readFile = pd.read_csv('../resource/Food Ingredients and Recipe Dataset with Image Name Mapping.csv')
    readFile = pd.DataFrame(readFile)
    readFile = readFile.dropna()
    readFile = readFile.drop_duplicates()
    for i, row in readFile.iterrows():
        readFile.at[i, 'Instructions'] = readFile.at[i, 'Instructions'].lower()
        readFile.at[i, 'Instructions'] = readFile.at[i, 'Instructions'].translate(
            str.maketrans('', '', string.punctuation + u'\xa0'))
        readFile.at[i, 'Instructions'] = readFile.at[i, 'Instructions'].translate(
            str.maketrans(string.whitespace, ' ' * len(string.whitespace), ''))

    return readFile


def search_for_recipe_by_ingredients_TFIDF(data_sec, ingredients):
    ingredientsName = data_sec
    for i, row in ingredientsName.iterrows():
        ingredientsName.at[i, 'Cleaned_Ingredients'] = ingredientsName.at[i, 'Cleaned_Ingredients'].lower()
        ingredientsName.at[i, 'Cleaned_Ingredients'] = ingredientsName.at[i, 'Cleaned_Ingredients'].translate(
            str.maketrans('', '', string.punctuation + u'\xa0'))
        ingredientsName.at[i, 'Cleaned_Ingredients'] = ingredientsName.at[i, 'Cleaned_Ingredients'].translate(
            str.maketrans(string.whitespace, ' ' * len(string.whitespace), ''))

    print("-------------------------------------------")
    print("input ingredients: ")
    # ingredients = input()
    clean_input = ingredients
    clean_input = clean_input.lower()
    clean_input = clean_input.translate(str.maketrans('', '', string.punctuation + u'\xa0'))
    clean_input = clean_input.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), ''))

    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X = vectorizer.fit_transform(ingredientsName['Cleaned_Ingredients'])
    query_vec = vectorizer.transform([clean_input])
    results = cosine_similarity(X, query_vec).reshape((-1,))
    query = []
    for i in results.argsort()[-5:][::-1]:
        query.append({
            "Food_name": ingredientsName.at[i, 'Title'],
            "Ingredients": ingredientsName.at[i, 'Cleaned_Ingredients'],
            "Recipes": ingredientsName.at[i, 'Instructions'],
            "Images": ingredientsName.at[i, 'Image_Name'] + ".jpg"
        })
    return query


def search_recipe_from_favourite(data_sec, favouriteInput):
    favouriteRecipe = data_sec
    clean_input = favouriteInput
    clean_input = clean_input.lower()
    clean_input = clean_input.translate(str.maketrans('', '', string.punctuation + u'\xa0'))
    clean_input = clean_input.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), ''))
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X = vectorizer.fit_transform(favouriteRecipe['title'])
    query_vec = vectorizer.transform([clean_input])
    results = cosine_similarity(X, query_vec).reshape((-1,))
    query = []
    for i in results.argsort()[::-1]:
        if results[i] > 0:
            query.append({
                "id": favouriteRecipe.at[i, 'id'],
                "title": favouriteRecipe.at[i, 'title'],
                "image": favouriteRecipe.at[i, 'image']
            })
    return query


if __name__ == '__main__':
    get_and_clean()
