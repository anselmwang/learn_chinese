import itertools
import pinyin_utils
import re

# 我认为现代汉语词典的拼音错误更多
SPECIAL_CHARS = "’∥•…－"

WORD_RE = re.compile(r"^【(.*)】"+"((" + "|".join(pinyin_utils.PINYIN_MAPPING.keys()) +
                     "|" + "|".join(SPECIAL_CHARS) + "|[a-z]|ɡ|ɑ|α|1)+)")

INVALID_WORD_RE = re.compile("[a-z0-9，]")

word_2_pinyin_dic = {}
for line in open(r"C:\work\GitRoot\learn_chinese\data\现代汉语词典（第五版）全文_更新.txt", encoding="utf-8"):
    m = WORD_RE.match(line.lower())
    if m is not None:
        word = m.group(1)
        for c in SPECIAL_CHARS:
            word = word.replace(c, "")
        if INVALID_WORD_RE.search(word) is not None: # to skip "阿Q"
            #print(c)
            continue

        weird_pinyin = m.group(2).replace("ɡ", "g").replace("ɑ", "a").replace("1", "l").replace("α", "a")
        pinyin = []
        for char_pinyin in pinyin_utils.split_pinyin(weird_pinyin):
            pinyin.append(pinyin_utils.standardize_pinyin(char_pinyin))
        pinyin = " ".join(pinyin)

        word_2_pinyin_dic[word] = pinyin
        if pinyin.count(" ") != pinyin_utils.get_pinyin(word).count(" ") and "儿" not in word:
            print(word, pinyin, pinyin_utils.get_pinyin(word))
            print(m.group(1), weird_pinyin, pinyin_utils.split_pinyin(weird_pinyin))
            break


for word, pinyin in word_2_pinyin_dic.items():
    if pinyin != pinyin_utils.get_pinyin(word) and word not in \
            set(["吖", "阿尔法粒子", "阿伏伽德罗常量"]):
        print(word, "%s/%s" % (pinyin, pinyin_utils.get_pinyin(word)))









