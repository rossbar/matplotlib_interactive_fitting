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
    # ************** Plot example
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
    fw.setWindowTitle('Plot Example')
    fw.plot(x, y)

    # TODO: This should be done elsewhere
    # Initialize fitter
    fw.fitter.model = gaus
    fw.fitter.params = (a, b, c)

    # ************** Hist example
    num_vals = 10000
    # Parameters for distribution
    centroid = 10.0
    sigma = 3.0
    vals = np.random.normal(centroid, sigma, num_vals)

    # Test the histogramming with some kwargs
    fw = QMPLFitterWidget()
    fw.setWindowTitle('Hist Example')
    fw.hist(vals, bins=100, histtype="step", log=False);

    # Set the fitter model
    fw.fitter.model = gaus
