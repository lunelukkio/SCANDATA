# weakref.WeakSet


from weakref import WeakSet

class Base:
    def __init__(self):
        self._counter = WeakSet() # 生存しているオブジェクトのみを数える場合
        self._total = 0 # 累計の生成数をカウントしたい場合

        self.obj = self.createProduct()
        self.obj = self.createProduct() # この時点で前に生成した self.obj は破棄される

    def createProduct(self, *args, **kw):
        obj = Product(*args, **kw)
        self._counter.add(obj)
        self._total += 1
        return obj

    @property
    def total(self):
        return self._total

    @property
    def count(self):
        return len(self._counter)

class Product:
    def __init__(self, num=0):
        self.num = num

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.num=}>"


if __name__ == "__main__":

    base  = Base()
    print(base.count) # 1

    obj = base.createProduct()
    print(base.count) # 2

    print(obj)
    del obj
    print(base.count) # 1
    
    print(base._counter)

    from functools import partial
    create10 = partial(base.createProduct, 10)
    obj = create10()
    print(obj)
    print(base.count) # 2