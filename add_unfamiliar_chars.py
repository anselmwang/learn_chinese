import corpus_utils
import common
import nltk
import collections
import data_utils
import anki_utils
import pinyin_utils

import glob

def load_char_2_word_cnt_pairs_dic():
    full_words = []
    for path in glob.glob(r"C:\work\GitRoot\learn_chinese\data\corpus\*"):
        content = corpus_utils.get_content(path)
        words = corpus_utils.get_words(content)
        words = [word for word in words if word not in common.SPECIAL_CHAR_SET and len(word) > 1]
        full_words.extend(words)

    dist = nltk.FreqDist(full_words)

    char_2_word_cnt_pairs_dic = collections.defaultdict(list)
    for word, cnt in dist.most_common(len(dist)):
        for char in word:
            char_2_word_cnt_pairs_dic[char].append((word, cnt))
    return char_2_word_cnt_pairs_dic

def get_candidate_words(char, known_char_set, n_candidate = 2):
    candidate_words = []
    for word, cnt in char_2_word_cnt_pairs_dic[char]:
        if all([c == char or c in known_char_set for c in word]):
            if len(candidate_words) < n_candidate:
                candidate_words.append((word, pinyin_utils.get_pinyin(word)))
    return candidate_words


char_2_word_cnt_pairs_dic = load_char_2_word_cnt_pairs_dic()

added_single_char_set = set(char for char in anki_utils.get_single_chars())
junior_school_unfamiliar_chars = data_utils.build_junior_school_unfamiliar_chars()
unfamiliar_chars = [char for char in junior_school_unfamiliar_chars if char.char not in added_single_char_set]
unfamiliar_char_set = set([char.char for char in unfamiliar_chars])
unfamiliar_char_2_pinyin_dict = {char.char:char.pinyin for char in unfamiliar_chars}



cards = []
for unfamiliar_char in unfamiliar_chars:
    if unfamiliar_char.char in added_single_char_set:
        continue
    candidate_words = get_candidate_words(unfamiliar_char.char, added_single_char_set)
    if len(candidate_words) != 0:
        cards.append((unfamiliar_char.char, unfamiliar_char.pinyin))
        added_single_char_set.add(unfamiliar_char.char)
        cards.extend(candidate_words)
    else:
        candidate_words = get_candidate_words(unfamiliar_char.char, added_single_char_set.union(unfamiliar_char_set))
        for c in set("".join(word for word, pinyin in candidate_words)):
            if c in added_single_char_set:
                continue
            cards.append((c, unfamiliar_char_2_pinyin_dict[c]))
            added_single_char_set.add(c)
        cards.extend(candidate_words)

not_added_set = unfamiliar_char_set - set([word for word, pinyin in cards if len(word) == 1])
print(len(not_added_set)) # 26
print(len(cards))

with open(r"C:\work\GitRoot\learn_chinese\data\小学新字_20190112.txt", "w", encoding="utf-8") as out_f:
    for word, pinyin in cards:
        out_f.write("%s\t%s\t%s\n" % (word, "", pinyin))
