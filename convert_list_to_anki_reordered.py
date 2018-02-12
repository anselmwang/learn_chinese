lines = None
with open(r"C:\temp\四五快读第五册.txt", "r", encoding="utf-8") as in_f:
    lines = in_f.readlines()

lines[0] = lines[0][1:]  # remove the BOM char

chars = []
word_set = set()
story_2_char_set_dic = {}
for line in lines:
    line = line.strip()
    if len(line) == 1:
        chars.append(line)
    elif "p" in line.lower():
        story_2_char_set_dic[line] = set(chars)
    else:
        word_set.add(line)

all_char_set = set(chars)
known_char_set = set()
reordered_note_list = []
# 找到本书所有的故事
# 对于每个字，找到所有可能认识的词语，添加在后面
# 找到所有故事，remove这个字，如果这个故事已经可以了，结束
for ch in chars:
    print(ch)
    reordered_note_list.append(ch)
    known_char_set.add(ch)
    words_to_be_append = []
    for word in word_set:
        if all([(word_char in known_char_set) or (word_char not in all_char_set)
                for word_char in word]):
            words_to_be_append.append(word)
    print(words_to_be_append)
    print(known_char_set)
    reordered_note_list.extend(words_to_be_append)
    word_set = word_set - set(words_to_be_append)

    stories_to_be_append = []
    for story in story_2_char_set_dic.keys():
        story_2_char_set_dic[story].remove(ch)
        if len(story_2_char_set_dic[story]) == 0:
            stories_to_be_append.append(story)
    reordered_note_list.extend(stories_to_be_append)
    for story in stories_to_be_append:
        del story_2_char_set_dic[story]

with open(r"C:\temp\四五快读第五册_reordered.txt", "w", encoding="utf-8") as out_f:
    for note in reordered_note_list:
        out_f.write("%s\t\n" % note)
