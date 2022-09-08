"""
# -- ----------------------------------------------------------------------------------------------------  -- #
# -- project: This project evaluates ETF IShares NAFTRAC Active and Passive Investment defined strategies. -- #
# -- script: data.py : python script for data collection                                                   -- #
# -- author: oscaralfonso17                                                                                -- #
# -- license: GPL-3.0 License                                                                              -- #
# -- repository: https://github.com/oscaralfonso17/myst_if710183_lab1.git                                  -- #
# -- ----------------------------------------------------------------------------------------------------  -- #
"""

from os import listdir
from os.path import isfile, join
import pandas as pd
import pandas_datareader as pdr
from datetime import datetime


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_rep', True)
pd.set_option('display.width', None)

def read_csv(data):
    """
    Function that reads csv files and returns a dataframe of its content.

        Parameters
        ----------
        data: csv data.

        Returns
        -------
        data: pd.DataFrame(data)
    """
    df = pd.read_csv(data)
    return df

def yf_adjclose(tickers, start, end):

    """
    Function that downloads and returns yahoo finance ticker(s) adj. closes.

        Parameters
        ----------
        tickers: ticker(s) to download as a list.
        start: datetime.datetime(y,m,d)
        end: datetime.datetime(y,m,d)

        Returns
        -------
        data: pd.DataFrame(data)
    """
    #Daily Adj. closes df 
    df = pdr.DataReader(tickers,'yahoo',start,end)["Adj Close"] #Adj. closes download
    return df



