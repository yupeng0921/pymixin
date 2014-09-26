#!/usr/bin/env python

import unittest
from mixin import Mixin, mixin, InstantiationMixinError, InvalidMixinError, InheritMixinError

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
            def func_mixin_c(self):
                return 'do_func_mixin_c'
        self.MixinC_A = MixinC_A
        @mixin(MixinB)
        @mixin(MixinA)
        class MixinC_A_B(Mixin):
            def func_mixin_c(self):
                return 'do_func_mixin_c'
        self.MixinC_A_B = MixinC_A_B
        class MixinShadowA(Mixin):
            def func_mixin_a(self):
                return 'do_func_mixin_shadow_a'
        self.MixinShadowA = MixinShadowA

    def test_instantiation_simple_mixin(self):
        with self.assertRaises(InstantiationMixinError):
            self.MixinA()

    def test_instantiation_inherit_mixin(self):
        with self.assertRaises(InstantiationMixinError):
            self.MixinC_A()

    def test_instantiation_inherit_two_level_mixin(self):
        with self.assertRaises(InstantiationMixinError):
            self.MixinC_A_B()

    def test_inherit_simple_mixin_to_normal(self):
        with self.assertRaises(InheritMixinError):
            class A(self.MixinA): pass

    def test_inherit_inherit_mixin_to_normal(self):
        with self.assertRaises(InheritMixinError):
            class A(self.MixinC_A): pass

    def test_using_simple_mixin(self):
        @mixin(self.MixinA)
        class A(object): pass
        self.assertTrue(hasattr(A, 'func_mixin_a'))
        a = A()
        self.assertEqual('do_func_mixin_a', a.func_mixin_a())

    def test_using_inherit_mixin(self):
        @mixin(self.MixinC_A)
        class A(object): pass
        self.assertTrue(hasattr(A, 'func_mixin_a'))
        self.assertTrue(hasattr(A, 'func_mixin_c'))
        a = A()
        self.assertEqual('do_func_mixin_a', a.func_mixin_a())
        self.assertEqual('do_func_mixin_c', a.func_mixin_c())

    def test_using_inherit_two_level_mixin(self):
        @mixin(self.MixinC_A_B)
        class A(object): pass
        self.assertTrue(hasattr(A, 'func_mixin_a'))
        self.assertTrue(hasattr(A, 'func_mixin_b'))
        self.assertTrue(hasattr(A, 'func_mixin_c'))
        a = A()
        self.assertEqual('do_func_mixin_a', a.func_mixin_a())
        self.assertEqual('do_func_mixin_b', a.func_mixin_b())
        self.assertEqual('do_func_mixin_c', a.func_mixin_c())

    def test_multi_level_mixin(self):
        @mixin(self.MixinB)
        @mixin(self.MixinA)
        class A(object): pass
        self.assertTrue(hasattr(A, 'func_mixin_a'))
        self.assertTrue(hasattr(A, 'func_mixin_b'))
        a = A()
        self.assertEqual('do_func_mixin_a', a.func_mixin_a())
        self.assertEqual('do_func_mixin_b', a.func_mixin_b())

    def test_single_level_multi_mixin(self):
        @mixin(self.MixinA, self.MixinB)
        class A(object): pass
        self.assertTrue(hasattr(A, 'func_mixin_a'))
        self.assertTrue(hasattr(A, 'func_mixin_b'))
        a = A()
        self.assertEqual('do_func_mixin_a', a.func_mixin_a())
        self.assertEqual('do_func_mixin_b', a.func_mixin_b())

    def test_multi_level_shadow(self):
        @mixin(self.MixinShadowA)
        class A(object): pass
        self.assertTrue(hasattr(A, 'func_mixin_a'))
        a = A()
        self.assertEqual('do_func_mixin_shadow_a', a.func_mixin_a())

        @mixin(self.MixinA)
        @mixin(self.MixinShadowA)
        class A(object): pass
        self.assertTrue(hasattr(A, 'func_mixin_a'))
        a = A()
        self.assertEqual('do_func_mixin_a', a.func_mixin_a())

    def test_single_level_shadow(self):
        @mixin(self.MixinShadowA)
        class A(object): pass
        self.assertTrue(hasattr(A, 'func_mixin_a'))
        a = A()
        self.assertEqual('do_func_mixin_shadow_a', a.func_mixin_a())

        @mixin(self.MixinA,self.MixinShadowA)
        class A(object): pass
        self.assertTrue(hasattr(A, 'func_mixin_a'))
        a = A()
        self.assertEqual('do_func_mixin_a', a.func_mixin_a())

    def test_current_class_overite(self):
        @mixin(self.MixinA)
        class A(object):
            def func_mixin_a(self):
                return 'do_func_in_real_class'
        a = A()
        self.assertEqual('do_func_in_real_class', a.func_mixin_a())

    def test_father_class_overrite(self):
        class M(object):
            def func_mixin_a(self):
                return 'do_func_in_father_class'
        @mixin(self.MixinA)
        class A(M): pass
        a = A()
        self.assertEqual('do_func_mixin_a', a.func_mixin_a())

    def test_multi_metaclass(self):
        class MetaM(type): pass
        class M(object):
            __metaclass__ = MetaM
        @mixin(self.MixinA)
        class A(M): pass
        self.assertTrue(hasattr(A, 'func_mixin_a'))
        a = A()
        self.assertEqual('do_func_mixin_a', a.func_mixin_a())

    def test_old_style_class(self):
        @mixin(self.MixinA)
        class A(): pass
        self.assertTrue(hasattr(A, 'func_mixin_a'))
        a = A()
        self.assertEqual('do_func_mixin_a', a.func_mixin_a())

    def test_inherit_from_mixined_class(self):
        @mixin(self.MixinA)
        class A(): pass
        class M(A): pass
        self.assertTrue(hasattr(M, 'func_mixin_a'))
        m = M()
        self.assertEqual('do_func_mixin_a', m.func_mixin_a())

    def test_multi_inherit_from_mixined_class(self):
        @mixin(self.MixinA)
        class A(): pass
        @mixin(self.MixinB)
        class B(): pass
        class M(A, B): pass
        self.assertTrue(hasattr(M, 'func_mixin_a'))
        self.assertTrue(hasattr(M, 'func_mixin_b'))
        m = M()
        self.assertEqual('do_func_mixin_a', m.func_mixin_a())
        self.assertEqual('do_func_mixin_b', m.func_mixin_b())
