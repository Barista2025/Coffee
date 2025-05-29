import yfinance as yf
import numpy as np
import pandas as pd
import sys
import os
import time
import numpy as np
import requests

def get_stock_list(li = -1):
    API_KEY = "d0s38k1r01qumepheougd0s38k1r01qumepheov0"
    symbol = "AMBA"
    url0 = f"https://finnhub.io/api/v1/stock/earnings?symbol={symbol}&token={API_KEY}"
    url = f"https://finnhub.io/api/v1/calendar/earnings?from=2019-01-02&to=2024-01-02&symbol={symbol}&token={API_KEY}"
    res = requests.get(url0)
    print(res.json())
    '''
    for item in res.json():
        print(item)
    stock_list = ['AMBA','META','NVDA','TSLA']
    fp = open("history/stock_list.txt","r")
    stocks = fp.read().split('\n')[:-1]
    for stock in stocks:
        print(stock)
        df = pd.read_csv('history/'+stock+'.csv', date_format="%m/%d/%Y")

    return stock_list'''

get_stock_list()
