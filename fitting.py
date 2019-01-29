import numpy as np
from scipy.optimize import curve_fit

def gaus(x, a, b, c):
    """
    3-parameter Gaussian function.
    """
    return a*np.exp( -(x - b)**2 / (2*c**2) )

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

    @property
    def perr(self):
        if self.popt is None or self.pcov is None: return None
        return np.sqrt(np.diag(self.pcov))

    def set_data(self, x, y):
        self.xdata, self.ydata = x, y

    def fit(self):
        self.popt, self.pcov = curve_fit(self.model, self.xf, self.yf, p0=self.params)
