import yfinance as yf
import numpy as np
import pandas as pd
import sys
import os
import matplotlib as mpl
mpl.use('Qt5Agg')
import matplotlib.pyplot as plt
import talib
import math

from sklearn.metrics import confusion_matrix, classification_report

def is_coffee_and_handle(STK,START,END):
    price = yf.Ticker(STK).history(start=START,end=END, interval='1d').Close
    date = yf.Ticker(STK).history(start=START,end=END, interval='1d').index
    l = len(price)
    for i in range(l-1,0,-1):
        if price.iloc[i]>price.iloc[i-1]:
            j = i-1 #pivot1
            for k in range(j-1,0,-1):
                if price.iloc[k]>price.iloc[k-1]:
                    r = k #cup right point
                    for p in range(r-1,0,-1):
                        if price.iloc[p] >= price.iloc[r]:
                            print(str(price.iloc[j])+" "+str(date[j]))
                            fig,ax=plt.subplots()
                            ax.plot(price.iloc[p:j],label='Price')
                            ax.legend()
                            plt.show()
                            return True
    return False

dict = {'NVDA':('2015-12-30','2016-05-12')}
stocks = ['NVDA']#,'AMBA']
for stock in stocks:
    print("Is "+stock+" a good coffee? "+str(is_coffee_and_handle(stock,dict[stock][0],dict[stock][1])))
