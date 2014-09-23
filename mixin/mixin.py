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
    def generate_mixin(orig_cls):
        ori_type = type(orig_cls)
        normal_types = six.class_types + (MixinMeta,)
        if ori_type in normal_types:
            new_type = MixinMeta
        else:
            new_type = type('MixinMeta', (MixinMeta, ori_type), {})
        orig_vars = orig_cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        try:
            is_mixin = getattr(orig_cls, '__mixin__')
        except Exception as exc:
            is_mixin = False
        orig_vars['__mixin__'] = is_mixin
        if not is_mixin:
            try:
                orig_new = getattr(orig_cls, '__new__')
            except Exception as exc:
                orig_new = getattr(object, '__new__')
            orig_vars['__new__'] = orig_new
        orig_bases = list(orig_cls.__bases__)
        if object in orig_bases:
            orig_bases.remove(object)
        if Mixin in orig_bases:
            orig_bases.remove(Mixin)
        return new_type(orig_cls.__name__,
                        tuple(orig_bases) + tuple(clses),
                        orig_vars)
    return generate_mixin
