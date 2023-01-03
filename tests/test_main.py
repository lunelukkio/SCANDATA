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
    #print(unittest.TestResult(test_suite))

    print('roiのwidth情報がほぞんされない')
    print('large roiをadd_dataで対処したがROIBOXがROI情報を受け取れない')
    print('ROIの問題は値ROIオブジェにｘ、ｙだけを渡せないー＞＊argsつかって値オブジェう表現')
    print('-->get dataでROIinforをgetできるようにする。　stateパターン？これによりROIBOXが直接roiデータを持ってこれる。')
    
    print('data_setのcreate_dataのリファクタリングが必要。state メソッド使用？')
    
    
    print('difference imageの実装')
    print('TraceData __sub__の実装＞バックグランドを減算する為')
    print('dF/F などのモッド実装')
    print('tkinterの見た目をよくする。imageが小さい')
    print('view_mainのツリー構造実装')
    
    print('Filename and WholeFilename should be sapaated because of isolation.')

