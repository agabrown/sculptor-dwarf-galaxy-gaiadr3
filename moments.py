"""
Provides the following functions:
    - rse : Calculate the robust scatter estimate for a series of observations.
    - weighted_mean_twod : Calculate the weighted mean of a set of 2D vectors, accounting for the full covariance matrix of
      the measurement uncertainties on the vector components. Can be applied to, for example, proper motion data.

Anthony Brown Aug 2021 - Mar 2023
"""

import numpy as np
from numpy.linalg import inv
from scipy.special import erfinv
from scipy.stats import scoreatpercentile

__all__ = ["rse", "weighted_mean_twod"]

_rse_constant = 1.0 / (np.sqrt(2) * 2 * erfinv(0.8))


def rse(x):
    """
    Calculate the Robust Scatter Estimate for an array of values (see GAIA-C3-TN-ARI-HL-007).

    Parameters
    ----------
    x : float array
        Array of input values (can be of any dimension)

    Returns
    -------
    rse : float
        The Robust Scatter Estimate (RSE), defined as 0.390152 * (P90-P10),
        where P10 and P90 are the 10th and 90th percentile of the distribution
        of x.
    """
    return _rse_constant * (scoreatpercentile(x, 90) - scoreatpercentile(x, 10))


def weighted_mean_oned(x, sx):
    """
    Calculate the weighted mean for the measurements x with associated uncerainties sx.

    Parameters
    ----------
    x : float array (1D)
        Values of x
    sx : float array (1D)
        Uncertainties in x

    Returns
    -------
    wx : float
        Weighted mean of x.
    swx : float
        Uncertainty on the weighted mean.
    """
    w = np.sum(1 / sx * sx)
    wx = np.sum(x / sx * sx) / w
    return wx, np.sqrt(1.0 / w)


def weighted_mean_twod(x, y, sx, sy, cxy):
    r"""
    Provide the weighted mean of the vectors x and y.

    The elements :math:`(x_i, y_i)` have covariance matrices:

    .. math::

        \begin{pmatrix}
        s_x^2 & c_{xy}s_xs_y \\
        c_{xy}s_xs_y & s_y^2
        \end{pmatrix}

    Parameters
    ----------
    x : float array (1D)
        Values of x-component of data vector
    y : float array (1D)
        Values of y-component of data vector
    sx : float array (1D)
        Uncertainties in x
    sy : float array (1D)
        Uncertainties in y
    cxy : float array (1D)
        Correlation coefficient of sx and sy

    Returns
    -------
    wx, wy : float
        Weighted means wx, wy.
    covw : float array (2,2)
        Covariance matrix of the weighted mean.
    """
    ndata = x.size
    cinv = np.zeros((2 * ndata, 2 * ndata))
    cov = np.zeros((2, 2))
    mat_a = np.zeros((2 * ndata, 2))
    vec_b = np.zeros(2 * ndata)
    for j in range(0, 2 * ndata, 2):
        mat_a[j] = [1, 0]
        mat_a[j + 1] = [0, 1]
        k = int(j / 2)
        vec_b[j] = x[k]
        vec_b[j + 1] = y[k]
        cov[0, 0] = sx[k] ** 2
        cov[1, 1] = sy[k] ** 2
        cov[1, 0] = sx[k] * sy[k] * cxy[k]
        cov[0, 1] = cov[1, 0]
        cinv[j : j + 2, j : j + 2] = inv(cov)
    covw = inv(np.dot(mat_a.T, np.dot(cinv, mat_a)))
    wx, wy = np.dot(covw, np.dot(mat_a.T, np.dot(cinv, vec_b)))
    return wx, wy, covw
