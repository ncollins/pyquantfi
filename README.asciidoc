PyQuantFi README
===================
Nick Collins <nick@vividx.co.uk>
:Author Initials: NJC
:website: https://github.com/ncollins/pyQuantFi

Overview
--------
PyQuantFi is a simple quantitative finance library written in Python.
It is adapted from the framework in the book "C++ Design Patterns and 
Derivatives Pricing" by Mark Joshi. Currently it has features covered in 
the first 6 chapters, including classes for options, payoffs, parameters, 
random number generators and statistics gathering.

PyQuantFi only requires the Python Standard Library, it does not
use any additional libraries written in C (e.g. NumPy, SciPy). 
This limits its speed when running on CPython but means
it will run on a wider range of Python implementations, including
PyPy, Jython and Google App Engine.

Known Issues
------------
I have tested the code on the following Python implementations:

- Python 2.5, Mac OS X
- Python 3.1, Mac OS X
- PyPy 1.4 (2.5 compliant), Mac OS X
- Jython 2.5, Mac OS X
- Python 2.6, Ubuntu GNU/Linux
- PyPy 1.4 (2.5 compliant), Ubuntu GNU/Linux

Both Python 3.1 and PyPy 1.4 on Mac OS X produce results inconsisent
with the other implementations. I'm still in the process of tracking
down the reasons for this.

While I've performed a few "reasonability" tests against QuantLib
(using RQuantLib), but I'm not yet willing to endorse the acuracy of 
the results. I intend to add some more extensive testing scripts in
the future.
