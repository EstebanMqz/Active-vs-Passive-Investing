
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: visualizations.py : python script with data visualization functions                         -- #
# -- author: EstebanMqz                                                                                  -- #
# -- license: GNU General Public License v3.0                                                            -- #
# -- repository: https://github.com/EstebanMqz/MS_Lab1_Marquez-Delgado-Esteban                           -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go #plotly
import plotly.express as px
from data import *


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_rep', True)
pd.set_option('display.width', None)


def hist_csv(df, title, tickers, weights):
    """
    Function that returns histogram of tickers and weights of portfolio in a df.

        Parameters
        ----------
        df: Tickers and Weights of stocks in a dataframe.
        title: Title of the histogram.
        tickers: Column with tickers as str.
        weights: Column with tickers as str.

        Returns
        -------
        histogram of Tickers and Weights of the portfolio in a df.
    """
    fig = px.histogram([0,1], x=df[tickers], y= df[weights], title=title, color=df[tickers])
    fig.update_xaxes(categoryorder = 'total descending')
    fig.update_layout( yaxis = dict( tickfont = dict(size=9)), xaxis_title=tickers, yaxis_title=weights)
    fig.show()


def stocks_summary(s0,St, W, capital, returns, mean_ret):

    """
    Function that returns a stock summary of the behavior of a portfolio in a given date 
    with known initial global investment, returns of assets, weights and S0 and St.

        Parameters
        ----------
        s0: Initial price in a dataframe of 1*n.
        St: Last price in a dataframe of 1*n.
        W: Weights of holdings as an array.
        capital: Scalar of capital amount.
        returns: Dataframe of holdings returns.
        mean_ret: Mean returns of holdings.

        Returns
        -------
        A dataframe with the behavior of Holdings (S_0, S_t, Owned Titles, Initial_investment, Return and Volatility in a given period).
    """
    stocks_summary = pd.DataFrame({"S_0": s0.values.flatten(), "S_t": St.values.flatten(), "Rounded_Titles": (((W*capital/s0).round()).values.flatten()),
    "Initial_Investment": ((((W*capital/s0).round())*s0).values.flatten()), "Return" : mean_ret, "Volatility" : returns.std()*np.sqrt(252)})

    return stocks_summary 

def port_pasivo(returns, W, capital, I_inv, com, cash):

    """
    Function that returns the individual capital behavior in holdings from a portfolio in a given date 
    and calculates the total capital, portfolio returns and acummulated returns on a daily basis.

        Parameters
        ----------
        returns: Dataframe of holdings returns.
        W: Weights of holdings as an array.
        capital: Scalar of capital amount.
        initial_investment: Amount of the capital invested in a hldgs portfolio.
        com: Commission of transactions (Buy/Sell).
        cash: Amount of capital not invested (Capital - initial_investment).

        Returns
        -------
        A dataframe with the behavior of Holdings (S_0, S_t, Owned Titles, Initial_investment, Return and Volatility in a given period).
    """

    port_pas=returns.mul(W*capital, axis=1)
    port_pas["Capital"] = port_pas.sum(axis=1)
    port_pas["Capital"][0] = I_inv*com+I_inv+cash
    port_pas["Capital"]=port_pas["Capital"].cumsum()

    port_pas["Portfolio Returns"] = port_pas["Capital"].pct_change()
    port_pas["Portfolio Returns"][0] = (I_inv*com)/capital #Charged on investment day (0).

    port_pas["Accumulated Returns"] = (port_pas["Portfolio Returns"] + 1).cumprod()
    port_pas.index.name="timestamp"
    port_pas.round(6)
    return port_pas


def df_pasiva(port_pas):
    
    """
    Function that converts the capital in a portfolio, its returns and accumulated returns to a monthly basis.

        Parameters
        ----------
        port_pas: Dataframe that contains 'Capital', 'Portfolio Returns' and 'Accumulated Returns' columns in order.

        Returns
        -------
        A monthly dataframe of the Capital the Monthly Return and Accumulated Return for the investment in a period.
    """

    df_pasiva=port_pas[['Capital', 'Portfolio Returns', 'Accumulated Returns']]
    df_pasiva=df_pasiva.iloc[port_pas.iloc[: , -3:].reset_index().groupby(port_pas.iloc[: , -3:].index.to_period('M'))['timestamp'].idxmax()]
    return df_pasiva

def plot(metric, title, xlabel, ylabel):

    """
    Function that converts the capital in a portfolio, its returns and accumulated returns to a monthly basis.

        Parameters
        ----------
        port_pas: Dataframe that contains 'Capital', 'Portfolio Returns' and 'Accumulated Returns' columns in order.

        Returns
        -------
        A monthly dataframe of the Capital the Monthly Return and Accumulated Return for the investment in a period.
    """
    #Line Style
    plt.style.use('dark_background')
    plt.rc('grid', linestyle="--", color='gray')
    plt.rc('ytick', labelsize=13, color='yellow')
    plt.rc('xtick', labelsize=11, color='white')

    #Plot
    metric.plot(figsize = (16,8),color='g',
    label=('Final Value=',metric.iloc[-1]))

    #General Style
    plt.title(title, size='17', weight='bold', family="Constantia")
    plt.xlabel(xlabel, size='15', weight='roman', family="Georgia")
    plt.ylabel(ylabel, size='15', weight='bold', family="Georgia", color='g')
    plt.grid(True)
    plt.legend(loc = "best")
    plt.show()

def plotly_graph(x, y, x_label, y_label, title):
    """
    Function that plots a line+marker graph with plotly.

        Parameters
        ----------
        x: index from Dataframe of selected metric to graph with plotly.
        y: Values of the selected of selected metric to graph with plotly.
        title: Title of the plot.
        x_label: Variable name in the label x.
        y_label: Variable name in the label y.

        Returns
        -------
        Returns a didactic graph with plotly of the selected metric.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers',
    name=y_label, line=dict(color='black'), marker=dict(symbol=3, color='green')))
    fig.update_layout(title=title, xaxis_title=x_label, yaxis_title=y_label)
    fig.update_xaxes(showspikes=True)
    fig.update_yaxes(showspikes=True)

    return fig.show()
