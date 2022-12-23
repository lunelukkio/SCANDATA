"""A test model consisting of a simple function.

Contains:

* powerplot    Function that provides (x, y) data suitable for matplotlib 
               plotting.
"""

import numpy as np


def powerplot(base, exponent):
    """
    Calculates data for plotting the function: y = (base * x) ** exponent,
    for x = 0...10.
    Arguments: base and exponent as floats
    Returns: two numpy arrays of x and y coordinates (length 800).
    """

    x = np.linspace(0, 10, 800)
    y = (x * base) ** exponent
    return x, y
