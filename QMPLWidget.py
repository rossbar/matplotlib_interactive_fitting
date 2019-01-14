"""
Matplotlib-based widgets incorporated into QWidget container to support
custom functionality.

Largely derived from `matplotlib user interface examples 
<https://matplotlib.org/examples/user_interfaces/index.html>`_.
"""

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.widgets import RectangleSelector

from PySide import QtCore, QtGui

class QMPLWidget(QtGui.QWidget):
    """
    Qt4 Widget container for matplotlib artists & canvas.
    """
    def __init__(self, parent=None, axes=(1, 1), fig_facecolor="none"):
        """
        Create a new QMPLWidget.
        """
        # Parent constructor
        super(QMPLWidget, self).__init__(parent)
        # TODO: switch from pyplot API to OO API
        self.fig, self.axes = plt.subplots(*axes)
        self.canvas = FigureCanvas(self.fig)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self, coordinates=False)

        # Set figure facecolor
        self.fig.patch.set_facecolor(fig_facecolor)

        # Setup and apply layout
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.mpl_toolbar)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

        # Initial render
        # TODO: is this necessary? Check for both standalone and embedded use
        # cases
        self.canvas.draw()
