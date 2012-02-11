# random number class

from random import normalvariate, uniform
from normals import *

class SimpleRandom(object):
    """
    This is a template for the new style of random number classes.
    getUniforms() and getNormals() return a generator object.
    """

    def __init__(self, dim):
        self.dim = dim

    def getGaussians(self, N):
        def vector():
            return (normalvariate(0,1) for x in range(self.dim))
        return (vector() for x in range(N))

    def getUniforms(self, N):
        def vector():
            return (uniform(0,1) for x in range(self.dim))
        return (vector() for x in range(N))
        
        

class RandomBase(object):
    """
    Abstract random number class.
    """

    def __init__(self, dim):
        self._dimension = dim

    def getDimensionality(self):
        return self._dimension

    def getUniforms(self):
        return self._getUniforms()

    def getGaussians(self):
        return self._getGaussians()

    def skip(self,numberOfPaths):
        return self._skip(numberOfPaths)

    def setSeed(self, seed):
        self._setSeed(seed)

    def reset(self):
        self._reset

    def resetDimensionality(self, newDim):
        self._resetDimensionality(newDim)

    def _getGaussians(self):
        return [inverseCumulativeNormal(x) for x in self.getUniforms()]

    def _resetDimensionality(self,newDim):
        self._dimension = newDim


class ParkMiller(object):
    """
    Park-Miller random number generator.
    """

    def __init__(self,seed=1,N=2**32):
        self._const_a = 16807
        self._const_m = 2147483647
        self._const_q = 127773
        self._const_r = 2836
        self._seed = seed

    def setSeed(self,seed):
        self._seed = int(seed) or 1

    def max(self):
        return self._const_m - 1

    def min(self):
        return 1

    def iter(self):
        return self

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        k = self._seed / self._const_q
        self._seed = (self._const_a * (self._seed - k * self._const_q) 
                    - k * self._const_r)
        if self._seed < 0:
            self._seed += self._const_m
        return self._seed

    
class RandomParkMiller(RandomBase):
    """
    A RandomBase class using the ParkMiller class
    to generate the uniform random variables.
    """
    
    def __init__(self,dim,seed=1):
        self._dimension = dim
        self._initialSeed = seed
        self._innerGenerator = ParkMiller(seed)
        self._reciprocal = 1/(1. + self._innerGenerator.max())

    def _getUniforms(self):
        dim = self.getDimensionality()
        r = self._reciprocal
        return [x * r
                for x,y in zip(self._innerGenerator,range(dim))]

    def _skip(self, numberOfPaths):
        tmp = []
        for i in range(numberOfPaths):
            tmp.append(self.getUniforms())

    def _setSeed(self,seed):
        self._initialSeed = seed
        self._innerGenerator.setSeed(seed)

    def _reset(self):
        self._innerGenerator.setSeed(self._initialSeed)

    def _resetDimensionality(self,newDim):
        self._dimension = newDim
        self._innerGenerator.setSeed(self._initialSeed)


class AntiThetic(RandomBase):
    """
    Anti-thetic sampling class: acts as a wrapper for
    any other RandomBase class.
    """

    def __init__(self,base):
        self._base = base
        self._oddEven = True

    def _getUniforms(self):
        if self._oddEven:
            v = self._base.getUniforms()
            self._oddEven = False
        else:
            v = [(1-x) for x in self._variates]
            self._oddEven = True
        return v

    def _setSeed(self,seed):
        self._base.setSeed(seed)
        self._oddEven = True

    def _skip(self,numberOfPaths):
        if numberOfPaths == 0:
            return
        if self._oddEven:
            self._oddEven = False
            self._numberOfPaths -= 1
        self._base.skip(numberOfPaths / 2)
        if numberOfPaths % 2 == 1: # this needs to be tidied!
            tmp = self.getUniforms()

    def _resetDimensionality(self,newDim):
        self._dimensionality = newDim
        self._base.resetDimensionality(newDim)

    def _reset(self):
        self._base.reset()
        self._oddEven = True


# stratified random sampling

def loop(N):
    i = 0
    while 1:
        yield i
        i += 1
        if i == N: i = 0

def stratified(N):
    """
    Returns uniform random variables in (0,1).
    The interval is divided into numSeg segments and an equal number
    of rv is taken from each segment.
    """
    l = loop(N)
    while 1:
        a = l.next() + .0
        yield uniform(a/N, (a+1)/N)



class SimpleStratified(RandomBase):
    
    def __init__(self,seed=0,numberOfSegments=2**16):
        self._dimension = 1
        self._seed = seed
        self._numberOfSegments = numberOfSegments
        self._stratified = stratified(numberOfSegments)

    def _getUniforms(self):
        return [self._stratified.next()]



class SimpleStratifiedPM(RandomBase):
    """
    Stratified random sampling based on the RandomParkMiller class.
    After returning (x1, x2, x3, ...) it will next return (-x1, -x2, -x3, ...).
    """

    def __init__(self,seed=0,segments=2**16):
        self.dimension = 1
        self._rpm = RandomParkMiller(1,seed)
        self._seed = seed
        self._segments = segments
        self._loop = loop(segments)

    def _getUniforms(self):
        rv = self._rpm.getUniforms()[0]
        a = self._loop.__next__()
        x = (a + rv) / self._segments
        if x == 0: print(rv,a,self._segments)
        return [(a + rv) / self._segments]

#testing

if __name__ == "__main__":
    #rpm = RandomParkMiller(1,1)
    rv = SimpleStratifiedPM(1,16)
    N = 2**12
    r = []
    for i in range(N):
        x = rv.getUniforms()[0]
        r.append(x)
        print(x)
    mean = sum(r)/N
    var = sum((x-mean)**2 for x in r)/N
    print("mean = %f" % mean)
    print("variance = %f" % var)
    print("stdev = %f" % var**0.5)
