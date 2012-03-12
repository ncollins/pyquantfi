# MODULES 

import time

from payoffs import *
from options import *
from simple_mc import *
from parameters import *
from statistics_mc import *
from random_base import *
from path_dependent import *

# CONSTANTS

N = 100000
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

t1 = time.time() # start time

engine = ExoticBSEngine(asian,r,d,vol,randomGen,100)
engine.do_simulation(N,gatherer)
print(gatherer.get_results())

t2 = time.time() # stop time

print(str(round(t2 - t1,2)) + " seconds")
