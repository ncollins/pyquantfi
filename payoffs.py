
import math
import random

class Payoff(object):
    0

class VanillaCall(Payoff):
    def __init__(self,k):
        self._strike = k
    def __call__(self,s):
        return max(s - self._strike, 0)


class VanillaPut(Payoff):
    def __init__(self,k):
        self._strike = k
    def __call__(self,s):
        return max(self._strike - s, 0)

class DigitalCall(Payoff):
    def __init__(self,k):
        self._strike = k
    def __call__(self,s):
        if s > self._strike: return 1
        else: return 0

class DigitalPut(Payoff):
    def __init__(self,k):
        self._strike = k
    def __call__(self,s):
        if s < self._strike: return 1
        else: return 0



