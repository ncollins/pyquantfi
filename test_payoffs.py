# PyQuantFi - payoffs.py
# (c) 2012 Nick Collins
# Designed to be used with py.test

from payoffs import VanillaCall, VanillaPut, DigitalCall, DigitalPut

def test_vanilla_call_0():
    p = VanillaCall(100)
    assert (p(150),p(100),p(50),p(0)) == (50, 0, 0, 0)

def test_vanilla_call_1():
    p = VanillaCall(100)
    assert 0 == round(p(100.00001) - 0.00001,5)
    
def test_vanilla_put_0():
    p = VanillaPut(100)
    assert (p(150),p(100),p(50),p(0)) == (0, 0, 50, 100)

def test_vanilla_put_1():
    p = VanillaPut(100)
    assert 0 == round(0.00001 - p(99.99999),5)

def test_digital_call():
    p = DigitalCall(60)
    assert (p(60.00001),p(60),p(59.99999)) == (1, 0, 0)

def test_digital_put():
    p = DigitalPut(60)
    assert (p(60.00001),p(60),p(59.99999)) == (0, 0, 1)
