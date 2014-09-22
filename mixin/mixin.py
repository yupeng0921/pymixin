#!/usr/bin/env python

import types

class InstantiationMixinError(Exception):
    pass

class InvalidMixinError(Exception):
    pass

class InheritMixinError(Exception):
    pass

def mixin_new(cls, *args, **kwargs):
    raise InstantiationMixinError(cls)

class MixinMeta(type):
    def __new__(cls, clsname, bases, dct):
        if clsname == 'Mixin':
            dct['__mixin__'] = True
        elif (len(bases) == 1) and bases[0].__name__ == 'Mixin':
            dct['__mixin__'] = True
        if '__mixin__' in dct:
            if dct['__mixin__']:
                dct['__new__'] = mixin_new
        else:
            raise InheritMixinError(clsname)
        return super(MixinMeta, cls).__new__(cls, clsname, bases, dct)

class Mixin(object):
    __metaclass__ = MixinMeta

def mixin(*clses):
    for cls in clses:
        if not (hasattr(cls, '__mixin__') and getattr(cls, '__mixin__')):
            raise InvalidMixinError(cls)
    def generate_mixin(ori_cls):
        meta_clses = []
        ignore_clses = (types.ClassType, types.TypeType, MixinMeta)
        for base in ori_cls.__bases__:
            base_type = type(base)
            if base_type not in ignore_clses and base_type not in meta_clses:
                meta_clses.append(base_type)
        if meta_clses:
            new_type = type('MixinMeta', (MixinMeta,)+tuple(meta_clses), {})
        else:
            new_type = MixinMeta
        dct = {}
        try:
            is_mixin = getattr(ori_cls, '__mixin__')
        except Exception,e:
            is_mixin = False
        dct['__mixin__'] = is_mixin
        if not is_mixin:
            try:
                ori_new = getattr(ori_cls, '__new__')
            except Exception, e:
                ori_new = getattr(object, '__new__')
            dct['__new__'] = ori_new
        return new_type(ori_cls.__name__,
                        (ori_cls,)+tuple(clses),
                        dct)
    return generate_mixin
