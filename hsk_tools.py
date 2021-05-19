'''
Useful tools when working with chinese vocabulary datasets.
'''
import os
import re
import pandas as pd

try:
    os.chdir('G:/My Drive/Chinesisch')
except:
    os.chdir('G:/Meine Ablage/Chinesisch')


def get_hsk_list(level=None):
    '''
    returns a dataset containing vocabulary for the given hsk-level

    Parameters
    level : int, optional, hsk-level. gets all levels if None

    Returns
    hsk : pandas dataframe, contains vocabulary for hsk level

    '''

    link = 'https://raw.githubusercontent.com/glxxyz/hskhsk.com/main/data/lists/HSK%20Official%20With%20Definitions%202012%20L'
    names = ['Hanzi', 'Traditional', 'Coded Pinyin', 'Pinyin', 'English']
    if level:
        hsk = pd.read_csv(link + '{}.txt'.format(level), sep='	', names=names)
    else:
        hsk = pd.read_csv(link + '1.txt', sep='	', names=names)
        hsk['Level'] = 1
        for lvl in range(2,7):
            lvl_list = pd.read_csv(link + '{}.txt'.format(lvl), sep='	', names=names, index_col=False)
            lvl_list['Level'] = lvl
            hsk = hsk.append(lvl_list, ignore_index=True)

    return hsk


def create_char_df(hsk_list, level=None):
    '''
    generates list of characters from given list of words

    Parameters
    hsk_list : pandas dataframe, contains columns 'Hanzi' with chinese words
    level : int, optional, adds level tag to characters in seperate columns 'Level'

    Returns
    charDf : pandas dataframe, lists all characters and level

    '''
    char_list = []
    for i in range(1,7):

        step = ''.join(hsk_list.loc[hsk_list.Level==i, 'Hanzi'].to_list())

        for other in char_list:
            for char in other:
                step = step.replace(char, '')

        char_list.append(step)

    char_df = pd.DataFrame({'Hanzi': list(char_list[0]), 'Level': [level]*len(char_list[0])})
    for i in range(1,6):
        char_df = char_df.append(pd.DataFrame({'Hanzi': list(char_list[i]), 'Level': [i+1]*len(char_list[i])}))

    char_df = char_df.drop_duplicates()
    return char_df


def assign_lvl_to_char(char, max_level, df_chars):
    '''returns hsk level for a given character'''
    try:
        lvl = df_chars.loc[df_chars.Hanzi==char, 'HSK level'].reset_index(drop=True).iloc[0]
    except:
        lvl = max_level + 1

    return lvl


def assign_lvl_to_sentence(string, max_level, df_chars):
    '''returns the hardest characters hsk level'''
    lvl = max([assign_lvl_to_char(c, max_level, df_chars) for c in string])

    return lvl

def extract_hanzi_from_string(string):
    '''filters out any western characters like english names from a given string'''
    string = ''.join([a for a in string if a.isalnum()])
    string = re.sub('[A-Za-z]+', '', string)

    return string


def assign_lvl_to_column(df_vocab, max_level, df_chars, col_name='Hanzi'):
    '''applies sentence-level assignment of hsk-level to a whole column'''
    level = df_vocab[col_name].apply(lambda x: assign_lvl_to_sentence(x, max_level, df_chars))

    return level


def count_hsk(df_vocab, hsk=None, level=None, name='Hanzi', target='Chinese'):
    '''counts number of words in vocab that are part of the given hsk list.
    alternatively, pass a level to have the list being loaded from the internet

    vocab: pandas dataframe, vocabulary list
    hsk: pandas dataframe, contains words to look for
    level: hsk level to look for
    name: str, name of column in "vocab"
    target: str, name of column in "hsk"
    '''
    if not hsk:
        hsk = get_hsk_list(level=level)
    counted = df_vocab[name].apply(lambda x: x in hsk[target].to_list()).sum()

    return counted


def encode_vocab_list():
    '''adds columns 'Pinyin + English' and 'Hanzi + Pinyin' to given dataset
    for usage in anki-app as backside of cards'''
    df_vocab = pd.read_excel('Full Vocab List.xlsx', usecols=['Hanzi', 'English', 'Pinyin'])
    df_vocab['Pinyin + English'] = df_vocab.Pinyin + ' - ' + df_vocab.English
    df_vocab['Hanzi + Pinyin'] = df_vocab.Hanzi + ' - ' + df_vocab.Pinyin

    df_vocab.to_csv('Full Vocab List.csv', encoding='utf-8', index=False)


def encode_char_list():
    '''adds column 'Pinyin + Definition' to given dataset for usage in
    anki-app as backside of cards'''
    df_vocab = pd.read_excel('Characters.xlsx', usecols=['Hanzi', 'Pinyin', 'Definition', 'HSK level'])
    df_vocab['Pinyin + Definition'] = df_vocab.Pinyin + ' - ' + df_vocab.Definition
    df_vocab.to_csv('Characters.csv', encoding='utf8', index=False)


def plot_hsk_levels(hanzi_series):
    '''placeholder. will plot level of cahracters in a given column as pie chart'''
    pass
