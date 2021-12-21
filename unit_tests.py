'''unit tests for functions in hsk_tools'''

import pandas as pd

def test_all(hsk):


    assert (hsk.char_lvl('话') == 1 and
        hsk.char_lvl('给') == 2 and
        hsk.char_lvl('干') == 3 and
        hsk.char_lvl('广') == 4 and
        hsk.char_lvl('抓') == 5 and
        hsk.char_lvl('颇') == 6), 'char_lvl test failed'
    
    assert (hsk.sentence_lvl('你今天怎么样?') == 1 and
            hsk.sentence_lvl('阿姨， 帮我把！') == 3 and
            hsk.sentence_lvl('你抽烟吗?') == 4), 'sentence_lvl test failed'

    assert (hsk.column_lvl(pd.Series(['婆婆', '加班', '看法'])) == pd.Series([5,3,3])).all(),\
        'column_lvl test failed'
    
    assert (hsk.count_hsk(
        pd.Series(['婆婆', '加班', '看法', '位', '熊猫', '奇怪', '敬酒'], name='Hanzi'))
        == pd.Series([3,2,2], index = ([3.0, 'Not in HSK', 4.0]))).all(),\
        'count_hsk test failed'

    assert (hsk.filter_by_level(
        pd.Series(['好棒啊', '加班', '看法', '我们一起去厨房吧', '啤酒很难喝', '老师好'], name='Hanzi'),
        3)
        == pd.Series(['加班', '看法', '啤酒很难喝', '老师好'], name='Hanzi')).all(),\
        'filter_by_level test failed'
        
