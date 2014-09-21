#!/usr/bin/env python

class InstantiationMixinError(Exception):
    pass

class InvalidMixinError(Exception):
    pass

class Mixin(object):
    def __new__(cls, *args, **kwargs):
        raise InstantiationMixinError(cls)

def mixin(*clses):
    for cls in clses:
        for klass in cls.__mro__:
            if klass.__new__ != Mixin.__new__ and klass != object:
                raise InvalidMixinError(klass)
    def generate_mixin(ori_cls):
        try:
            default_new = getattr(ori_cls, '__new__')
        except Exception, e:
            default_new = getattr(object, '__new__')
        return type(ori_cls.__name__,
                    (ori_cls,)+tuple(clses),
                    {'__new__': default_new})
    return generate_mixin
