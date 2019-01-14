class Fitter(object):
    def __init__(self, xdata=None, ydata=None, model=None, params=None,
                 estimator=None):
        # Inputs
        self.xdata = xdata
        self.ydata = ydata
        self.xmin, self.xmax = None, None
        self.ymin, self.ymax = None, None
        self.model = model
        self.params = params
        self.estimator = estimator
        # Outputs
        self.popt = None
        self.pcov = None

    def set_data(self, x, y):
        self.xdata, self.ydata = x, y


