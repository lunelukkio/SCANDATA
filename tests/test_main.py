# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 10:47:47 2022

lunelukkio@gmail.com
"""
import unittest


def suite():
    test_suite = unittest.TestSuite()
    
    #test_classes = "test*.py"   # test*.py    for all tests
    test_classes = "test0*.py"  #   for model
    #test_classes = "test1*.py"  # test1*py    for view
    #test_classes = "test2*.py"  # test2*.py    for controller

    
    all_test_suite = unittest.defaultTestLoader.discover(".", pattern=test_classes)
    print(all_test_suite)
    for ts in all_test_suite:
        test_suite.addTest(ts)
    return test_suite



if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)

    print('Model は データフィルごとに新たに作る。それをコントローラーが保持する')
    print('delete_entityの辞書delの使い方')
    print('roival取得とroiboxの番号を一致させておくことでバインドさせる　roibox(i) = get roival(i)')

    print('ファサード使ってbuilderのシンプル化')
    
    print('現状ではaxesが一つのroiviewのtraceの数しか持てないので、複数のRoiViewのtraceを全部持てるようにする')
    
    print('modではvalue objectを変換してinterfaceへおくる')
    

    print('Controller roiのobseverの名前列記printのリストにアペンド仕方が分からなかった')


    print(' リファクタリング data の名前をインスタンス変数に固定')
    print('back ground compの引き算がおかしい。まずノーマライズする必要がある')
    
    print('viewで呼び出したオブジェクトはgetしなくても自動的にsetしてあげれば自動的に更新されている？　要チェック！！！！！')
    print(' dF/F などのモッド実装')

    print(' tkinterの見た目をよくする。imageが小さい')
    print('view_mainのツリー構造実装')
    
    print('view class　と button functionの作り直し')
    
    print(' Filename and WholeFilename should be saparated because of isolation.')

