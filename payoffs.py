# PyQuantFi - payoffs.py
# (c) 2012 Nick Collins

import math
import random

class Payoff(object):
    0

class VanillaCall(Payoff):
    """
    >>> p = VanillaCall(100)
    >>> results = (p(150),p(100.00001),p(100),p(99.99999),p(50),p(0),p(-50))
    >>> (p(150),p(100),p(50),p(0))
    (50, 0, 0, 0)
    >>> 0 == round(p(100.00001) - 0.00001,5)
    True
    """
    
    def __init__(self,k):
        self._strike = k

    def __call__(self,s):
        return max(s - self._strike, 0)


class VanillaPut(Payoff):
    """
    >>> p = VanillaPut(100)
    >>> results = (p(150),p(100.00001),p(100),p(99.99999),p(50),p(0),p(-50))
    >>> (p(150),p(100),p(50),p(0))
    (0, 0, 50, 100)
    >>> 0 == round(0.00001 - p(99.99999),5)
    True
    """

    def __init__(self,k):
        self._strike = k
        
    def __call__(self,s):
        return max(self._strike - s, 0)

class DigitalCall(Payoff):
    """
    >>> p = DigitalCall(60)
    >>> (p(60.00001),p(60),p(59.99999))
    (1, 0, 0)
    """

    def __init__(self,k):
        self._strike = k

    def __call__(self,s):
        if s > self._strike: return 1
        else: return 0

class DigitalPut(Payoff):
    """
    >>> p = DigitalPut(60)
    >>> (p(60.00001),p(60),p(59.99999))
    (0, 0, 1)
    """

    def __init__(self,k):
        self._strike = k

    def __call__(self,s):
        if s < self._strike: return 1
        else: return 0


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
