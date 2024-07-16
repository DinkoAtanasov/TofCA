
import math
import numpy as np
import warnings
from scipy import constants
from scipy.optimize import curve_fit
from configparser import ConfigParser


class CfgParser(ConfigParser):
    """
    ConfigParser with a custom dictionary conversion method.
    """

    def as_dict(self) -> dict:
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d

    def dict_to_parser(self, d) -> None:
        """
        Convert modified settings from dictionary to ConfigParser variables.
        Dict of dicts, i.e. {Section1:{field:value, ...}, Section2:{field:value,...}}
        :return:
        """
        self.read_dict(d)


def str_with_err(value, error):
    if error < 1:
        digits = int(abs(math.floor(math.log10(error))))
        return f'{value: .{digits}f}({error * 10 ** digits:.0f})'
    else:
        return f'{value: .0f}({round(error):.0f})'


def format_stats(opt, std, units='ns'):
    # return f'Mean = {opt[1]:.3f} +/- {std[1]:.3f}\nFWHM = {opt[2]*2.35:.3f} +/- {std[2]*2.35:.3f}'
    return f'Mean = {str_with_err(opt[1], std[1])} {units}\nFWHM = {str_with_err(opt[2], std[2])} {units}'


def gauss_parameters(opt, unc):
    a = 'A0'
    p0 = str_with_err(opt[0], unc[0])
    m = 'Mean'
    p1 = str_with_err(opt[1], unc[1])
    s = 'Std'
    p2 = str_with_err(opt[2], unc[2])
    bl = 'BaseL'
    p3 = str_with_err(opt[3], unc[3])
    fwhm = 'FWHM'
    pf = str_with_err(stdev_to_fwhm(opt[2]), stdev_to_fwhm(unc[2]))
    text = f'{a:8} = {p0: <12}\n{m:6} = {p1: <12}\n{s:8} = {p2: <12}\n{bl:6} = {p3: <12}\n{fwhm:6} = {pf: <10}'
    return text


def stdev_to_fwhm(val: float) -> float:
    return 2 * np.sqrt(2 * np.log(2)) * val


def gauss(x, Ampl=1, Center=0, Sigma=0.5, Baseline=0) -> float:
    """
    This is a method from the Pynalyse's class returning a point on a gaussian distribution

    :param x: The variable for Gaussian distribution
    :param Ampl: Amplitude
    :param Center: Mean
    :param Sigma: Standard deviation
    :param Baseline: Baseline for non-zero background
    :return: expectation value of the Gaussian distribution at x
    """
    return Ampl * np.exp(-((x - Center) ** 2) / (2 * Sigma ** 2)) + Baseline


def edges_to_center(values: list) -> list:
    xc = []
    for i in range(len(values) - 1):
        xc.append((values[i] + values[i + 1]) / 2)
    return xc


def fit_simple_gauss(data: tuple, view_xrange: tuple) -> tuple:
    """
    Fit a Gaussian function over data received from a pyqtgraph PlotItem.

    This is simplification and not the general case:
    Thus, the x values would arrive in this method either from
    a) histogram with x = y + 1 values or
    b) curve plot with x = y values

    :param data: Tuple containing the x and y vectors (x, y)
    :param view_xrange: tuple or list of the zoomed view of the PlotItem
    :return:
    """
    xlo = view_xrange[0]
    xhi = view_xrange[1]
    x_origin = data[0]  # This should correspond to bin edges and will have a shape(Y+1)
    y_origin = data[1]

    xc = edges_to_center(x_origin) if x_origin.shape != y_origin.shape else x_origin

    transformed_data = np.array([xc, y_origin])
    cut = (transformed_data >= xlo) & (transformed_data <= xhi)
    selection = transformed_data[:, cut[0]]

    x = selection[0]
    y = selection[1]

    bnds = ([0, xlo, 0, 0],
            [np.max(y)*10+1, xhi, xhi - xlo, np.max(y)*0.009])
    p_init_guess = [np.max(y), np.average(x, weights=y), 0.3 * (xhi - xlo), 0.]
    return curve_fit(gauss, x, y, p0=p_init_guess, bounds=bnds)