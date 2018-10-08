import sys

sys.path.append(r"C:\work\GitRoot\python-pinyin")

from pypinyin import pinyin, lazy_pinyin, Style


with open(r"C:\temp\Chinese_with_pinyin.txt", "w", encoding="utf-8") as out_f:
    for line in open(r"C:\temp\Chinese.txt", encoding="utf-8"):
        word, meaning, pinyin_s = line.strip("\n").split("\t")
        pinyin_s = " ".join(char_pinyin[0] for char_pinyin in pinyin(word, style=Style.TONE3))
        out_f.write("%s\t%s\t%s\n" % (word, meaning, pinyin_s))

