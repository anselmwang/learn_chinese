# very strange.
# If I send all the code in python console, anki_utils retrieve 0 cards from 第一册 deck
# however if I run the whole script directly, it works.
import anki_utils
import re
import matplotlib.pyplot as plt
import itertools
import add_pinyin

BOOK_PATH = r"c:\work\GitRoot\learn_chinese\data\小熊宝宝_5_大声回答哎.txt"
CARD_PATH = BOOK_PATH.replace(".txt", ".new_word.txt").replace("\data\\", "\output\\")
N_WORD_TO_LEARN = 5000

col = anki_utils.get_col()
ids = anki_utils.get_all_cards()

learnt_single_char_set = set(anki_utils.get_single_chars())
learnt_single_char_set = learnt_single_char_set.union(
    set(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
         '—', '“', '”', '…', '、', '《', '》', '！', '，', '：', '；', '？', '。']))

words = anki_utils.get_words(anki_utils.get_content(BOOK_PATH))

import pandas as pd
se = pd.Series([c for c in "".join(words)])
char_freq_se = se.value_counts()

unknown_chars = []
for ch in char_freq_se.index:
    if ch not in learnt_single_char_set:
        unknown_chars.append(ch)

print("len(unknown_chars):%s" % len(unknown_chars))
char_list, new_readable_words_list, n_new_readable_word_list, n_readable_word_list, readable_word_ratio_list = anki_utils.calc_learnt_char_vs_readable_unit(
    char_freq_se,
    learnt_single_char_set,
    words)

plt.plot(n_readable_word_list)

with open(CARD_PATH, "w", encoding="utf-8") as out_f:
    for char, words in itertools.islice(zip(char_list, new_readable_words_list), N_WORD_TO_LEARN):
        pinyin_s = add_pinyin.get_pinyin(char)
        out_f.write("%s\t\t%s\n" % (char, pinyin_s))
        for word in words:
            if len(word) > 1:
                pinyin_s = add_pinyin.get_pinyin(word)
                out_f.write("%s\t\t%s\n" % (word, pinyin_s))

anki_utils.close_col(col)

