import re
import pinyin_utils

class ChineseChar:
    def __init__(self, char, pinyin):
        self.char = char
        self.pinyin = pinyin


def build_junior_school_unfamiliar_chars():
    LINE_RE = re.compile(r"(.*\d+、)(.*)$")
    SEG_RE = re.compile(r"(.)\((.*)\)")
    JUNIOR_SCHOOL_UNFAMILIAR_CHARS = []
    for line in open(r"C:\work\GitRoot\learn_chinese\data\小学生字表.txt"):
        m = LINE_RE.match(line)
        if m is not None:
            for seg in m.group(2).strip().split(" "):
                if seg != "":
                    seg_match = SEG_RE.match(seg)
                    char, pinyin = seg_match.group(1), seg_match.group(2)
                    pinyin = pinyin_utils.standardize_pinyin(pinyin)
                    JUNIOR_SCHOOL_UNFAMILIAR_CHARS.append(ChineseChar(char, pinyin))

    return JUNIOR_SCHOOL_UNFAMILIAR_CHARS

