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

    print('Controller roiのobseverの名前列記printのリストにアペンド仕方が分からなかった')
    print('フルオトレースは３つでひとまとめのクラスを作る。イメージも。viewでゲットする必要があるのかチェック')
    print('Tip Roiの名前の問題 roiのオブザーバーの名前表示がおかしい')
    print('Tip リファクタリング data の名前をインスタンス変数に固定')
    print('back ground compの引き算がおかしい。まずノーマライズする必要がある')
    print('Trace のちゃんねるがおかしい、ROIとも結びついてない')
    
    print('viewで呼び出したオブジェクトはgetしなくても自動的にsetしてあげれば自動的に更新されている？　要チェック！！！！！')
    print('Tip TraceData __sub__の実装＞バックグランドを減算する為')
    print('Tip dF/F などのモッド実装')
    print('Tip Builderのcreate_dataのリファクタリングが必要。state メソッド使用？')
    
    print('Tip 右クリックでロ位変更実装')
    print('Tip difference imageの実装.そしてvalue objectのsub実装')

    print('Tip tkinterの見た目をよくする。imageが小さい')
    print('Tip view_mainのツリー構造実装')
    
    print('Tip Filename and WholeFilename should be sapaated because of isolation.')

