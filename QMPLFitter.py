import numpy as np
from QMPLWidget import QMPLWidget
from matplotlib.widgets import RectangleSelector

from PySide import QtGui

from fitting import Fitter

class QMPLFitterWidget(QMPLWidget):
    """
    Qt4 Widget with matplotlib elements modified to include interactive
    fitting functionality.
    """
    def __init__(self, parent=None):
        # Initialize QMPLWidget
        super(QMPLFitterWidget, self).__init__(parent)

        # Add a rectangle selector widget for interactive fit selection
        self.selector = RectangleSelector(self.axes,
                                          self.rect_select_callback,
                                          drawtype="box",
                                          useblit=True,
                                          button=[1],
                                          minspanx=5,
                                          minspany=5,
                                          spancoords="pixels")
        self.selector.set_active(False)

        # Add a "fitter" object to the widget
        self.fitter = Fitter()

        # Modify navigation toolbar to include a fitting action/icon
        self.expand_toolbar()

    # TODO: This is hacky - look at subclassing the NavigationToolbar2Qt to 
    # get the desired behavior
    def expand_toolbar(self):
        """
        Modify the default navigation toolbar to include a new icon for 
        activating/deactivating an interactive fitter.
        """
        # Add a separator to the end of the toolbar
        self.mpl_toolbar.addSeparator()
        fit_icon = QtGui.QIcon("resources/gaus.svg")
        self.fit_action = self.mpl_toolbar.addAction(fit_icon,
                                                     "Interactive fitting",
                                                     self.activate_fitter)
        self.fit_action.setCheckable(True)

    def rect_select_callback(self, click_event, release_event):
        """
        Handle events from selector.
        """
        # TODO: Implement
        x1, y1 = click_event.xdata, click_event.ydata
        x2, y2 = release_event.xdata, release_event.ydata
        # Set the data subregion of the fitter
        self.fitter.xmin, self.fitter.xmax = x1, x2
        # Fit data
        self.fitter.fit()
        # Turn fitting action back off
        self.deactivate_fitter()

    def activate_fitter(self):
        self.fit_action.setChecked(True)
        self.selector.set_active(True)

    def deactivate_fitter(self):
        self.fit_action.setChecked(False)
        self.selector.set_active(False)

    # TODO: Explicit wrapper of axes.plot - figure out how to do this 
    # implicitly (class decorator? Populate obj dict with axes.__dict__?)
    def plot(self, *args, **kwargs):
        # Input parsing
        if len(args) == 1:
            y = args[0]
            x = np.arange(y)
        elif len(args) == 2:
            if(type(args[1]) == str):
                y = args[0]
                x = np.arange(y)
            else:
                x, y = args
        elif len(args) == 3:
            x, y = args[:-1]

        # Set fitter properties
        self.fitter.set_data(x, y)
        
        # Pass arguments along to axis method
        self.axes.plot(*args, **kwargs)
        # Render
        self.canvas.draw()
