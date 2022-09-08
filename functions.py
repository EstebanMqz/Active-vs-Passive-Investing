"""
# -- ----------------------------------------------------------------------------------------------------  -- #
# -- project: This project evaluates ETF IShares NAFTRAC Active and Passive Investment defined strategies. -- #
# -- script: functions.py : python script with general functions                                           -- #
# -- author: EstebanMqz                                                                                    -- #
# -- license: GNU General Public License v3.0                                                              -- #
# -- repository: https://github.com/EstebanMqz/MS_Lab1_Marquez-Delgado-Esteban                             -- #
# -- ----------------------------------------------------------------------------------------------------  -- #
"""

import numpy as np
import plotly.graph_objects as go #plotly
import plotly.express as px
from data import *


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_rep', True)
pd.set_option('display.width', None)


def s_metrics(prices):
    """
    Function that calculates daily simple return metrics of prices.

        Parameters
        ----------
        prices: dataframe of price(s).

        Returns
        -------
        returns: Simple returns on a daily basis.
        mean_returns: Mean of returns (annualized).
        cov: Covariance (annualized).
        index: Name of the metrics dataframe calculated as str.
    """
    returns = prices.pct_change().fillna(0) #NAs filled w/ 0s to preserve daily returns for all rows (days) in every column (ticker)
    mean_ret = returns.mean() * 252 #E(r)
    cov = returns.cov() * 252 #Covariance

    return returns, mean_ret, cov

def log_metrics(prices):
    """
    Function that calculates daily simple return metrics of prices.

        Parameters
        ----------
        prices: dataframe of price(s).

        Returns
        -------
        returns: Simple returns on a daily basis.
        mean_returns: Mean of returns (annualized).
        cov: Covariance (annualized).
        index: Name of the metrics dataframe calculated as str.
    """
    # Mean, Std, and Covariance from returns.
    returns = prices.pct_change().fillna(0) #NAs filled w/ 0s to preserve daily returns for all rows (days) in every column (ticker)
    log_ret = np.log(1+returns)
    mean_lr = log_ret.mean() * 252
    mean_ret = returns.mean() * 252 #E(lr)
    cov = returns.cov() * 252 #Covariance

    return returns, log_ret, mean_lr, mean_ret, cov

def optimize(mean_lr):
    """
    Function that calculates bounds and constraints neccesary for 
    Minimum Variance Portfolio with a given set of assets returns
    and Markowitz EMV portfolio.
    
        Parameters
        ----------
        mean_lr: mean logarithmic returns of given returns.
    
        Returns
        -------
        bnds: Simple returns on a daily basis.
        cons: Mean of returns (annualized).
        w0: Vector of ones of len(mean_lr)

    """
    N = len(mean_lr)
    w0 = np.ones(N) / N
    bnds = ((0, None), ) * N
    cons = {"type" : "eq", "fun" : lambda w : w.sum() - 1}

    return w0, bnds, cons


# Variance minimization function
def Var(w, cov):
    return np.dot(w.T, np.dot(cov, w))
