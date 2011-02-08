
class VanillaOption(object):
    
    def __init__(self,payoff,expiry):
        self._payoff = payoff
        self._expiry = expiry

    def payoff(self,*args):
        return self._payoff(*args)

    def expiry(self):
        return self._expiry
   
