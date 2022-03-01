import re
import string
import numpy as np
import pandas as pd

from spellchecker import SpellChecker

spell = SpellChecker()


# def get_and_clean():
#     readFile = pd.read_csv('resource/Food Ingredients and Recipe Dataset with Image Name Mapping.csv')
#     readFile = pd.DataFrame(readFile)
#     search_for_recipe_by_name(readFile)

def get_and_clean():
    readFile = pd.read_csv('resource/Food Ingredients and Recipe Dataset with Image Name Mapping.csv')
    readFile = pd.DataFrame(readFile)
    readFile = readFile.dropna()
    readFile = readFile.drop_duplicates()
    for i, row in readFile.iterrows():
        readFile.at[i, 'Title'] = readFile.at[i, 'Title'].lower()
        readFile.at[i, 'Title'] = readFile.at[i, 'Title'].translate(str.maketrans('', '', string.punctuation + u'\xa0'))
        readFile.at[i, 'Title'] = readFile.at[i, 'Title'].translate(
            str.maketrans(string.whitespace, ' ' * len(string.whitespace), ''))

    search_for_recipe_by_name_TFIDF(readFile)


def search_for_recipe_by_name_TFIDF(data_sec):
    recipeName = data_sec
    for i, row in recipeName.iterrows():
        recipeName.at[i, 'Title'] = recipeName.at[i, 'Title'].lower()
        recipeName.at[i, 'Title'] = recipeName.at[i, 'Title'].translate(
            str.maketrans('', '', string.punctuation + u'\xa0'))
        recipeName.at[i, 'Title'] = recipeName.at[i, 'Title'].translate(
            str.maketrans(string.whitespace, ' ' * len(string.whitespace), ''))

    print("-------------------------------------------")
    print("input name: ")
    recipe_name = input()
    clean_input = recipe_name
    clean_input = clean_input.lower()
    clean_input = clean_input.translate(str.maketrans('', '', string.punctuation + u'\xa0'))
    clean_input = clean_input.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), ''))
    spell_correct = spell.correction(clean_input)
    print({'Recipe name': clean_input, 'Spell correct': ' '.join(spell_correct)})
    # print(recipe_name)

    list = []
    for j, row in recipeName.iterrows():
        if recipeName.at[j, 'Title'] == clean_input:
            list.append([recipeName.at[j, 'Instructions']])
    list_df = pd.DataFrame(list, columns=['Instructions'])
    list_df = list_df.sort_values('Instructions')

    count = 0
    for i, row in list_df.iterrows():
        count += 1
        print("Recipes:", list_df.at[i, 'Instructions'])


if __name__ == '__main__':
    get_and_clean()
