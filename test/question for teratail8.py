import inspect

class Base():
    def __init__(self):
        self.obj = Product()
        self.obj = Product()

class Product():
    def __init__(self):
        print(inspect.stack()[2])
        base = inspect.stack()[1].frame.f_locals['self']
        base.num = getattr(base, 'num', 0)
        base.num += 1
        print(base.num)
    
if __name__ == '__main__':
    test1 = Base()
    test2 = Base()

# 1
# 2
# 1
# 2