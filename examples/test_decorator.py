#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################
#   デコレータ (decorator)
###########################################
from functools import wraps

class my_decorator_base:
    def __init__( self, *args, **kwargs ):
        # func 引数の判定と引数の格納
        self._func = None
        self._args = []
        self._kwargs = {}
        if len(args) == 1 and callable(args[0]):
            # 引数なしのデコレータが呼び出された場合
            self._func = self._wrapper( args[0] )
        else:
            # 引数ありのデコレータが呼び出された場合
            self._args = args
            self._kwargs = kwargs

    def __call__( self, *args, **kwargs ):
        # func 引数の有無で判定
        if self._func is None:
            if len(args) == 1 and callable(args[0]):
                # 引数ありのデコレータが呼び出された場合
                self._func = self._wrapper( args[0] )
                return self._func
        else:
            # 引数なしのデコレータが呼び出された場合
            try:
                ret = self._func( *args, **kwargs )
            except:
                raise
            return ret

    def _wrapper( self, func ):
        # _wrapper() はサブクラスで実装する
        @wraps
        def wrapper_f( *args, **kwargs ):
            return func( *args, **kwargs )
        return wrapper_f


class my_decorator(my_decorator_base):
    """
    for doctest

    >>> @my_decorator
    ... def f1( arg1 ):
    ...     print( arg1 )
    ...
    >>> @my_decorator('mytest1')
    ... def f2( arg2 ):
    ...     print( arg2 )
    ...
    >>> @my_decorator
    ... def f3( arg1 ):
    ...     print( arg1 )
    ...     a = 1/0
    ...
    >>> @my_decorator('mytest2')
    ... def f4( arg2 ):
    ...     print( arg2 )
    ...     a = 1/0
    ...
    >>> try:
    ...     f1( "Hello, World! #1" )
    ... except:
    ...     print( "error #1" )
    ...
    前処理はここ
    called wrapper_f with args: ('Hello, World! #1',) kwargs: {} priv args: [] kwargs: {}
    Hello, World! #1
    後処理はここ
    >>> try:
    ...     f2( "Hello, World! #2" )
    ... except:
    ...     print( "error #2" )
    ...
    前処理はここ
    called wrapper_f with args: ('Hello, World! #2',) kwargs: {} priv args: ('mytest1',) kwargs: {}
    Hello, World! #2
    後処理はここ
    >>> try:
    ...     f3( "Hello, World! #3" )
    ... except:
    ...     print( "error #3" )
    ...
    前処理はここ
    called wrapper_f with args: ('Hello, World! #3',) kwargs: {} priv args: [] kwargs: {}
    Hello, World! #3
    error #3
    >>> try:
    ...     f4( "Hello, World! #4" )
    ... except:
    ...     print( "error #4" )
    ...
    前処理はここ
    called wrapper_f with args: ('Hello, World! #4',) kwargs: {} priv args: ('mytest2',) kwargs: {}
    Hello, World! #4
    error #4
    >>>
    """
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )

    def _wrapper( self, func ):
        """デコレータ呼び出し本体"""
        @wraps(func)
        def wrapper_f( *args, **kwargs ):
            # 前処理はここ
            print( "前処理はここ" )
            print( "called wrapper_f with",
                "args:", args, "kwargs:", kwargs,
                "priv args:", self._args, "kwargs:", self._kwargs )
            try:
                ret = func( *args, **kwargs )
            except:
                raise
            # 後処理はここ
            print( "後処理はここ" )
            return ret
        # wrapper_f 内で、__name__ と __doc__ を操作する場合には
        # 下の setattr は削除する
        setattr( self, "__name__", wrapper_f.__name__ )
        setattr( self, "__doc__", wrapper_f.__doc__ )
        return wrapper_f


###########################################
#   unitttest
###########################################
import unittest
from io import StringIO
import sys

class Test_My_Decorator(unittest.TestCase):
    def setUp(self):
        self.saved_stdout = sys.stdout
        self.stdout = StringIO()
        sys.stdout = self.stdout

    def tearDown(self):
        sys.stdout = self.saved_stdout

    def test_decorator_noarg(self):
        @my_decorator
        def t1(arg0):
            print( arg0 )

        t1("test_decorator_noarg")

        self.assertEqual(self.stdout.getvalue(),
            "前処理はここ\n"
            "called wrapper_f with args: ('test_decorator_noarg',) kwargs: {} priv args: [] kwargs: {}\n"
            "test_decorator_noarg\n"
            "後処理はここ\n"
            )

    def test_decorator_witharg(self):
        @my_decorator('with arg')
        def t1(arg0):
            print( arg0 )

        t1("test_decorator_witharg")

        self.assertEqual(self.stdout.getvalue(),
            "前処理はここ\n"
            "called wrapper_f with args: ('test_decorator_witharg',) kwargs: {} priv args: ('with arg',) kwargs: {}\n"
            "test_decorator_witharg\n"
            "後処理はここ\n"
            )

    def test_functionname(self):
        @my_decorator
        def t1():
            return t1.__name__

        f_name = t1()

        self.assertEqual( f_name, "t1" )

    def test_docattribute(self):
        @my_decorator
        def t1():
            """Test Document"""
            pass

        self.assertEqual( t1.__doc__, "Test Document" )


###########################################
#   main
###########################################
if __name__ == '__main__':

    @my_decorator
    def f1( arg1 ):
        print( arg1 )

    @my_decorator('mytest1')
    def f2( arg2 ):
        print( arg2 )

    @my_decorator
    def f3( arg1 ):
        print( arg1 )
        a = 1/0

    @my_decorator('mytest2')
    def f4( arg2 ):
        print( arg2 )
        a = 1/0

    try:
        f1( "Hello, World! #1" )
    except:
        print( "error #1" )

    try:
        f2( "Hello, World! #2" )
    except:
        print( "error #2" )

    try:
        f3( "Hello, World! #3" )
    except:
        print( "error #3" )

    try:
        f4( "Hello, World! #4" )
    except:
        print( "error #4" )

    import doctest
    doctest.testmod()

    unittest.main()