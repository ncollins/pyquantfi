PyQuantFi README
================================================================================
Nick Collins <nick@vividx.co.uk>

[https://github.com/ncollins/pyquantfi](https://github.com/ncollins/pyquantfi)

Overview
--------------------------------------------------------------------------------
PyQuantFi is a simple quantitative finance library written in Python.
It is adapted from the approach in the book "C++ Design Patterns and 
Derivatives Pricing" by Mark Joshi, but with a more "pythonic" style. 
Currently it has features covered in the first 6 chapters, including classes
for options, payoffs, parameters, random number generators and statistics
gathering.

PyQuantFi only requires the Python Standard Library, it does not
use any additional libraries written in C (e.g. NumPy, SciPy). 
This limits its speed when running on CPython but means
it will run on a wider range of Python implementations, including
PyPy and Jython.

While I've performed a few "reasonability" tests against QuantLib
(using RQuantLib), I'm not yet willing to endorse the acuracy of 
the results. I intend to add some more extensive testing scripts in
the future.
