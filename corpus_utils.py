import jieba
import re
def get_content(book_path):
    content = open(book_path).read()
    content = content.replace("\n", "")
    return content

def get_sents(content):
    sents = [sent.strip() for sent in re.split(u'\n|。|！ ', content) if sent.strip() != ""]
    return  sents

def get_words(content):
    return list(jieba.cut(content))

