# random number class

from random import random
from normals import inverseCumulativeNormal
from sys import version_info

if version_info[0] == 3:
    xrange = range

class RandomBase(object):
    """
    Abstract random number class.
    Uses the standard library's random() for uniform random variables and
    normals.inverseCumulativeNormal() to transform them.
    """

    def __init__(self, dim):
        self.dim = dim

    def getUniforms(self, N):
        return ([random() for x in xrange(self.dim)] for x in xrange(N))

    def getGaussians(self, N):
        return ([inverseCumulativeNormal(x) for x in v] for v in self.getUniforms(N))



class ParkMiller(object):
    """
    Park-Miller random number generator.
    stream() method returns a generator producing pseudo-random
    numbers in the interval [1, 2147483646].
    """

    def __init__(self,seed=1):
        self._const_a = 16807
        self._const_m = 2147483647
        self._const_q = 127773
        self._const_r = 2836
        self._seed = max(int(seed),1)
        self.maximum = self._const_m - 1
        self.minimum = 1

    def stream(self,N):
        a, m, q, r = self._const_a, self._const_m, self._const_q, self._const_r
        count = 0
        while count < N:
            k = self._seed // q # // ensures integer division for Python 3.
            self._seed = (a * (self._seed - k * q) - k * r)
            if self._seed < 0:
                self._seed += m
            yield self._seed
            count += 1


    
class RandomParkMiller(RandomBase):
    """
    A RandomBase class using the ParkMiller class
    to generate the uniform random variables.
    """
    
    def __init__(self,dim,seed=1):
        self.dim = dim
        self._seed = seed
        self._pm = ParkMiller(seed)
        self._r = 1/(1. + self._pm.maximum)

    def getUniforms(self,N):
        return ([x * self._r for x in self._pm.stream(self.dim)] for i in xrange(N))

    def skip(self, nPaths):
        for i in self.getUniforms(nPaths):
            pass

    def reset(self):
        self._pm = ParkMiller(self.seed)

    def _getSeed(self):
        return self._seed

    def _setSeed(self,seed):
        self._seed = seed
        self.reset(seed)

    seed = property(_getSeed, _setSeed)



class AntiThetic(RandomBase):
    """
    Anti-thetic sampling class: wraps another RandomBase class.
    Currently this only works properly for streams of an even length.
    """

    def __init__(self, base):
        self._base = base
        self._oddEven = True

    def getUniforms(self, N):
        for v in self._base.getUniforms(N // 2): # the argument must be an 'int' in Python3
            yield v
            yield [1-x for x in v]

    def _setSeed(self, seed):
        self._base.seed = seed
        self._oddEven = True

    def skip(self, nPaths):
        self._base.skip(nPaths / 2)

    def reset(self):
        self._base.reset()
        self._oddEven = True



def loop(N, s):
    """
    Returns a generator of length N, returning
    a loop of values modulo s.
    """
    i = 0
    while i < N:
        yield i % s
        i += 1



class SimpleStratifiedPM(RandomBase):
    """
    Stratified random sampling based on the RandomParkMiller class.
    """

    def __init__(self,seed=1,segments=2**8):
        self.dim = 1
        self._rpm = RandomParkMiller(1,seed)
        self._seed = seed
        self._segments = segments

    def getUniforms(self, N):
        s = self._segments
        return ([(l + x[0])/s] for l, x in zip(loop(N, s), self._rpm.getUniforms(N)))
        


# Testing

if __name__ == "__main__":
    rv = AntiThetic(SimpleStratifiedPM(1,16))
    N = 2**8
    r = [x[0] for x in rv.getUniforms(N)]
    mean = sum(r)/N
    var = sum((x-mean)**2 for x in r)/N
    print("mean = %f" % mean)
    print("variance = %f" % var)
