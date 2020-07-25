registry = set()

def register(active=True):
    def decorate(func):
        print(f'running register(active={active})->decorate({func})')
        if active:
            registry.add(func)
        else:
            registry.discard(func)
        return func
    return decorate


@register(active=False)
def f1():
    print('running f1()')

@register()
def f2():
    print('running f2()')

def f3():
    print('running f3()')

if __name__ == '__main__':
    print(f'registry:{registry}')
    f1()
    f2()
    f3()
    print(f'registry:{registry}')

