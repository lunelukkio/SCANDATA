class Base():
    def __init__(self):
        self.obj = Product()
        self.obj = Product()

class Product():
    num = 0
    def __init__(self):
        Product.num += 1
        print(Product.num)
    
if __name__ == '__main__':
    test1 = Base()
    test2 = Base()
    
# これをインスタンスごとに独立にnumを増やしたい
# Productを改変して、結果が1234 ではなく1212となるようにしたい