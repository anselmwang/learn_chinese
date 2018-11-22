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

def fill_pinyin_slot(input_card_fn, output_card_fn):
    with open(output_card_fn, "w", encoding="utf-8") as out_f:
        for line in open(input_card_fn, encoding="utf-8"):
            word, meaning, pinyin_s = line.strip("\n").split("\t")
            pinyin_s = get_pinyin(word)
            out_f.write("%s\t%s\t%s\n" % (word, meaning, pinyin_s))

if __name__ == "__main__":
    fill_pinyin_slot(r"C:\temp\Chinese.txt", r"C:\temp\Chinese_with_pinyin.txt")