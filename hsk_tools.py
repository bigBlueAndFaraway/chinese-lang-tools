'''
Useful tools when working with chinese vocabulary datasets.
'''

import re
import pandas as pd
import matplotlib.pyplot as plt
import unit_tests
import numpy as np


class hskInterpreter():
    
    def __init__(self):
        self.vocab = pd.read_csv('resources/hsk_list.csv')
        self.chars = pd.read_csv('resources/hsk_chars.csv')
        self.char_indices = pd.read_csv('resources/hsk_chars.csv', index_col='Hanzi')


    def char_lvl(self, char):
        '''returns hsk level for a given character'''
        try:
            return self.char_indices.loc[char, 'Level']
        except(KeyError):
            return np.nan


    def sentence_lvl(self, sentence):
        '''extracts hanzi characters and returns the highest hsk level'''
        sentence = ''.join([a for a in sentence if a.isalnum()])
        sentence = re.sub('[A-Za-z]+', '', sentence)
        
        return max([self.char_lvl(c) for c in sentence])


    def column_lvl(self, hanzi_col):
        '''applies sentence-level assignment of hsk-level to a whole column'''
        return hanzi_col.apply(lambda x: self.sentence_lvl(x))


    def count_hsk(self, hanzi_col):
        '''counts number of words in vocab that are part of the given hsk list.
        evaluates on word level (as opposed to self.column_lvl(), which evaluates
        on char level)

        column: series, contains words to be checked
        level: int, optional, return number of words in given level, return all
            level counts if level is none
        '''
        counted = (hanzi_col.to_frame()
                   .merge(self.vocab[['Hanzi', 'Level']], on='Hanzi', how='left')
                   .fillna('Not in HSK'))

        return counted['Level'].value_counts()

    
    def plot_hsk_levels(self, hanzi_col):
        '''plots hsk levels of characters in a donut chart'''
        
        plt.pie(hanzi_col, labels=hanzi_col.index)
        inner_circle = plt.Circle( (0,0), 0.7, color='white')
        p = plt.gcf()
        p.gca().add_artist(inner_circle)
        
        plt.show()
    
    
    def filter_by_level(self, hanzi_col, level, how='inplace'):
        '''filters column by the characters in chars that are in given level or lower
    
        hanyu_col: pd.Series, column with words or sentences
        level: integer, hsk level by which data should be filtered
        how: string, default: "inplace". set to "index" to return indices instead of values
        '''
        
        extract_hanzi = lambda s: re.sub('[A-Za-z]+', '', ''.join([c for c in s if c.isalnum()]))
        hanzi_col = hanzi_col.apply(extract_hanzi)

        lvl_col = hanzi_col.apply(self.sentence_lvl).dropna() <= level
        
        if how=='index':
            return lvl_col
        elif how=='inplace':
            hanzi_col = hanzi_col[lvl_col].reset_index(drop=True)
            return hanzi_col

hsk = hskInterpreter()
unit_tests.test_all(hsk)
