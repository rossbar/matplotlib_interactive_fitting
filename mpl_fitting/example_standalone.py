"""
Example script for testing interactive fitting as a standalone widget.
"""

import numpy as np
from PySide import QtGui
from QMPLFitter import QMPLFitterWidget
from fitting import gaus

# Must have a QApplication instance before QWidget can be created.
# Without this blurb, it is not possible to run as a script
# (e.g. python example_standalone.py)
app = QtGui.QApplication.instance()
if not app:
    app = QtGui.QApplication([])

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

    # Call application run loop
#    app.exec_()
