
registry_list = []

def register(func):
    print(f'running register {func}')
    registry_list.append(func)
    return func

@register
def f1():
    print(f'running f1()')

@register
def f2():
    print(f'running f2()')

def f3():
    print(f'running f3()')

def main():
    print('running main()')
    print(f'registry_list:{registry_list}')
    f1()
    f2()
    f3()

if __name__ == '__main__':
    main()