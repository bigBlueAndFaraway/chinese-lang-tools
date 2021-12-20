'''
Useful tools when working with chinese vocabulary datasets.
'''

import re
import pandas as pd
import matplotlib.pyplot as plt
import unit_tests


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
            return None


    def sentence_lvl(self, sentence):
        '''extracts hanzi characters and returns the highest hsk level'''
        sentence = ''.join([a for a in sentence if a.isalnum()])
        sentence = re.sub('[A-Za-z]+', '', sentence)
        return max([self.char_lvl(c) for c in sentence])


    def column_lvl(self, column):
        '''applies sentence-level assignment of hsk-level to a whole column'''
        return column.apply(lambda x: self.sentence_lvl(x))


    def count_hsk(self, column):
        '''counts number of words in vocab that are part of the given hsk list.
        evaluates on word level (as opposed to self.column_lvl(), which evaluates
        on char level)

        column: series, contains words to be checked
        level: int, optional, return number of words in given level, return all
            level counts if level is none
        '''
        counted = (column.to_frame()
                   .merge(self.vocab[['Hanzi', 'Level']], on='Hanzi', how='left')
                   .fillna('Not in HSK'))

        return counted['Level'].value_counts()

    
    def plot_hsk_levels(self, hanzi_series):
        '''plots hsk levels of characters in a donut chart'''
        
        plt.pie(hanzi_series, labels=hanzi_series.index)
        inner_circle = plt.Circle( (0,0), 0.7, color='white')
        p = plt.gcf()
        p.gca().add_artist(inner_circle)
        
        plt.show()

hsk = hskInterpreter()
unit_tests.test_all(hsk)

