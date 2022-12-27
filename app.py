
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

st.write(data)