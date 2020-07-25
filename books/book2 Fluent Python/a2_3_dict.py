import sys
import re

word_re = re.compile(r'\w+')

index = {}
# with open(sys.argv[1], encoding='utf-8') as f:
with open('test.py', encoding='utf-8') as f:
    for line_index, line in enumerate(f, 1):
        print(line)
        for match_obj in word_re.finditer(line):
            print(match_obj)
            word = match_obj.group()
            column_index = match_obj.start() + 1
            location_tup = (line_index, column_index)
            # word_list = index.get(word,[])
            # word_list.append(location_tup)
            # index[word] =word_list

            # 获取单词的出现情况列表，如果单词不存在，把单词和一个空列表放进映射，
            # 然后返回这个空列表，这样就能在不进行第二次查找的情况下更新列表了。
            index.setdefault(word, []).append(location_tup)

# 以字母顺序打印出结果
for word in sorted(index, key=str.upper):
    print(word, index[word])
