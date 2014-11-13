#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import namedtuple
import time

class hashdict(dict):
    """
    hashable dict implementation, suitable for use as a key into
    other dicts.

        >>> h1 = hashdict({"apples": 1, "bananas":2})
        >>> h2 = hashdict({"bananas": 3, "mangoes": 5})
        >>> h1+h2
        hashdict(apples=1, bananas=3, mangoes=5)
        >>> d1 = {}
        >>> d1[h1] = "salad"
        >>> d1[h1]
        'salad'
        >>> d1[h2]
        Traceback (most recent call last):
        ...
        KeyError: hashdict(bananas=3, mangoes=5)

    based on answers from
       http://stackoverflow.com/questions/1151658/python-hashable-dicts

    """
    def __key(self):
        return tuple(sorted(self.items()))
    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__,
            ", ".join("{0}={1}".format(
                    str(i[0]),repr(i[1])) for i in self.__key()))

    def __hash__(self):
        return hash(self.__key())
    def __setitem__(self, key, value):
        raise TypeError("{0} does not support item assignment"
                         .format(self.__class__.__name__))
    def __delitem__(self, key):
        raise TypeError("{0} does not support item assignment"
                         .format(self.__class__.__name__))
    def clear(self):
        raise TypeError("{0} does not support item assignment"
                         .format(self.__class__.__name__))
    def pop(self, *args, **kwargs):
        raise TypeError("{0} does not support item assignment"
                         .format(self.__class__.__name__))
    def popitem(self, *args, **kwargs):
        raise TypeError("{0} does not support item assignment"
                         .format(self.__class__.__name__))
    def setdefault(self, *args, **kwargs):
        raise TypeError("{0} does not support item assignment"
                         .format(self.__class__.__name__))
    def update(self, *args, **kwargs):
        raise TypeError("{0} does not support item assignment"
                         .format(self.__class__.__name__))
    def __add__(self, right):
        result = hashdict(self)
        dict.update(result, right)
        return result

class Cache():
    def __init__(self, app):
        self.app = app # retain a reference to the master app
                       # such that Cache does not drop out of scope
        self._cache_dict = {}

    def memoize( self, valid_for = float('Inf'), unless = (lambda: True) ):
        def dummy_func(func):
            def func_wrapper(*args, **kwargs):
                cache_key = {}
                if kwargs != None: cache_key.update(kwargs)
                cache_key.update({'args': args, 'func_nam': func.__name__})
                cache_key = hashdict( cache_key )
                retval = self.get(cache_key)
                if retval == None:
                    retval = func(*args, **kwargs)
                    if not unless():
                        self.set( cache_key, retval, valid_for )
                return retval
            return func_wrapper
        return dummy_func

    def set( self, key, value, valid_for = float('Inf')):
        self._cache_dict[key] = {'value': value,
            'time': time.time(),
            'valid_for': valid_for}

    def get( self, key ):
        value = self._cache_dict.get(key, None)

        if value != None:
            expired = time.time() - value['time'] > value['valid_for']
            if not expired:
                print 'cache_hit'
                return value['value']
            else:
                print 'expired'
                del self._cache_dict[key]
                return None
        else:
            print 'cache miss'
            return None


if __name__ == '__main__':
    import xmlrpclib, urllib
    from time import sleep

    app = True

    cache = Cache(app)
    debug = True

    @cache.memoize( unless = (lambda: debug) )
    def add( a, b ):
        return a+b

    print 'should get a miss'
    add(1,2)
    debug = False
    print 'should get a miss'
    add(1,2)
    print 'should get a hit'
    add(1,2)

    url = "http://lorempixel.com/400/400/"
    b = xmlrpclib.Binary(urllib.urlopen(url).read())
    cache_key = 1234
    cache.set(cache_key, b, 1)
    print 'should get a hit'
    cache.get(cache_key)
    sleep(1)
    print 'should be expired'
    cache.get(cache_key)
    print app

    # lacks memory safty. can get very large. 
    # no systematic deletion of expired cache