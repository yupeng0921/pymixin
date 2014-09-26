# do mixin for python

## What mixin is
In object-oriented programming languages, a mixin is a class which contains a combination of methods from other classes. How such a combination is done depends on the language, but it is not by inheritance. If a combination contains all methods of combined classes it is equivalent to multiple inheritance.
refer to this wiki:
http://en.wikipedia.org/wiki/Mixin

## install pymixin

install it from pip:
    pip install pymixin

In fact, the pymix package only has one file, it is mixin.py, so you can also copy it directly to your project directory.

## how to use pymixin

### a simple example

import the Mixin class and mixin decorator from the mixin module:

    from mixin import Mixin, mixin

The user's mixin should always inherit from the Mixin class:

    from mixin import Mixin
	class MixinA(Mixin):
	    def func_mixin_a(self):
		    return 'do_func_mixin_a'

and then use the mixin decorator add the mixin:

	@mixin(MixinA)
	class A(object): pass
	a = A()

	a.do_func_mixin_a # return 'do_func_mixin_a'

