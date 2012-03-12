# PyQuantFi - pathDependent.py
# (c) 2012 Nick Collins

from math import log, exp, sqrt
from sys import version_info

if version_info[0] == 3:
    xrange = range


class Cashflow(object):
    def __init__(self,timeIndex,amount):
        self.timeIndex = timeIndex
        self.amount = amount


class PathDependent(object):
    def __init__(self,lookAtTimes):
        self._lookAtTimes = lookAtTimes

    def get_look_at_times(self):
        return self._lookAtTimes

    def max_number_of_cashflows(self):
        return self._max_number_of_cashflows()

    def possible_cashflow_times(self):
        return self._possible_cashflow_times()

    def cashflows(self, spotValues):
        return self._cashflows(spotValues)


class ExoticEngine(object):

    def __init__(self,product,paramDiscount):
        self._product = product
        self._r = paramDiscount
        self._discounts = [exp(self._r.integral(0,t)) for t in 
                          self._product.possible_cashflow_times()]

    def do_simulation(self,numberOfPaths,statsGatherer):
        for path in self.get_paths(numberOfPaths):
            thisValue = self.do_one_path(path)
            statsGatherer.add_one_result(thisValue)

    def do_one_path(self,spotValues):
        value = 0.
        for c in self._product.cashflows(spotValues):
            value += c.amount * self._discounts[c.timeIndex]
        return value


class ExoticBSEngine(ExoticEngine):
    
    def __init__(self,product,r,d,vol,randomGen,spot):
        self._product = product
        self._r = r
        self._randomGen = randomGen

        self._discounts = [exp(self._r.integral(0,t)) for t in
                           self._product.possible_cashflow_times()]

        times = product.get_look_at_times()
        self._numberOfTimes = len(times)
        self._randomGen.dim = self._numberOfTimes

        # Since the drift and stDev terms are the same for each path
        # they are pre-calculated.
        var = vol.integral_sq(0,times[0])
        self._drifts = [r.integral(0,times[0])
                            - d.integral(0,times[0])
                            - 0.5 * var]
        self._stDevs = [sqrt(var)]

        for i in xrange(1,self._numberOfTimes):
            thisVar = vol.integral_sq(times[i-1],times[i])
            self._drifts.append(r.integral(times[i-1],times[i])
                                - d.integral(times[i-1],times[i])
                                - 0.5 * thisVar)
            self._stDevs.append(sqrt(thisVar))

        self._logSpot = log(spot)

    def get_paths(self, n):
        for v in self._randomGen.get_gaussians(n):
            currentLogSpot = self._logSpot
            spotValues = []
            for i in xrange(self._numberOfTimes):
                currentLogSpot += self._drifts[i]
                currentLogSpot += self._stDevs[i] * v[i]
                spotValues.append(exp(currentLogSpot))
            yield spotValues


class PathDependentAsian(PathDependent):

    def __init__(self,lookAtTimes,deliveryTime,payoff):
        self._payoff = payoff
        self._lookAtTimes = lookAtTimes
        self._numberOfTimes = len(lookAtTimes)
        self._deliveryTime = deliveryTime

    def _max_number_of_cashflows(self):
        return 1

    def _possible_cashflow_times(self):
        return [self._deliveryTime]

    def _cashflows(self, spotValues):
        product = 1
        for value in spotValues:
            product *= value
        mean = product ** (1./self._numberOfTimes)
        return [Cashflow(0, self._payoff(mean))]
