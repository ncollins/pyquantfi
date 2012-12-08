# MODULES 

import time

from payoffs import VanillaCall
from options import VanillaOption
from parameters import ParameterConstant
from statistics_mc import StatisticMean, ConvergenceTable
from random_base import RandomParkMiller, AntiThetic
from path_dependent import ExoticBSEngine, PathDependentAsian

# CONSTANTS

N = 2**15 
SPOT_100 = 100
SPOT_130 = 130

# INPUTS

call_100_1 = VanillaOption(VanillaCall(100),1)
call_130_1 = VanillaOption(VanillaCall(130),1)

r = ParameterConstant(0.04)
vol = ParameterConstant(0.4)

gatherer0 = StatisticMean()
gatherer = ConvergenceTable(gatherer0)

randomGen0 = RandomParkMiller(10,1)
randomGen = AntiThetic(randomGen0)

times = [n/100. for n in range(1,100,1)]
expiry = 1
callPayoff = VanillaCall(100)
asian = PathDependentAsian(times,expiry,callPayoff)

d = ParameterConstant(0.00)

# CALCULATIONS

engine = ExoticBSEngine(asian,r,d,vol,randomGen,100)
engine.do_simulation(N,gatherer)
print(gatherer.get_results())
