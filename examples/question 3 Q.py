from abc import ABCMeta, abstractmethod
import pprint

class Main():
    def __init__(self):
        self.obj = []  # productのオブジェクトリスト
        self.obj_name = []  # productの名前リスト
        self.obj_dict = {}  # productの辞書
            
    def create_obj(self, factory_type):
        product = factory_type.create_product()  # productのインスタンス作成
        object_name = product.__class__.__name__  # productのクラス名
        num_product = product.num  # productの作成回数
        
        self.obj.append(product)  # オブジェクトリストの追加
        self.obj_name.append(object_name + str(num_product))  # 名前（クラス名＋作成番号）リストの追加
        self.obj_dict = dict(zip(self.obj_name, self.obj))  # クラス名とオブジェクトのバインド
        
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
    num = 0  # インスタンス作成回数
    def __init__(self):
        FirstProduct.num += 1

    def print_name(self):
        print('First Product　' + str(FirstProduct.num))
        
class SecondProduct(Product):  # concrete product
    num = 0  # インスタンス作成回数
    def __init__(self):
        SecondProduct.num += 1

    def print_name(self):
        print('Second Product　' + str(FirstProduct.num))

if __name__ == '__main__':
    test_1 = Main()  # 一つ目のMainオブジェクト
    test_1.create_obj(FirstFactory())
    test_1.create_obj(SecondFactory())
    
    test_2 = Main()  # 二つ目のMainオブジェクト
    test_2.create_obj(FirstFactory())
    test_2.create_obj(SecondFactory())
    
    pprint.pprint(test_1.obj_dict)
    print()
    pprint.pprint(test_2.obj_dict)
    print()
    
    test_1.print_name('FirstProduct1')
    test_1.print_name('SecondProduct1')
    test_2.print_name('FirstProduct2')
    test_2.print_name('SecondProduct2')

    
    # 辞書のキーをMainのインスタンス(test_1,test_2)ごとに１から始めたい
    
    # 結果を
    #First Product 1
    #Second Product 1
    #First Product 1
    #Second Product 1
    #にしたい