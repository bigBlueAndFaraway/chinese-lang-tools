'''
Filter given list of chinese sentences by HSK-level

'''

import pandas as pd
from hsk_tools import hskInterpreter

LEVEL = 4

def load_sentence_datasets(level):
    '''loads datasets in given folderpath and renames columns. specific to the
    given datasets

    level: hsk level. necessary to load correct dataset
    '''

    names_1 = ['Sentence 1 - Chinese', 'Sentence 1 - Pinyin', 'Sentence 1 - English']
    names_2 = ['Sentence 2 - Chinese', 'Sentence 2 - Pinyin', 'Sentence 2 - English']
    new_names = ['Hanzi', 'Pinyin', 'English']

    df_sentences = pd.read_excel('sentences/HSK {} Sentences Examples.xlsx'.format(level))
    df_1 = df_sentences[names_1].dropna()
    df_1.columns = new_names
    
    df_2 = df_sentences[names_2].dropna()
    df_2.columns = new_names
    
    df_sentences = df_1.append(df_2)
    del df_1, df_2

    df_sentences['Hanzi + Pinyin'] = df_sentences.Hanzi + ' - ' + df_sentences.Pinyin
    df_sentences['Pinyin + English'] = df_sentences.Pinyin + ' - ' + df_sentences.English

    return df_sentences.reset_index(drop=True)


hsk = hskInterpreter()

df_sentences = load_sentence_datasets(LEVEL)
df_sentences = df_sentences[
    hsk.filter_by_level(df_sentences['Hanzi'], LEVEL, how='index')]

df_sentences.to_csv('sentences/Chinese Sentences HSK {} Filtered.csv'.format(LEVEL), encoding='UTF8', index=False)

