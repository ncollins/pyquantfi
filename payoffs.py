# PyQuantFi - payoffs.py
# (c) 2012 Nick Collins


def VanillaCall(k):
    def call(s):
        return max(s - k, 0)
    return call


def VanillaPut(k):
    def call(s):
        return max(k - s, 0)
    return call


def DigitalCall(k):
    def call(s):
        if s > k: return 1
        else: return 0
    return call


def DigitalPut(k):
    def call(s):
        if s < k: return 1
        else: return 0
    return call
