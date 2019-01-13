import re
import sys
sys.path.append(r"C:\work\GitRoot\python-pinyin")

from pypinyin import pinyin, lazy_pinyin, Style

def get_pinyin(word):
    pinyin_list = []
    for char_pinyin in pinyin(word, style=Style.TONE3):
        if char_pinyin[0][-1].isdigit():
            pinyin_list.append(char_pinyin[0])
        else:
            pinyin_list.append(char_pinyin[0] + "5")
    pinyin_s = " ".join(pinyin_list)
    return pinyin_s


PINYIN_MAPPING = {'ā': ('a', 1),
                  'á': ('a', 2),
                  'ǎ': ('a', 3),
                  'à': ('a', 4),

                  'ē': ('e', 1),
                  'é': ('e', 2),
                  'ě': ('e', 3),
                  'è': ('e', 4),

                  'ī': ('i', 1),
                  'í': ('i', 2),
                  'ǐ': ('i', 3),
                  'ì': ('i', 4),

                  'ō': ('o', 1),
                  'ó': ('o', 2),
                  'ǒ': ('o', 3),
                  'ò': ('o', 4),

                  'ū': ('u', 1),
                  'ú': ('u', 2),
                  'ǔ': ('u', 3),
                  'ù': ('u', 4),

                  'ü': ('v', None),
                  'ǘ': ('v', 2),
                  'ǚ': ('v', 3),
                  'ǜ': ('v', 4),
                  }


STANDARD_PINYIN_RE = re.compile("^[a-z1-5]+$")

def is_standard_pinyin(pinyin):
    return STANDARD_PINYIN_RE.match(pinyin) is not None

def standardize_pinyin(pinyin):
    new_pinyin = []
    tone = 5
    for c in pinyin:
        tmp_c, tmp_tone = PINYIN_MAPPING.get(c, (c, None))
        new_pinyin.append(tmp_c)
        if tmp_tone is not None:
            tone = tmp_tone
    new_pinyin = "".join(new_pinyin) + str(tone)
    assert is_standard_pinyin(new_pinyin), "%s %s" % (new_pinyin, pinyin)
    return  new_pinyin


SHENG_MU_LIST = "b p m f d t n l g k h j q x zh ch sh r z c s y".split(" ")
SHENG_MU_LIST = sorted(SHENG_MU_LIST, key=lambda x: len(x), reverse=True)
YUN_MU_LIST = "a ai an ang ao e ei en eng er i ia ian iang iao ie in ing iong iu o ong ou u ua uai uan uang ue ueng ui un uo v van ve vn üe".split(" ")
YUN_MU_LIST = sorted(YUN_MU_LIST, key=lambda x: len(x), reverse=True)
MORE_YUN_MU_LIST = []

import collections
simple_2_complex_dic = collections.defaultdict(list)
for complex, (simple, _) in PINYIN_MAPPING.items():
    simple_2_complex_dic[simple].append(complex)
for yun_mu in YUN_MU_LIST:
    for simple, complex_list in simple_2_complex_dic.items():
        if simple in yun_mu:
            MORE_YUN_MU_LIST.extend([yun_mu.replace(simple, complex) for complex in complex_list + [simple]])


PINYIN_RE = re.compile("(" + "|".join(SHENG_MU_LIST) + ")?" + "(" + "|".join(MORE_YUN_MU_LIST) + ")")

def split_pinyin(s):
    return [m.group() for m in PINYIN_RE.finditer(s)]


