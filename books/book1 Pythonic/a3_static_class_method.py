class A(object):
    def instance_method(self, var):
        print(f'instance_method: {self},{var}')

    @classmethod
    def class_method(cls, var):
        print(f'class_method:{cls},{var}')

    @staticmethod
    def static_method(var):
        print(f'static_method:{var}')

obj_a = A()
obj_a.instance_method('instance_method')
obj_a.class_method('class_method')
obj_a.static_method('static_method')