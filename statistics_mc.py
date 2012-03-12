# PyQuantFi - statisticsMC.py
# (c) 2012 Nick Collins

class StatisticMC(object):
    """
    Abstract statistics gathering class
    """

    def addOneResult(self,value):
        self._storeOneResult(value)

    def getResults(self):
        return self._getResults()


class StatisticMean(StatisticMC):

    def __init__(self):
        self._runningSum = 0
        self._pathsDone = 0

    def _storeOneResult(self,value):
        self._runningSum += value
        self._pathsDone += 1

    def _getResults(self):
        self._results = [[self._runningSum / self._pathsDone ]]
        return self._results


class ConvergenceTable(StatisticMC):

    def __init__(self,gatherer):
        self._stoppingPoint = 2
        self._pathsDone = 0
        self._statisticMC = gatherer
        self._results = []

    def _storeOneResult(self,value):
        self._statisticMC.addOneResult(value)
        self._pathsDone += 1
        if (self._pathsDone == self._stoppingPoint):
            self._stoppingPoint *= 2
            thisResult = self._statisticMC.getResults()
            for item in thisResult:
                item.append(self._pathsDone)
                self._results.append(item)

    def _getResults(self):
        tmp = self._results
        if (self._pathsDone * 2 != self._stoppingPoint):
            thisResult = self._statisticMC.getResults()
            for item in thisResult:
                item.append(self._pathsDone)
                tmp.append(item)
        return tmp

