class LookingGlass():
    def __enter__(self):
        import sys
        self.origin_write = sys.stdout.write
        sys.stdout.write = self.reverse_write
        return "reversed word -> drow desrever"

    def reverse_write(self, context):
        self.origin_write(context[::-1])

    def __exit__(self, exc_type, exc_val, exc_tb):
        import sys
        sys.stdout.write = self.origin_write
        if exc_type is ZeroDivisionError:
            print("do not divide by zero")
            return True


with LookingGlass() as look:
    print("I'm looking sth.")
    print(look)

manager = LookingGlass()
print(manager)
content = manager.__enter__()
print("12345")
print(manager)
print(content)

