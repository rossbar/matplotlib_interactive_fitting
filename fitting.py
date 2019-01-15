import numpy as np
from scipy.optimize import curve_fit

class Fitter(object):
    def __init__(self, xdata=None, ydata=None, model=None, params=None,
                 estimator=None):
        # Inputs
        self.xdata = xdata
        self.ydata = ydata
        self.xmin, self.xmax = None, None
        self.model = model
        self.params = params
        self.estimator = estimator
        # Outputs
        self.popt = None
        self.pcov = None

    @property
    def data_mask(self):
        return np.logical_and(self.xdata >= self.xmin,
                              self.xdata <= self.xmax)
    @property
    def xf(self):
        return self.xdata[self.data_mask]
    
    @property
    def yf(self):
        return self.ydata[self.data_mask]

    def set_data(self, x, y):
        self.xdata, self.ydata = x, y

    def fit(self):
        self.popt, self.pcov = curve_fit(self.model, self.xf, self.yf, p0=self.params)
