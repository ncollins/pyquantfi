# PyQuantFi - options.py
# (c) 2012 Nick Collins

class VanillaOption(object):
    
    def __init__(self,payoff,expiry):
        self.payoff = payoff
        self.expiry = expiry
