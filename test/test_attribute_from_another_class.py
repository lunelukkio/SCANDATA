# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 17:59:54 2022

lunelukkio@gmail.com
インスタンスへの関連付け
from https://teratail.com/questions/92605
"""

class Another():
    pass

class A(Another):
    def __init__(self):
        self.Coke = "コカ・コーラを飲もうよ"

class B(Another):
    def __init__(self, a: A):   #Aは関数アノテーション　”Aを受け取るべき”　引数はカッコ内に”：”　戻り値はかっこ外に”->”
        self.Coke = a.Coke

    def testB(self):
        print(self.Coke)

def main():
    a = A()
    b = B(a)
    b.testB()

if __name__ == '__main__':
    main()

"""実行結果
コカ・コーラを飲もうよ
"""