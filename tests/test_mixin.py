#!/usr/bin/env python

import unittest
from mixin.mixin import Mixin, mixin, InstantiationMixinError, InvalidMixinError, InheritMixinError

class TestCase(unittest.TestCase):
    def assertRaises(self, exception):
        class ExceptionContext(object):
            def __init__(self, exception, assertEqual):
                self.exception = exception
                self.assertEqual = assertEqual
            def __enter__(self):
                pass
            def __exit__(self, exception, value, traceback):
                self.assertEqual(self.exception, exception)
                return True
        return ExceptionContext(exception, self.assertEqual)

class TestMixin(TestCase):
    def setUp(self):
        class MixinA(Mixin):
            def func_mixin_a(self):
                return 'do_func_mixin_a'
        self.MixinA = MixinA
        class MixinB(Mixin):
            def func_mixin_b(self):
                return 'do_func_mixin_b'
        self.MixinB = MixinB
        @mixin(MixinA)
        class MixinC_A(Mixin):
            def func_mixin_C(self):
                return 'do_func_mixin_c'
        self.MixinC_A = MixinC_A
    def test_instantiation_simple_mixin(self):
        with self.assertRaises(InstantiationMixinError):
            self.MixinA()
    def test_instantiation_inherit_mixin(self):
        with self.assertRaises(InstantiationMixinError):
            self.MixinC_A()
    def test_inherit_simple_mixin(self):
        @mixin(self.MixinA)
        class A(object):
            pass
        self.assertTrue(hasattr(A, 'func_mixin_a'))
        a = A()
        self.assertEqual('do_func_mixin_a', a.func_mixin_a())
    def test_inherit_mixin(self):
        with self.assertRaises(InheritMixinError):
            class A(self.MixinA): pass
