from math import exp, log, sqrt
from random import normalvariate, lognormvariate, seed

def simpleMC8(option, spot, vol, r, N, gatherer, randomGen):
    randomGen.resetDimensionality(1)
    expiry = option.expiry()
    var = vol.integralSq(0,expiry)
    rootVar = sqrt(var)
    itoCorrection = -0.5 * var

    movedSpot = spot * exp(r.integral(0,expiry) + itoCorrection)
    discounting = exp(-r.integral(0,expiry))
    
    runningSum = 0
    for i in range(N):
        variateArray = randomGen.getGaussians()
        thisSpot = movedSpot * exp(rootVar * variateArray[0])
        thisPayoff = option.payoff(thisSpot)
        gatherer.addOneResult(discounting * thisPayoff)

    return

def simpleMC7(option, spot, vol, r, N, gatherer):
    seed(0)
    expiry = option.expiry()
    var = vol.integralSq(0,expiry)
    rootVar = sqrt(var)
    itoCorrection = -0.5 * var

    movedSpot = spot * exp(r.integral(0,expiry) + itoCorrection)
    discounting = exp(-r.integral(0,expiry))
    
    runningSum = 0
    for i in range(N):
        thisGaussian = normalvariate(0,1)
        thisSpot = movedSpot * exp(rootVar * thisGaussian)
        thisPayoff = option.payoff(thisSpot)
        gatherer.addOneResult(discounting * thisPayoff)

    return

def simpleMC2(option, spot, vol, r, N):
    expiry = option.expiry()
    var = vol.integralSq(0,expiry)
    rootVar = sqrt(var)
    itoCorrection = -0.5 * var

    movedSpot = spot * exp(r.integral(0,expiry) + itoCorrection)
    
    runningSum = 0
    for i in range(N):
        thisGaussian = normalvariate(0,1)
        thisSpot = movedSpot * exp(rootVar * thisGaussian)
        thisPayoff = option.payoff(thisSpot)
        runningSum += thisPayoff

    mean = runningSum / N
    mean *= exp(-r.integral(0,expiry))
    return mean
