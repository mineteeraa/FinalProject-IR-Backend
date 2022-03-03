import string
import pandas as pd

from spellchecker import SpellChecker
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

spell = SpellChecker()


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

    search_for_recipe_by_name_TFIDF(readFile)


def search_for_recipe_by_name_TFIDF(data_sec):
    recipeName = data_sec
    for i, row in recipeName.iterrows():
        recipeName.at[i, 'Title'] = recipeName.at[i, 'Title'].lower()
        recipeName.at[i, 'Title'] = recipeName.at[i, 'Title'].translate(
            str.maketrans('', '', '([$\'_&+,:;=?@\[\]#|<>.^*()%\\!"-])' + u'\xa0'))
        recipeName.at[i, 'Title'] = recipeName.at[i, 'Title'].translate(
            str.maketrans(string.whitespace, ' ' * len(string.whitespace), ''))

    print("-------------------------------------------")
    print("input name: ")
    recipe_name = input()
    clean_input = recipe_name
    clean_input = clean_input.lower()
    clean_input = clean_input.translate(str.maketrans('', '', '([$\'_&+,:;=?@\[\]#|<>.^*()%\\!"-])' + u'\xa0'))
    clean_input = clean_input.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), ''))

    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X = vectorizer.fit_transform(recipeName['Title'])
    query_vec = vectorizer.transform([clean_input])
    results = cosine_similarity(X, query_vec).reshape((-1,))
    count = 0
    query = []
    for i in results.argsort()[-10:][::-1]:
        title = recipeName.iloc[i, 1]
        recipes = recipeName.iloc[i, 3]
        count += 1
        query.append([title, recipes])
    querydf = pd.DataFrame(query, columns=["Title", "Recipes"])
    print(querydf)


# check correct spelling and suggest the possible spelling corrections
def recommendedWord(word):
    spell_correct = ""
    for w in word.split():
        if w == spell.correction(w):
            if spell_correct == "":
                spell_correct += w
            else:
                spell_correct = spell_correct + " " + w

        else:
            if spell_correct == "":
                spell_correct = spell_correct + spell.correction(w)
            else:
                spell_correct = spell_correct + " " + spell.correction(w)

    if word != spell_correct:
        return spell_correct
    else:
        return word


if __name__ == '__main__':
    get_and_clean()
