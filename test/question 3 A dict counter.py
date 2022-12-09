from abc import ABCMeta, abstractmethod
import pprint

class Main():
    def __init__(self):
        self.counter_dict = {} 
        self.obj_dict = {}
            
    def create_obj(self, factory_type):
        product = factory_type.create_product()  # productのインスタンス作成
        object_name = product.__class__.__name__  # productのクラス名
        last_num = self.counter_dict.get(object_name, 0)
        new_num = last_num + 1
        product.num = new_num
        self.counter_dict[object_name] = new_num
        self.obj_dict[object_name + str(product.num)] = product
        
    def print_name(self, product):
        self.obj_dict[product].print_name()

class Factory(metaclass=ABCMeta):  # factory
    @abstractmethod
    def create_product(self):
        pass
    
class FirstFactory(Factory):  # concrete factory
    def create_product(self):
        return FirstProduct()
    
class SecondFactory(Factory):  # concrete factory
    def create_product(self):
        return SecondProduct()

class Product(metaclass=ABCMeta):  #product  
    @abstractmethod
    def print_name(self):
        pass

class FirstProduct(Product):  # concrete product
    def __init__(self):
        pass

    def print_name(self):
        print('First Product　' + str(self.num))
        
class SecondProduct(Product):  # concrete product
    def __init__(self):
        pass

    def print_name(self):
        print('Second Product　' + str(self.num))

if __name__ == '__main__':
    test_1 = Main()  # 一つ目のMainオブジェクト
    test_1.create_obj(FirstFactory())
    test_1.create_obj(SecondFactory())

    
    test_2 = Main()  # 二つ目のMainオブジェクト
    test_2.create_obj(FirstFactory())
    test_2.create_obj(SecondFactory())
    
    test_1.create_obj(SecondFactory())
    test_1.create_obj(FirstFactory())
    test_1.create_obj(SecondFactory())
    
    pprint.pprint(test_1.obj_dict)
    print()
    pprint.pprint(test_2.obj_dict)
    print()

    test_1.print_name('FirstProduct1')
    test_1.print_name('SecondProduct3')
    test_2.print_name('FirstProduct1')
    test_2.print_name('SecondProduct1')
