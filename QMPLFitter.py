from QMPLWidget import QMPLWidget
from matplotlib.widgets import RectangleSelector

from PySide import QtGui

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
        print "Click @ (%.2f, %.2f) | Release @ (%.2f, %.2f)" \
              %(x1, y1, x2, y2)
        self.deactivate_fitter()

    def activate_fitter(self):
        self.fit_action.setChecked(True)
        self.selector.set_active(True)

    def deactivate_fitter(self):
        self.fit_action.setChecked(False)
        self.selector.set_active(False)
