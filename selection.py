import yfinance as yf
import numpy as np
import pandas as pd
import sys
import os
import time
import numpy as np
import requests

def get_stock_list(li = -1,catg = 4):
    stock_list = []
    fp = open("history/stock_list.txt","r")
    stocks = fp.read().split('\n')[:-1]
    for stock in stocks:
        #print(f"{stock}")
        price = pd.read_csv('history/'+stock+'.csv', date_format="%m/%d/%Y").Close
        volume = pd.read_csv('history/'+stock+'.csv', date_format="%m/%d/%Y").Volume
        MA20 = price.rolling(20).mean()
        if price.iloc[li]>MA20.iloc[li]:
            stock_list.append((stock,volume.iloc[li]))
    stock_list = sorted(stock_list, key=lambda x: x[1],reverse=True)
    print(stock_list[0:catg])
    return stock_list[0:catg]
