# PyQuantFi - payoffs.py
# (c) 2012 Nick Collins

def VanillaCall(k):
    """
    >>> p = VanillaCall(100)
    >>> (p(150),p(100),p(50),p(0))
    (50, 0, 0, 0)
    >>> 0 == round(p(100.00001) - 0.00001,5)
    True
    """
    def call(s):
        return max(s - k, 0)
    return call


def VanillaPut(k):
    """
    >>> p = VanillaPut(100)
    >>> (p(150),p(100),p(50),p(0))
    (0, 0, 50, 100)
    >>> 0 == round(0.00001 - p(99.99999),5)
    True
    """
    def call(s):
        return max(k - s, 0)
    return call

def DigitalCall(k):
    """
    >>> p = DigitalCall(60)
    >>> (p(60.00001),p(60),p(59.99999))
    (1, 0, 0)
    """
    def call(s):
        if s > k: return 1
        else: return 0
    return call

def DigitalPut(k):
    """
    >>> p = DigitalPut(60)
    >>> (p(60.00001),p(60),p(59.99999))
    (0, 0, 1)
    """
    def call(s):
        if s < k: return 1
        else: return 0
    return call


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
