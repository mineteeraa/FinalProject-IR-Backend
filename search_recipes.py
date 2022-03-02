import string
import pandas as pd

from spellchecker import SpellChecker
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

spell = SpellChecker()  # the default is English (language='en')


def get_and_clean():
    readFile = pd.read_csv('resource/Food Ingredients and Recipe Dataset with Image Name Mapping.csv')
    readFile = pd.DataFrame(readFile)
    readFile = readFile.dropna()
    readFile = readFile.drop_duplicates()
    for i, row in readFile.iterrows():
        readFile.at[i, 'Instructions'] = readFile.at[i, 'Instructions'].lower()
        readFile.at[i, 'Instructions'] = readFile.at[i, 'Instructions'].translate(
            str.maketrans('', '', '([$\'_&+,:;=?@\[\]#|<>.^*()%\\!"-])' + u'\xa0'))
        readFile.at[i, 'Instructions'] = readFile.at[i, 'Instructions'].translate(
            str.maketrans(string.whitespace, ' ' * len(string.whitespace), ''))

    search_for_recipe_by_ingredients_TFIDF(readFile)


def search_for_recipe_by_ingredients_TFIDF(data_sec):
    ingredientsName = data_sec
    for i, row in ingredientsName.iterrows():
        ingredientsName.at[i, 'Cleaned_Ingredients'] = ingredientsName.at[i, 'Cleaned_Ingredients'].lower()
        ingredientsName.at[i, 'Cleaned_Ingredients'] = ingredientsName.at[i, 'Cleaned_Ingredients'].translate(
            str.maketrans('', '', '([$\'_&+,:;=?@\[\]#|<>.^*()%\\!"-])' + u'\xa0'))
        ingredientsName.at[i, 'Cleaned_Ingredients'] = ingredientsName.at[i, 'Cleaned_Ingredients'].translate(
            str.maketrans(string.whitespace, ' ' * len(string.whitespace), ''))

    print("-------------------------------------------")
    print("input ingredients: ")
    ingredients = input()
    clean_input = ingredients
    clean_input = clean_input.lower()
    clean_input = clean_input.translate(str.maketrans('', '', '([$\'_&+,:;=?@\[\]#|<>.^*()%\\!"-])' + u'\xa0'))
    clean_input = clean_input.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), ''))

    # check correct spelling and suggest the possible spelling corrections
    spell_correct = ""
    for element in clean_input.split():
        if element == spell.correction(element):
            if spell_correct == "":
                spell_correct += element
            else:
                spell_correct = spell_correct + " " + element
        else:
            if spell_correct == "":
                spell_correct = spell_correct + spell.correction(element)
            else:
                spell_correct = spell_correct + " " + spell.correction(element)
    if clean_input != spell_correct:
        print("Showing results for", spell_correct)
    # spell_candidate = spell.candidates(spell_correct)
    # print("Related Search: ", spell_candidate)

    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X = vectorizer.fit_transform(ingredientsName['Cleaned_Ingredients'])
    query_vec = vectorizer.transform([spell_correct])
    results = cosine_similarity(X, query_vec).reshape((-1,))
    count = 0
    query = []
    for i in results.argsort()[-5:][::-1]:
        ingredients = ingredientsName.iloc[i, 5]
        recipes = ingredientsName.iloc[i, 3]
        count += 1
        query.append([ingredients, recipes])
    querydf = pd.DataFrame(query, columns=["Ingredients", "Recipes"])
    print(querydf)


if __name__ == '__main__':
    get_and_clean()
