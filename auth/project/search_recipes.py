import string
import numpy as np
import pandas as pd

from symspellpy import SymSpell
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

sym_spell = SymSpell()


def get_and_clean():
    readFile = pd.read_csv('../resource/Food Ingredients and Recipe Dataset with Image Name Mapping.csv')
    readFile = pd.DataFrame(readFile)
    readFile = readFile.drop_duplicates()
    readFile = readFile.replace("", np.nan)
    readFile = readFile.replace("#NAME?", np.nan)
    readFile = readFile.dropna(how="any", axis="rows")
    for i, row in readFile.iterrows():
        readFile.at[i, 'Instructions'] = readFile.at[i, 'Instructions'].lower()
        readFile.at[i, 'Instructions'] = readFile.at[i, 'Instructions'].translate(
            str.maketrans('', '', '[\',$\_&+:;=?@#|<>^*%\\!"-]' + u'\xa0'))

        readFile.at[i, 'Instructions'] = readFile.at[i, 'Instructions'].translate(
            str.maketrans(string.whitespace, ' ' * len(string.whitespace), ''))

    return readFile


def bagOfNameWords():
    data_sec = get_and_clean()
    for i, row in data_sec.iterrows():
        data_sec.at[i, 'Title'] = data_sec.at[i, 'Title'].lower()
        data_sec.at[i, 'Title'] = data_sec.at[i, 'Title'].translate(
            str.maketrans('', '', '[$\'_&+,:;=?@\[\]#|<>.^*%\\!"-]' + u'\xa0'))
        data_sec.at[i, 'Title'] = data_sec.at[i, 'Title'].translate(
            str.maketrans(string.whitespace, ' ' * len(string.whitespace), ''))

    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X = vectorizer.fit_transform(data_sec['Title'])
    listToString = ' '.join([str(element) for element in vectorizer.get_feature_names()])  # fetch words
    file = open('../static/resources/bagOfName.txt', 'w', encoding='utf-8')
    file.write(listToString)
    file.close()


def bagOfIngredientWords():
    data_sec = get_and_clean()
    for i, row in data_sec.iterrows():
        data_sec.at[i, 'Cleaned_Ingredients'] = data_sec.at[i, 'Cleaned_Ingredients'].lower()
        data_sec.at[i, 'Cleaned_Ingredients'] = data_sec.at[i, 'Cleaned_Ingredients'].translate(
            str.maketrans('', '', '[$\_&+:;=?@#|<>.^*%\\!"-]' + u'\xa0'))
        data_sec.at[i, 'Cleaned_Ingredients'] = data_sec.at[i, 'Cleaned_Ingredients'].translate(
            str.maketrans(string.whitespace, ' ' * len(string.whitespace), ''))

    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X = vectorizer.fit_transform(data_sec['Cleaned_Ingredients'])
    listToString = ' '.join([str(element) for element in vectorizer.get_feature_names()])  # fetch words
    file = open('../static/resources/bagOfIngredients.txt', 'w', encoding='utf-8')
    file.write(listToString)
    file.close()


def search_for_recipe_by_ingredients_TFIDF(data_sec, ingredients):
    ingredientsName = data_sec
    for i, row in ingredientsName.iterrows():
        ingredientsName.at[i, 'Cleaned_Ingredients'] = ingredientsName.at[i, 'Cleaned_Ingredients'].lower()
        ingredientsName.at[i, 'Cleaned_Ingredients'] = ingredientsName.at[i, 'Cleaned_Ingredients'].translate(
            str.maketrans('', '', '[$\_&+:;=?@#|<>.^*%\\!"-]' + u'\xa0'))
        ingredientsName.at[i, 'Cleaned_Ingredients'] = ingredientsName.at[i, 'Cleaned_Ingredients'].translate(
            str.maketrans(string.whitespace, ' ' * len(string.whitespace), ''))

    clean_input = ingredients
    clean_input = clean_input.lower()
    clean_input = clean_input.translate(str.maketrans('', '', string.punctuation + u'\xa0'))
    clean_input = clean_input.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), ''))

    vectorizer = TfidfVectorizer(ngram_range=(1, 3))
    X = vectorizer.fit_transform(ingredientsName['Cleaned_Ingredients'])
    query_vec = vectorizer.transform([clean_input])
    results = cosine_similarity(X, query_vec).reshape((-1,))
    query = []
    for i in results.argsort()[::-1]:
        if results[i] > 0:
            title = ingredientsName.iloc[i, 1]
            recipes = ingredientsName.iloc[i, 3]
            images = ingredientsName.iloc[i, 4]
            ingredients = ingredientsName.iloc[i, 5]
            query.append(
                {"Food_name": title, "Ingredients": ingredients, "Recipes": recipes, "Images": images + ".jpg"})
    return query


def search_for_recipe_by_name_TFIDF(data_sec, name):
    recipeName = data_sec
    for i, row in recipeName.iterrows():
        recipeName.at[i, 'Title'] = recipeName.at[i, 'Title'].lower()
        recipeName.at[i, 'Title'] = recipeName.at[i, 'Title'].translate(
            str.maketrans('', '', '[$\'_&+,:;=?@\[\]#|<>.^*%\\!"-]' + u'\xa0'))
        recipeName.at[i, 'Title'] = recipeName.at[i, 'Title'].translate(
            str.maketrans(string.whitespace, ' ' * len(string.whitespace), ''))

    clean_input = name
    clean_input = clean_input.lower()
    clean_input = clean_input.translate(str.maketrans('', '', string.punctuation + u'\xa0'))
    clean_input = clean_input.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), ''))

    vectorizer = TfidfVectorizer(ngram_range=(1, 3))
    X = vectorizer.fit_transform(recipeName['Title'])
    query_vec = vectorizer.transform([clean_input])
    results = cosine_similarity(X, query_vec).reshape((-1,))
    query = []
    for i in results.argsort()[::-1]:
        if results[i] > 0:
            title = recipeName.iloc[i, 1]
            recipes = recipeName.iloc[i, 3]
            images = recipeName.iloc[i, 4]
            ingredients = recipeName.iloc[i, 5]
            query.append(
                {"Food_name": title, "Ingredients": ingredients, "Recipes": recipes, "Images": images + ".jpg"})
    return query


def search_recipe_from_favourite(data_sec, favouriteInput):
    favouriteRecipe = data_sec
    clean_input = favouriteInput
    clean_input = clean_input.lower()
    clean_input = clean_input.translate(str.maketrans('', '', string.punctuation + u'\xa0'))
    clean_input = clean_input.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), ''))

    vectorizer = TfidfVectorizer(ngram_range=(1, 3))
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


# check correct spelling and suggest the possible spelling corrections
def recommendedNameWord(nameWord):
    sym_spell.create_dictionary('../auth/project/static/resources/bagOfName.txt', encoding='utf-8')
    sym_correct = sym_spell.word_segmentation(nameWord)
    return sym_correct.corrected_string


def recommendedIngredientWord(ingredientWord):
    sym_spell.create_dictionary('../auth/project/static/resources/BagOfIngredients.txt', encoding='utf-8')
    sym_correct = sym_spell.word_segmentation(ingredientWord)
    return sym_correct.corrected_string


def getdetails(data_sec, foodname):
    data = data_sec
    foodname = foodname

    list = []
    for j, row in data.iterrows():
        if data.at[j, 'Title'] == foodname:
            list.append({"Name": data.at[j, 'Title'],
                         "Instructions": data.at[j, 'Instructions'],
                         "Ingredients": data.at[j, 'Cleaned_Ingredients'],
                         "Image": data.at[j, 'Image_Name'] + ".jpg"})

    return list[0]


def currentPage(currentPage, allPages):
    prev_page = True
    next_page = True
    if currentPage - 1 >= 0:
        prev_page = True
    else:
        prev_page = False

    if currentPage + 1 < allPages:
        next_page = True
    else:
        next_page = False

    return [{'prevPage': prev_page, 'nextPage': next_page}]


def pagination(dataInput):
    dataPerPage = 9
    result = len(dataInput)
    data = []
    point = 0
    if result / dataPerPage <= 1:
        data.append(dataInput)
        return data
    else:
        pageNumber = result // dataPerPage
        for i in range(pageNumber + 1):
            if point < result:
                dataTemp = []
                for j in range(dataPerPage):
                    if point < result:
                        dataTemp.append(dataInput[point])
                        point = point + 1
                data.append(dataTemp)
        return data


if __name__ == '__main__':
    get_and_clean()
    bagOfNameWords()
    bagOfIngredientWords()
