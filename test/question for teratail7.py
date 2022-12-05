# weakref.WeakSetを使う場合
from weakref import WeakSet

class Base():
    def __init__(self):
        self.obj = []
        self.obj_name = []
        self.obj_dict = WeakSet()
        self.count = 0
        
    def create_product(self):
        product = Product(self)
        name = product.__class__.__name__
        
        self.obj.append(product)
        self.obj_name.append(name + str(self.count))
        self.obj_dict = dict(zip(self.obj_name, self.obj))
        

class Product():
    def __init__(self, base):
        self.base = base
        self.base.count  += 1
        print(self.base.count)

    def print_num(self):
        print('Product number = ' + str(self.base.count))
    
if __name__ == '__main__':
    test1 = Base()
    test2 = Base()
    
    test1.create_product()
    test2.create_product()
    test1.create_product()
    
    print(test1.obj_dict)
    print(test2.obj_dict)
    test1.obj_dict['Product1'].print_num()