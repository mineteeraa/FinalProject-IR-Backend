import string
import pandas as pd


def get_and_clean(filePath):
    readFile = pd.read_csv(filePath)
    readFile = pd.DataFrame(readFile)
    data_sec = readFile[readFile['Idiom'] == 'ENGLISH']
    data_sec = data_sec.drop_duplicates(subset=["SLink"])
    for i, row in data_sec.iterrows():
        data_sec.at[i, 'ALink'] = data_sec.at[i, 'ALink'].lstrip('/').rstrip('/')
    return data_sec

def Artist(data_sec, artist_name):
    articsName = data_sec
    for i, row in articsName.iterrows():
        articsName.at[i, 'ALink'] = articsName.at[i, 'ALink'].lower()
        articsName.at[i, 'ALink'] = articsName.at[i, 'ALink'].translate(str.maketrans('', '', string.punctuation + u'\xa0'))
        articsName.at[i, 'ALink'] = articsName.at[i, 'ALink'].translate(str.maketrans(string.whitespace, ' '*len(string.whitespace), ''))

    clean_input = artist_name
    clean_input = clean_input.lower()
    clean_input = clean_input.translate(str.maketrans('', '', string.punctuation + u'\xa0'))
    clean_input = clean_input.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), ''))
    print("Song of: ", artist_name)
    list = []
    for j, row in articsName.iterrows():
        if articsName.at[j, 'ALink'] == clean_input:
            list.append([articsName.at[j, 'SName']])
    list_df = pd.DataFrame(list, columns=['Song'])
    list_df = list_df.sort_values('Song')
    list_df.to_json('query/artist1.json', orient='records', indent=4)
    print("done")


if __name__ == '__main__':
    get_and_clean("filepath")