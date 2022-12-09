# inspectにより参照を取得する場合
import inspect

class Base():
    def __init__(self):
        self.obj = []
        self.obj_name = []
        self.obj_dict = {}
        
    def create_product(self):
        product = Product()
        name = product.__class__.__name__
        
        self.obj.append(product)
        self.obj_name.append(name + str(self.num))
        self.obj_dict = dict(zip(self.obj_name, self.obj))
        

class Product():
    def __init__(self):
        self.base = inspect.stack()[1].frame.f_locals['self']
        self.base.num = getattr(self.base, 'num', 0)
        self.base.num += 1
        print(self.base.num)

    def print_num(self):
        print('Product number = ' + str(self.base.num))
    
if __name__ == '__main__':
    test1 = Base()
    test2 = Base()
    
    test1.create_product()
    test2.create_product()
    test1.create_product()
    
    print(test1.obj_dict)
    print(test2.obj_dict)
    test1.obj_dict['Product2'].print_num()