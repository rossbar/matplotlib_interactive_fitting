import numpy as np
from QMPLWidget import QMPLWidget
from matplotlib.widgets import RectangleSelector

from PySide import QtGui

from fitting import Fitter

# Make the package importable from anywhere on the system (fix broken links
# to QIcon .svg)
import os
RESOURCE_PATH = os.path.join(os.path.dirname(__file__), "resources")

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
        # Artists to go along with fitter
        self.fit_line = None
        self.fit_textbox = None

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
        
        # Add interactive fit action
        fit_icon = QtGui.QIcon("/".join((RESOURCE_PATH, "gaus.svg")))
        self.fit_action = self.mpl_toolbar.addAction(fit_icon,
                                                     "Interactive fitting",
                                                     self.activate_fitter)
        self.fit_action.setCheckable(True)

        # Add fit-clearing action
        clearfit_icon = QtGui.QIcon("/".join((RESOURCE_PATH, "clear.svg")))
        self.clearfit_action = self.mpl_toolbar.addAction(clearfit_icon,
                                                          "Clear current fit",
                                                          self.clear_fit)

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
        self.show_fit()
        # Turn fitting action back off
        self.deactivate_fitter()

    def activate_fitter(self):
        self.fit_action.setChecked(True)
        self.selector.set_active(True)

    def deactivate_fitter(self):
        self.fit_action.setChecked(False)
        self.selector.set_active(False)

    # TODO: The functionality in this method should be moved to the Fitter
    # class. See branch feat/fitter_textbox for aborted attempt
    def generate_text_summary(self):
        """
        Summarize the results presenting the optimal parameters in text
        """
        # Return None if no optimized params to summarize
        if self.fitter.popt is None: return
        hdr = "Optimal Parameters $(\pm 1\sigma)$:\n"
        # Summarize fit results
        summary = "\n".join(["  p[%s] = %.3f $\pm$ %.3f" %(p, val, err) for \
                             p, (val, err) in enumerate(zip(self.fitter.popt, self.fitter.perr))])
        return hdr + summary

    def show_fit(self):
        """
        Draw the model with the optimized params on the axis.
        """
        # Generate x-values in ROI at 2x density of actual data
        x = np.linspace(self.fitter.xmin, self.fitter.xmax,
                        2 * self.fitter.xf.shape[0])
        y = self.fitter.model(x, *self.fitter.popt)
        # TODO: How to choose/set the color/texture of fitted model
        self.fit_line = self.axes.plot(x, y, "m-")[0]
        # Add a textbox summarizing the fit
        # TODO: Customize where/how summary of text shows up. Currently, have
        # textbox pop up in upper-left corner
        self.fit_textbox = self.axes.text(0.0, 1.0,   # Axes coordinates
                                          self.generate_text_summary(),
                                          horizontalalignment="left",
                                          verticalalignment="top",
                                          transform=self.axes.transAxes,
                                          bbox={"facecolor" : "yellow",
                                                "alpha"     : 0.5,
                                                "pad"       : 0})
        self.canvas.draw()

    def clear_fit(self):
        """
        Remove artists associated with interactive fitting from the canvas.
        """
        if self.fit_line is not None:
            self.axes.lines.remove(self.fit_line)
            self.fit_line = None
        if self.fit_textbox is not None:
            self.fit_textbox.remove()
            self.fit_textbox = None
        self.canvas.draw()

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

    def hist(self, *args, **kwargs):
        # Create histogram first
        h, be, _ = self.axes.hist(*args, **kwargs)
        # Set fitter
        # TODO: Assumes regular binning
        bc = be[:-1] + np.diff(be)[0] / 2
        self.fitter.set_data(bc, h)
        # Render
        self.canvas.draw()

