#!/usr/bin/env python

import types
import six

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

@six.add_metaclass(MixinMeta)
class Mixin(object): pass

def mixin(*clses):
    for cls in clses:
        if not (hasattr(cls, '__mixin__') and getattr(cls, '__mixin__')):
            raise InvalidMixinError(cls)
    def generate_mixin(ori_cls):
        ori_type = type(ori_cls)
        if ori_type in (types.ClassType, types.TypeType, MixinMeta):
            new_type = MixinMeta
        else:
            new_type = type('MixinMeta', (MixinMeta, ori_type), {})
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
