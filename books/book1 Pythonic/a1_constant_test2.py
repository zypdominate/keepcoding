dir()
# ['__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__']


import sys
import a1_constant_testmodule

dir()
# ['__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__',
#   'sys', 'a1_constant_testmodule']

assert 'a1_constant_testmodule' in sys.modules.keys()

assert id(a1_constant_testmodule) == id(sys.modules['a1_constant_testmodule'])

dir(a1_constant_testmodule)
# ['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'a', 'b']