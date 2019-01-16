"""
Matplotlib-based widgets incorporated into QWidget container to support
custom functionality.

Largely derived from `matplotlib user interface examples 
<https://matplotlib.org/examples/user_interfaces/index.html>`_.
"""

import matplotlib
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

from PySide import QtCore, QtGui

class QMPLWidget(QtGui.QWidget):
    """
    Qt4 Widget container for matplotlib artists & canvas.
    """
    def __init__(self, parent=None, axes=111, fig_facecolor="none"):
        """
        Create a new QMPLWidget.
        """
        # Parent constructor
        super(QMPLWidget, self).__init__(parent)

        # Set up figure, axes, figure canvas, and navigation bar
        self.fig = Figure()
        self.axes = self.fig.add_subplot(axes)
        self.canvas = FigureCanvas(self.fig)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self, coordinates=False)
        # Add a label for current mouse position
        self.loc_label = QtGui.QLabel("POSITION INFO HERE", self.canvas)
        self.loc_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        self.loc_label.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))

        # Get rid of ugly white/gray border around figure object in widget
        self.fig.patch.set_facecolor(fig_facecolor)

        # Setup and apply layout
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.mpl_toolbar)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.loc_label)
        self.setLayout(self.layout)

        # Initial render
        # TODO: is this necessary? Check for both standalone and embedded use
        # cases
        self.canvas.draw()
        self.show()
