### 覆盖型与非覆盖型描述符对比

Python**存取属性**的方式特别不对等。**通过实例读取属性时，通常返回的是实例中定义的属性；但是，如果实例中没有指定的属性，那么会获取类属性。而为实例中的属性赋值时，通常会在实例中创建属性，根本不影响类。**

这种不对等的处理方式对描述符也有影响。其实，根据是否定义 `__set__` 方法，描述符可分为两大类。若想观察这两类描述符的行为差异，则需要使用几个类。

```python
def cls_name(obj_or_cls):
    cls = type(obj_or_cls)
    print(cls)
    if cls is type:
        cls = obj_or_cls
    return cls.__name__.split('.')[-1]


def display(obj):
    cls = type(obj)
    if cls is type:
        return f'<class {obj.__name__}>'
    elif cls in [type(None), int]:
        return repr(obj)
    else:
        return f'<{cls_name(obj)} object>'


def print_args(name, *args):
    pseudo_args = ','.join(display(x) for x in args)
    print(f'-> {cls_name(args[0])}.__{name}__{pseudo_args}')


class Overriding:
    """数据描述符/强制描述符"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class OverridingNoGet:
    """没有__get__方法的覆盖型描述符"""

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class NonOverriding:
    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)


class Managed:
    # 托管类：使用各个描述符的一个实例
    over = Overriding()
    over_no_get = OverridingNoGet()
    non_over = NonOverriding()

    def spam(self):
        # spam方法放在这里是为了对比，因为方法也是描述符。
        print(f'-> Managed.spam({display(self)})')
```

---

#### 1. 覆盖型描述符

实现 `__set__` 方法的描述符属于**覆盖型描述符**，因为虽然描述符是类属性，但是实现`__set__`方法的话，会覆盖对实例属性的赋值操作。

特性也是覆盖型描述符：如果没提供设值函数，property 类中的 `__set__` 方法会抛出 AttributeError 异常，指明那个属性是只读的。

```python
obj = Managed()
obj.over
# -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)
# obj.over触发描述符的__get__方法，第二个参数的值是托管实例obj。

Managed.over
# -> Overriding.__get__(<Overriding object>, None, <class Managed>)
# Managed.over触发描述符的__get__方法，第二个参数（instance）的值是None。

obj.over = 1
# -> Overriding.__set__(<Overriding object>, <Managed object>, 1)
# 为obj.over赋值，触发描述符的__set__方法，最后一个参数的值是1。

obj.over
# -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)
# 读取obj.over，仍会触发描述符的__get__方法。

obj.__dict__['over'] = 8
# 跳过描述符，直接通过obj.__dict__属性设值。

print(vars(obj))
# {'over': 8}
# 确认值在obj.__dict__属性中，在over键名下。

obj.over
# -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)
# 即使是名为over的实例属性，Managed.over描述符仍会覆盖读取obj.over这个操作。
```

---

#### 2. 没有__get__方法的覆盖型描述符

通常，覆盖型描述符既会实现 `__set__` 方法，也会实现 `__get__` 方法，不过也可以只实现 `__set__` 方法。

此时，只有写操作由描述符处理。通过实例读取描述符会返回描述符对象本身，因为没有处理读操作的 `__get__`方法。如果直接通过实例的 `__dict__` 属性创建同名实例属性，以后再设置那个属性时，仍会由 `__set__`方法插手接管，但是读取那个属性的话，就会直接从实例中返回新赋予的值，而不会返回描述符对象。也就是说，**实例属性会遮盖描述符，不过只有读操作是如此**。

```python
obj = Managed()
print(obj.over_no_get)
# <__main__.OverridingNoGet object at 0x000001E072A18BA8>
# 这个覆盖型描述符没有__get__方法，因此，obj.over_no_get从类中获取描述符实例。

print(Managed.over_no_get)
# <__main__.OverridingNoGet object at 0x000001E072A18BA8>

obj.over_no_get = 1
# -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 1)
# 为obj.over_no_get赋值会触发描述符的__set__方法。

print(obj.over_no_get)
# <__main__.OverridingNoGet object at 0x000001E072A18BA8>
# 因为__set__方法没有修改属性，所以在此读取obj.over_no_get获取的仍是托管类中的描述符实例。

obj.__dict__['over_no_get'] = 2
print(obj.over_no_get)  # 2
# 通过实例的__dict__属性设置名为over_no_get的实例属性。

obj.over_no_get = 3
# -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 3)
#  为obj.over_no_get赋值，仍然经过描述符的__set__方法处理。

print(obj.over_no_get)  # 2
# 但是读取时，只要有同名的实例属性，描述符就会被遮盖。
```

---

#### 3. 非覆盖型描述符

没有实现 `__set__` 方法的描述符是非覆盖型描述符。如果设置了同名的实例属性，描述符会被遮盖，致使描述符无法处理那个实例的那个属性。方法是以非覆盖型描述符实现的。

```python
obj = Managed()
obj.non_over
# -> NonOverriding.__get__(<NonOverriding object>, <Managed object>, <class Managed>)
# obj.non_over触发描述符的__get__方法，第二个参数的值是obj。

obj.non_over = 1
# Managed.non_over是非覆盖型描述符，因此没有干涉赋值操作的__set__方法。

print(obj.non_over)  # 1
# obj有个名为non_over的实例属性，把Managed类的同名描述符属性遮盖掉。

Managed.non_over
# -> NonOverriding.__get__(<NonOverriding object>, None, <class Managed>)
# Managed.non_over描述符依然存在，会通过类截获这次访问。

del obj.non_over
obj.non_over
# -> NonOverriding.__get__(<NonOverriding object>, <Managed object>, <class Managed>)
# 如果把non_over实例属性删除了，那么，读取obj.non_over时，会触发类中描述符的__get__方法；
# 但要注意，第二个参数的值是托管实例。
```

---

#### 4. 在类中覆盖描述符

不管描述符是不是覆盖型，为类属性赋值都能覆盖描述符。这是一种猴子补丁技术。

```python
Managed.over = 1
Managed.over_no_get = 2
Managed.non_over = 3
print(obj.over, obj.over_no_get, obj.non_over)
# 1 2 3
```

读写属性的另一种不对等：读类属性的操作可以由依附在托管类上定义有 `__get__`方法的描述符处理，但是写类属性的操作不会由依附在托管类上定义有 `__set__` 方法的描述符处理。

---

#### 5. 方法是描述符

在类中定义的函数属于绑定方法（bound method），因为用户定义的函数都有 `__get__` 方法，所以依附到类上时，就相当于描述符。

```python
print(obj.spam)
# <bound method Managed.spam of <__main__.Managed object at 0x000001C5275EBC50>>
# obj.spam获取的是绑定方法对象。

print(Managed.spam)
# <function Managed.spam at 0x000001C52761E6A8>
# 但是Managed.spam获取的是函数。

obj.spam = 1
print(obj.spam)  # 1
# 如果为obj.spam赋值，会遮盖类属性，导致无法通过obj实例访问spam方法。
```

函数没有实现 `__set__` 方法，因此是非覆盖型描述符。

obj.spam 和 Managed.spam 获取的是不同的对象。与描述符一样，通过托管类访问时，函数的 `__get__` 方法会返回自身的引用。但是，通过实例访问时，函数的 `__get__` 方法返回的是绑定方法对象：一种可调用的对象，里面包装着函数，并把托管实例（例如obj）绑定给函数的第一个参数（即self），这与functools.partial函数的行为一致。

---

#### 6. 描述符用法建议

**1. 使用特性以保持简单：**

内置的property类创建的其实是覆盖型描述符，`__set__` 方法和 `__get__` 方法都实现了，即便不定义设值方法也是如此。特性的 `__set__` 方法默认抛出AttributeError: can't set attribute，因此创建只读属性最简单的方式是使用特性，这能避免下一条所述的问题。

**2.只读描述符必须有`__set__`方法：**

如果使用描述符类实现只读属性，要记住，`__get__` 和 `__set__` 两个方法必须都定义，否则，实例的同名属性会遮盖描述符。只读属性的 `__set__` 方法只需抛出AttributeError异常，并提供合适的错误消息。 

**3.用于验证的描述符可以只有`__set__`方法：**

对仅用于验证的描述符来说，`__set__` 方法应该检查 value 参数获得的值，如果有效，使用描述符实例的名称为键，直接在实例的 `__dict__` 属性中设置。这样，从实例中读取同名属性的速度很快，因为不用经过 `__get__` 方法处理。 

**4.仅有`__get__`方法的描述符可以实现高效缓存：**

如果只编写了`__get__`方法，那么创建的是非覆盖型描述符。这种描述符可用于执行某些耗费资源的计算，然后为实例设置同名属性，缓存结果。同名实例属性会遮盖描述符，因此后续访问会直接从实例的 `__dict__` 属性中获取值，而不会再触发描述符的 `__get__` 方法。

**5.非特殊的方法可以被实例属性遮盖：**

由于函数和方法只实现了`__get__` 方法，它们不会处理同名实例属性的赋值操作。因此，像`my_obj.the_method=7`这样简单赋值之后，后续通过该实例访问 the_method 得到的是数字7——但是不影响类或其他实例。然而，特殊方法不受这个问题的影响。解释器只会在类中寻找特殊的方法，也就是说，repr(x)执行的其实是 `x.__class__.__repr__(x)`，因此x的 `__repr__`属性对repr(x)方法调用没有影响。出于同样的原因，实例的 `__getattr__` 属性不会破坏常规的属性访问规则。