# MODULES 

import time

from payoffs import *
from options import *
from simple_mc import *
from parameters import *
from statistics_mc import *
from random_base import SimpleStratifiedPM, AntiThetic

# CONSTANTS

N = 2 ** 16 #100000
SPOT_100 = 100
SPOT_130 = 130

# INPUTS

call_100_1 = VanillaOption(VanillaCall(100),1)
call_130_1 = VanillaOption(VanillaCall(130),1)

r = ParameterConstant(0.04)
vol = ParameterConstant(0.4)

gatherer0 = StatisticMean()
gatherer = ConvergenceTable(gatherer0)

gathererB0 = StatisticMean()
gathererB = ConvergenceTable(gathererB0)

randomStrat0 = SimpleStratifiedPM(1,64)
randomStrat = AntiThetic(randomStrat0)


# CALCULATIONS

t1 = time.time()

simpleMC8(call_130_1, SPOT_100, vol, r, N, gatherer, randomStrat)
print(gatherer.getResults())

print("")

simpleMC8(call_130_1, SPOT_100, vol, r, N, gathererB, randomStrat)
print(gathererB.getResults())

t2 = time.time()
print(str(round(t2 - t1,2)) + " seconds")
