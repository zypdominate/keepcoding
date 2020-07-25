import re
import collections

word_re = re.compile(r'\w+')
index_dict = collections.defaultdict(list)

with open('test.py', encoding='utf-8') as f:
    for line_index, line in enumerate(f, 1):
        print(line)
        for match_obj in word_re.finditer(line):
            print(match_obj)
            word = match_obj.group()
            column_index = match_obj.start() + 1
            location_tup = (line_index, column_index)
            index_dict[word].append(location_tup)

# 以字母顺序打印出结果
for word in sorted(index_dict, key=str.upper):
    print(word, index_dict[word])
