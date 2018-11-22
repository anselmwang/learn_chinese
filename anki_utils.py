import sys
sys.path.append(r"C:\work\GitRoot\anki")

from anki import Collection
import collections
import re
import jieba

def get_all_cards():
    #ids = col.findCards(u"deck:'Chinese::第一册'")
    ids = col.findCards(u"deck:'Chinese'")
    return ids

def is_single_char(s):
    return len(s) == 1

def get_front(card):
    note = card.note()
    return dict(note.items())["Front"]

# #(learning + due) equals the #(young + learn + mature) in UI
# #(new) == #(unseen) in UI
type_list = ["new", "learning", "due"]
def single_char_card_iterator():
    for id in get_all_cards():
        card = col.getCard(id)
        if is_single_char(get_front(card)):
            yield card

def get_single_chars():
    return [get_front(card) for card in single_char_card_iterator()]

def get_learnt_single_chars(ids):
    learnt_single_chars = []
    for card in single_char_card_iterator():
        if type_list[card.type] in ('learning', 'due'):
            learnt_single_chars.append(get_front(card))
    return learnt_single_chars

def single_char_stat(ids):
    stat = collections.defaultdict(int)
    for card in single_char_card_iterator():
            stat[type_list[card.type]] += 1
    return stat


COLLECTION_PATH = u'C:\\Users\\yuwan\\AppData\\Roaming\\Anki2\\Yu Wang\\collection.anki2'
# don't worry about another app is using it.
# If using it, an exception "sqlite3.OperationalError: database is locked" will be throw out.

col = Collection(COLLECTION_PATH, log=True)
def get_col():
    return col

def close_col(col):
    col.close()


BOOK1_PATH = r"c:\work\GitRoot\learn_chinese\data\舒克贝塔历险记.TXT"
def get_content(book_path):
    content = open(book_path).read()
    content = content.replace("\n", "")
    return content

def get_sents(content):
    sents = [sent.strip() for sent in re.split(u'\n|。|！ ', content) if sent.strip() != ""]
    return  sents

def get_words(content):
    return list(jieba.cut(content))

def get_readable_units(units, learnt_single_char_set):
    readable_units = []
    for unit in units:
        new_chars = [c for c in unit if c not in learnt_single_char_set]
        n_new = len(new_chars)
        n_ratio = float(n_new) / len(unit)
        if n_new == 0:
            readable_units.append(unit)
    return readable_units



def calc_learnt_char_vs_readable_unit(char_freq_se, learnt_single_char_set, units):
    readable_units = get_readable_units(units, learnt_single_char_set)
    n_readable_unit = len(readable_units)
    readable_unit_ratio = n_readable_unit / float(len(units)) * 100
    print("initial readable units: %s (%.2f%%)", (n_readable_unit, readable_unit_ratio))

    old_readable_unit_set = set(readable_units)
    n_new_learn = 0
    n_readable_unit_list = []
    readable_unit_ratio_list = []
    n_new_readable_unit_list = []

    char_list = []
    new_readable_units_list = []
    import copy
    learnt_single_char_set = copy.copy(learnt_single_char_set)
    for ch in char_freq_se.index:
        if ch not in learnt_single_char_set:
            learnt_single_char_set.add(ch)
            char_list.append(ch)
            n_new_learn += 1

            readable_units = get_readable_units(units, learnt_single_char_set)
            readable_unit_set = set(readable_units)
            new_readable_units_list.append(readable_unit_set - old_readable_unit_set)
            old_readable_unit_set = readable_unit_set

            n_readable_unit = len(readable_units)
            readable_unit_ratio = n_readable_unit / float(len(units)) * 100
            n_new_readable_unit = len(new_readable_units_list[-1])

            n_readable_unit_list.append(n_readable_unit)
            readable_unit_ratio_list.append(readable_unit_ratio)
            n_new_readable_unit_list.append(n_new_readable_unit)

            print("learned char: %s, readable units: %s (%.2f%%), current char %s (%s), freq: %s" %
                  (n_new_learn, n_readable_unit, readable_unit_ratio,
                   ch,
                   repr(ch),
                   char_freq_se.loc[ch])
                  )

    return char_list, new_readable_units_list, n_new_readable_unit_list, n_readable_unit_list, readable_unit_ratio_list
