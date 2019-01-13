import sys
import pinyin_utils

def fill_pinyin_slot(input_card_fn, output_card_fn):
    with open(output_card_fn, "w", encoding="utf-8") as out_f:
        for line in open(input_card_fn, encoding="utf-8"):
            word, meaning, pinyin_s = line.strip("\n").split("\t")
            pinyin_s = pinyin_utils.get_pinyin(word)
            out_f.write("%s\t%s\t%s\n" % (word, meaning, pinyin_s))

if __name__ == "__main__":
    fill_pinyin_slot(r"C:\temp\Chinese.txt", r"C:\temp\Chinese_with_pinyin.txt")