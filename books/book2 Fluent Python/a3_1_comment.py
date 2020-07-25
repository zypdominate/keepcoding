def clip(text: str, max_len: 'int > 0' = 8) -> str:  # 有注解的函数声明
    """
    在max_len前面或后面的第一个空格处截断文本
    """
    end = None
    space_before = space_after = ''
    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)
        print(space_before)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
            print(space_after)
            if space_after >= 0:
                end = space_after
    if end is None:  # 没找到空格
        end = len(text)
    return text[:end].rstrip()


print(clip("1adsfd2sdfjkl 3dsfa 4jskldf"))
print(clip.__annotations__)
'''
1adsfd2sdfjkl 3dsfa
{'text': <class 'str'>, 'max_len': 'int > 0', 'return': <class 'str'>}
'''
