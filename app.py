import streamlit as st
from pandas_datareader.data import DataReader
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import plotting
import copy
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from io import BytesIO
from tvDatafeed import TvDatafeed, Interval
import vnquant.data as dt

pd.set_option('expand_frame_repr', False)

tv = TvDatafeed()

st.set_page_config(page_title = "Duy Chu's Stocks", layout = "wide")
st.header("Duy Chu's Stocks")

col1, col2 = st.columns(2)

with col1:
	start_date = st.date_input("Start Date")
	
with col2:
	end_date = st.date_input("End Date") # it defaults to current date
tickers = st.text_input('Nhập mã chứng khoán mà không có dấu cách, ví dụ: "TCB", "SSI", "VHC", "VHM", "HBC", "FPT", "HPG" ', ' ')
loader = dt.DataLoader([tickers], str(start_date), str(end_date), minimal=True, data_source = "cafe")

data= loader.download()
data=data.stack()
data=data.reset_index()
haf = data.pivot_table(values = 'adjust', index = 'date', columns = 'Symbols').dropna()

mu = expected_returns.mean_historical_return(haf)
S = risk_models.sample_cov(haf)
from pypfopt import plotting
plotting.plot_covariance(S)
ef = EfficientFrontier(mu, S)
raw_weights = ef.max_sharpe()
cleaned_weights = ef.clean_weights()
performance = ef.portfolio_performance(verbose=True)

ef = EfficientFrontier(mu, S)
ef.min_volatility()

from pypfopt import plotting
ef = EfficientFrontier(mu, S)
a= ef.min_volatility()
plotting.plot_weights(a)

from pypfopt import plotting
ef = EfficientFrontier(mu, S)
b=ef.max_sharpe()
plotting.plot_weights(b)

#HRP
from pypfopt import hierarchical_portfolio
returns = expected_returns.returns_from_prices(haf, log_returns=False)
hierarchical_portfolio.HRPOpt(returns,S)
hrp = hierarchical_portfolio.HRPOpt(returns,risk_models.sample_cov(haf))
weights_hrp=hrp.optimize()
hrp_performance = hrp.portfolio_performance(verbose=True)

#CVar
from pypfopt import efficient_frontier
cvar = efficient_frontier.EfficientCVaR(mu,returns,beta = 0.95,weight_bounds=(0, 1),verbose=False)
mincvar=cvar.min_cvar()
cvar_performance = cvar.portfolio_performance(verbose=True)

form = st.form(key="my_form")
submit1 = form.form_submit_button(label="Get data")
if submit1:
    st.write(haf)
    st.subheader("Optimized Max Sharpe Portfolio")
    st.write(cleaned_weights)
    st.write(performance)
 
    st.subheader("HRP")
    st.write(weight_hrp)
    st.write(hrp_performance)
  
    st.subheader("Min CVaR")
    st.write(cvar_performance)
