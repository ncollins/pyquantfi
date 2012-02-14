from math import exp, log, sqrt
from random import normalvariate, lognormvariate, seed

def simpleMC8(option, spot, vol, r, N, gatherer, randomGen):
    randomGen.dim = 1
    expiry = option.expiry()
    var = vol.integralSq(0,expiry)
    rootVar = sqrt(var)
    itoCorrection = -0.5 * var

    movedSpot = spot * exp(r.integral(0,expiry) + itoCorrection)
    discounting = exp(-r.integral(0,expiry))
    
    gaussians = randomGen.getGaussians(N)
    spots = (movedSpot * exp(rootVar * v[0]) for v in gaussians)
    payoffs = (option.payoff(s) for s in spots)
    for p in payoffs:
        gatherer.addOneResult(discounting * p)

    return
