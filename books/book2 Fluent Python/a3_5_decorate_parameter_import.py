from a3_5_decorate_parameter import register, registry, f1, f2, f3

# running register(active=False)->decorate(<function f1 at 0x000002B454CCB400>)
# running register(active=True)->decorate(<function f2 at 0x000002B454CCB488>)

print(registry)
# {<function f2 at 0x000001EF0F53B488>}

register()(f3)
# running register(active=True)->decorate(<function f3 at 0x00000254B782B378>)
print(registry)
# {<function f2 at 0x000001E6ADD3B488>, <function f3 at 0x000001E6ADD3B378>}

register(active=False)(f2)
# running register(active=False)->decorate(<function f2 at 0x000001EA98F7B488>)
print(registry)
# {<function f3 at 0x000001FC890BB378>}