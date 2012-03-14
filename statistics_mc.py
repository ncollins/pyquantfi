# PyQuantFi - statisticsMC.py
# (c) 2012 Nick Collins


class StatisticMC(object):
    """
    Abstract statistics gathering class
    """

    def add_one_result(self,value):
        self._store_one_result(value)

    def get_results(self):
        return self._get_results()


class StatisticMean(StatisticMC):

    def __init__(self):
        self._runningSum = 0
        self._pathsDone = 0

    def _store_one_result(self,value):
        self._runningSum += value
        self._pathsDone += 1

    def _get_results(self):
        self._results = [[self._runningSum / self._pathsDone ]]
        return self._results


class ConvergenceTable(StatisticMC):

    def __init__(self,gatherer):
        self._stoppingPoint = 2
        self._pathsDone = 0
        self._statisticMC = gatherer
        self._results = []

    def _store_one_result(self,value):
        self._statisticMC.add_one_result(value)
        self._pathsDone += 1
        if (self._pathsDone == self._stoppingPoint):
            self._stoppingPoint *= 2
            thisResult = self._statisticMC.get_results()
            for item in thisResult:
                item.append(self._pathsDone)
                self._results.append(item)

    def _get_results(self):
        tmp = self._results
        if (self._pathsDone * 2 != self._stoppingPoint):
            thisResult = self._statisticMC.get_results()
            for item in thisResult:
                item.append(self._pathsDone)
                tmp.append(item)
        return tmp
