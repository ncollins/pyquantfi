# PyQuantFi - pathDependent.py
# (c) 2012 Nick Collins

from math import log, exp, sqrt
from payoffs import *


class Cashflow(object):
    def __init__(self,timeIndex,amount):
        self.timeIndex = timeIndex
        self.amount = amount


class PathDependent(object):
    def __init__(self,lookAtTimes):
        self._lookAtTimes = lookAtTimes

    def getLookAtTimes(self):
        return self._lookAtTimes

    def maxNumberOfCashflows(self):
        return self._maxNumberOfCashflows()

    def possibleCashflowTimes(self):
        return self._possibleCashflowTimes()

    def cashflows(self,spotValues,generatedFlows):
        return self._cashflows(spotValues,generatedFlows)


class ExoticEngine(object):

    def __init__(self,product,paramDiscount):
        self._product = product
        self._r = paramDiscount
        self._cashflows = [0] * self._product.maxNumberOfCashflows()

        self._discounts = [exp(self._r.integral(0,t)) for t in 
                          self._product.possibleCashflowTimes()]

    def getOnePath(self,spotValues):
        return self._getOnePath(spotValues)

    def doSimulation(self,numberOfPaths,statsGatherer):
        spotValues = [0] * len(self._product.getLookAtTimes())
        for i in range(numberOfPaths):
            self.getOnePath(spotValues)
            #print "doSimulation > getOnePath(): "
            #print "spotValues = " + str(spotValues)
            #print "_cashflows = " + str(self._cashflows)
            thisValue = self.doOnePath(spotValues)
            statsGatherer.addOneResult(thisValue)

    def doOnePath(self,spotValues):
        numberFlows = self._product.maxNumberOfCashflows()
        self._product.cashflows(spotValues,self._cashflows)
        value = 0.
        for i in range(numberFlows):
            value += (self._cashflows[i].amount *
                      self._discounts[self._cashflows[i].timeIndex])
        return value


class ExoticBSEngine(ExoticEngine):
    
    def __init__(self,product,r,d,vol,randomGen,spot):
        self._product = product
        self._r = r
        self._randomGen = randomGen
        self._drifts = []
        self._stDevs = []

        self._cashflows = [0] * self._product.maxNumberOfCashflows()
        self._discounts = [exp(self._r.integral(0,t)) for t in
                           self._product.possibleCashflowTimes()]

        times = product.getLookAtTimes()
        self._numberOfTimes = len(times)
        self._randomGen.resetDimensionality(self._numberOfTimes)

        var = vol.integralSq(0,times[0])
        self._drifts.append(r.integral(0,times[0])
                            - d.integral(0,times[0])
                            - 0.5 * var)
        self._stDevs.append(sqrt(var))

        for i in range(1,self._numberOfTimes):
            thisVar = vol.integralSq(times[i-1],times[i])
            self._drifts.append(r.integral(times[i-1],times[i])
                                - d.integral(times[i-1],times[i])
                                - 0.5 * thisVar)
            self._stDevs.append(sqrt(thisVar))

        self._logSpot = log(spot)

        
    def _getOnePath(self,spotValues):
        #spotValues = [] # for now spotValues is overwritten
        self._variates = self._randomGen.getGaussians()
        currentLogSpot = self._logSpot
        for i in range(self._numberOfTimes):
            currentLogSpot += self._drifts[i]
            currentLogSpot += self._stDevs[i] * self._variates[i]
            spotValues[i] = exp(currentLogSpot)
            #spotValues.append(exp(currentLogSpot)) #
        return spotValues #


class PathDependentAsian(PathDependent):

    def __init__(self,lookAtTimes,deliveryTime,payoff):
        self._payoff = payoff
        self._lookAtTimes = lookAtTimes
        self._numberOfTimes = len(lookAtTimes)
        self._deliveryTime = deliveryTime

    def _maxNumberOfCashflows(self):
        return 1

    def _possibleCashflowTimes(self):
        return [self._deliveryTime]

    def _cashflows(self,spotValues,generatedFlows):
        #total = sum(spotValues)
        #mean = total/self._numberOfTimes
        #product = reduce(lambda x,y: x * y,spotValues)
        product = 1
        for value in spotValues:
            product *= value
        mean = product ** (1./self._numberOfTimes)
        generatedFlows[0] = Cashflow(0,self._payoff(mean))
        #generatedFlows[0].timeIndex = 0
        #generatedFlows[0].amounts = self.payoff(mean)

