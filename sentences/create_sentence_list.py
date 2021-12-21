'''
Filter given list of chinese sentences by HSK-level

Functions:
    extract_hanzi_from_string(string)
    assign_lvl_to_char(char)
    assign_lvl_to_sentence(string)
    load_datasets(level, folderpath, alternative_folderpath='')
    filter_by_level(df_sentences, chars, level)
'''
import os
import pandas as pd

level = 4

def load_datasets(level, folderpath, alternative_folderpath=''):
    '''loads datasets in given folderpath and renames columns. specific to the
    given datasets

    level: hsk level. necessary to load correct dataset
    folderpath: path where sentences dataset is located
    alternative_folderpath: default for unvalid folderpath. useful for local gdrive'''

    try:
        os.chdir(folderpath)
    except:
        os.chdir(alternative_folderpath)

    df_chars = pd.read_excel(folderpath + '\\Characters.xlsx')

    df_original = pd.read_excel(folderpath + '\\HSK {}.xlsx'.format(level))
    df_sentences = df_original[['Sentence 1 - Chinese', 'Sentence 1 - Pinyin', 'Sentence 1 - English']]
    df_original = df_original[['Sentence 2 - Chinese', 'Sentence 2 - Pinyin', 'Sentence 2 - English']].dropna()
    df_original.columns = ['Sentence 1 - Chinese', 'Sentence 1 - Pinyin', 'Sentence 1 - English']
    df_sentences = df_sentences.append(df_original)
    del df_original

    df_sentences.columns = ['Hanzi', 'Pinyin', 'English']
    df_sentences['Hanzi + Pinyin'] = df_sentences.Hanzi + ' - ' + df_sentences.Pinyin
    df_sentences['Pinyin + English'] = df_sentences.Pinyin + ' - ' + df_sentences.English

    return df_sentences, df_chars

df_sentences = pd.read_excel('sentences/HSK {} Sentences.xlsx'.format(level))

def filter_by_level(df_sentences, df_chars, level):
    '''filters df_sentences by the characters in chars that are in given level or lower

    df_sentences: dataset with sentences. needs to have column called "Hanzi"
    df_chars: dataset containing characters for all levels. needs to have column called "HSK level"
    level
    '''

    df_chars = df_chars[df_chars['HSK level'] <= level]

    df_sentences['HSK level'] = df_sentences.Hanzi.apply(extract_hanzi_from_string)
    lvl_assign = lambda x: assign_lvl_to_sentence(x, level, df_chars)
    df_sentences['HSK level'] = df_sentences['HSK level'] .apply(lvl_assign)
    df_sentences = df_sentences[df_sentences['HSK level'] <= level]

    return df_sentences


df_sentences, df_chars = load_datasets(LEVEL, PATH, ALT_PATH)
df_sentences = filter_by_level(df_sentences, df_chars, LEVEL)

df_sentences.to_csv(os.getcwd() + '\\Chinese Sentences HSK {}.csv'.format(LEVEL), encoding='UTF8', index=False)
