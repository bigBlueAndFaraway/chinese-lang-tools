
import pandas as pd

def get_df_hsk(level=None):
    '''
    returns a dataset containing vocabulary for the given hsk-level

    Parameters
    level : int, optional, hsk-level. gets all levels if None

    Returns
    df_vocab : pandas dataframe, contains vocabulary for hsk level

    '''

    link = 'https://raw.githubusercontent.com/glxxyz/hskhsk.com/main/data/lists/HSK%20Official%20With%20Definitions%202012%20L'
    names = ['Hanzi', 'Traditional', 'Coded Pinyin', 'Pinyin', 'English']
    if level:
        df_hsk = pd.read_csv(link + '{}.txt'.format(level), sep='	', names=names)
    else:
        df_hsk = pd.read_csv(link + '1.txt', sep='	', names=names)
        df_hsk['Level'] = 1
        for lvl in range(2,7):
            lvl_list = pd.read_csv(link + '{}.txt'.format(lvl), sep='	', names=names, index_col=False)
            lvl_list['Level'] = lvl
            df_hsk = df_hsk.append(lvl_list, ignore_index=True)
    
    return df_hsk


def create_char_df(hsk_list):
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

    df_chars = pd.DataFrame({'Hanzi': list(char_list[0]), 'Level': [1]*len(char_list[0])})
    for i in range(1,6):
        df_chars = df_chars.append(pd.DataFrame({'Hanzi': list(char_list[i]), 'Level': [i+1]*len(char_list[i])}))

    df_chars = df_chars.drop_duplicates().reset_index(drop=True)
    
    return df_chars


def vocab_to_anki():
    '''adds columns 'Pinyin + English' and 'Hanzi + Pinyin' to given dataset
    for usage in anki-app as backside of cards'''
    df_vocab = pd.read_excel('Full Vocab List.xlsx', usecols=['Hanzi', 'English', 'Pinyin'])
    df_vocab['Pinyin + English'] = df_vocab.Pinyin + ' - ' + df_vocab.English
    df_vocab['Hanzi + Pinyin'] = df_vocab.Hanzi + ' - ' + df_vocab.Pinyin

    df_vocab.to_csv('Full Vocab List.csv', encoding='utf-8', index=False)


def chars_to_anki():
    '''adds column 'Pinyin + Definition' to given dataset for usage in
    anki-app as backside of cards'''
    df_vocab = pd.read_excel('Characters.xlsx', usecols=['Hanzi', 'Pinyin', 'Definition', 'HSK level'])
    df_vocab['Pinyin + Definition'] = df_vocab.Pinyin + ' - ' + df_vocab.Definition
    df_vocab.to_csv('Characters.csv', encoding='utf8', index=False)


df_vocab = get_df_hsk()

df_chars = create_char_df(df_vocab)


df_vocab.to_csv('resources/hsk_list.csv')

df_chars.to_csv('resources/hsk_chars.csv')

