#!/usr/bin/env python

__all__ = ['mixin', 'Mixin', 'InstantiationMixinError', 'InvalidMixinError']

try:
    from mixin import mixin, Mixin, InstantiationMixinError, InvalidMixinError
except Exception, e:
    pass
