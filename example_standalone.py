"""
Example script for testing interactive fitting as a standalone widget.
"""

import numpy as np
from QMPLFitter import QMPLFitterWidget

def gaus(x, a, b, c):
    """
    3-parameter Gaussian function.
    """
    return a*np.exp( -(x - b)**2 / (2*c**2) )

if __name__ == "__main__":
    num_vals = 100
    # Parameter for function
    a = 100
    b = 0
    c = 2.0
    x = np.linspace(-10, 10, num_vals)
    y = gaus(x, a, b, c)

    # Add some jitter to the values
    y += np.random.normal(loc=0, scale=10, size=num_vals)

    # Make the plot with interactive fitting
    fw = QMPLFitterWidget()
    fw.plot(x, y)

    # TODO: This should be done elsewhere
    # Initialize fitter
    fw.fitter.model = gaus
    fw.fitter.params = (a, b, c)
