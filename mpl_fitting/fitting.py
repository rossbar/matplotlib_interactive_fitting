import numpy as np
from scipy.optimize import curve_fit

def gaus(x, a, b, c):
    """
    3-parameter Gaussian function.
    """
    return a*np.exp( -(x - b)**2 / (2*c**2) )

def lin(x, m, b):
    """
    Linear function, m = slope, b = intercept.
    """
    return m*x + b

def gaus_pol1(x, a, b, c, m, yint):
    """
    Gaussian function on top of linear background.
    """
    return gaus(x, a, b, c) + lin(x, m, yint)

def gaus_pol1_param_estimator(x, y):
    """
    Use input x, y data to determine initial parameter estimates for the 
    gaus_pol1 model.
    """
    # Amplitude estimate
    a = np.max(y)
    # Centroid
    b = x[np.argmax(y)]
    # Std. dev
    half_max_domain = x[np.where(y > 0.5*a)]
    fwhm = half_max_domain[-1] - half_max_domain[0]
    c = fwhm / 2.355
    # Linear slope
    m = (y[-1] - y[0]) / (x[-1] - x[0])
    # Y-intercept of line
    yint = y[0] - m*x[0]
    # Return parameter estimates
    return (a, b, c, m, yint)

class Fitter(object):
    def __init__(self, xdata=None, ydata=None, model=gaus_pol1,
                 estimator=gaus_pol1_param_estimator):
        # Inputs
        self.xdata = xdata
        self.ydata = ydata
        self.xmin, self.xmax = None, None
        self.model = model
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
        """
        Find optimal parameter estimates using scipy.curve_fit
        """
        # Initialize parameter estimates
        if self.estimator is not None:
            param_estimates = self.estimator(self.xf, self.yf)
        else: param_estimates = None
        self.popt, self.pcov = curve_fit(self.model, self.xf, self.yf, 
                                         p0=param_estimates)
