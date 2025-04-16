import yfinance as yf
import numpy as np
import pandas as pd
import sys 
import os
import matplotlib as mpl 
mpl.use('Qt5Agg')
import matplotlib.pyplot as plt 
import matplotlib.ticker as mticker
import talib
import math
import time
from utility import is_coffee_and_handle 

fp = open("history/stock_list.txt","r")
stocks = fp.read().split('\n')[:-1]
for stock in stocks:
    print(stock)
    df = pd.read_csv('history/'+stock+'.csv', date_format="%m/%d/%Y")
    is_coffee_and_handle(stock,df,2)
