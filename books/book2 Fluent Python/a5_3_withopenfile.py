with open("a5_3_with.py") as f:
    content = f.read(100)

print(f)  # fp 变量仍然可用
print(len(content))
print(f.closed, f.encoding)
print(content)
# f.read(10)
