# PyQuantFi - parameters.py
# (c) 2012 Nick Collins

class Parameter(object):
    """
    Abstract parameter class:
    The integral() and integralSq() methods are "public"
    but should be definited in the child object.
    """

    def mean(self,t1,t2):
        total = self.integral(t1,t2)
        return total / (t2-t1)

    def rootMeanSq(self,t1,t2):
        total = self.integralSq(t1,t2)
        return total / (t2-t1)


class ParameterConstant(Parameter):

    def __init__(self, c):
        self._constant = c

    def integral(self,t1,t2):
        return (t2-t1) * self._constant

    def integralSq(self,t1,t2):
        return (t2-t1) * self._constant**2
