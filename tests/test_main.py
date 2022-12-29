# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 10:47:47 2022

lunelukkio@gmail.com
"""
import unittest


def suite():
    test_suite = unittest.TestSuite()
    all_test_suite = unittest.defaultTestLoader.discover(".", pattern="test0*.py")
    print(all_test_suite)
    for ts in all_test_suite:
        test_suite.addTest(ts)
    return test_suite




if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)
  #print(unittest.TestResult(test_suite))

