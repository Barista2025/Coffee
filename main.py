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

from sklearn.metrics import confusion_matrix, classification_report

def is_coffee_and_handle(STK,START,END):
    time.sleep(2)  # 每支股票之間等 2 秒
    price = yf.Ticker(STK).history(start=START,end=END, interval='1d').Close
    date = yf.Ticker(STK).history(start=START,end=END, interval='1d').index
    l = len(price)
    for i in range(l-1,0,-1):
        if price.iloc[i]>price.iloc[i-1]:
            j = i-1 #pivot1
            
            # 條件：往前推35天內，是否有價格 >= price[j]
            lookback_window = 35
            left_found = False
            for t in range(j - lookback_window):
                if price.iloc[t] >= price.iloc[j]:
                    left_found = True
                    left_idx = t
                    break
            if not left_found:
                continue  # 不符合右緣條件，繼續往前掃
            
            handle_right=j-1
            for k in range(j-1,0,-1):
                if price.iloc[k]>price.iloc[k-1]:
                    r = k #cup right point
                    for p in range(r-1,0,-1):
                        if price.iloc[p] > price.iloc[r]:
                            print("Found potential Cup and Handle")
                            print(f"Right edge price: {price.iloc[handle_right]:.2f} @ {date[handle_right].date()}")
                            print(f"Left point higher than right: {price.iloc[left_idx]:.2f} @ {date[left_idx].date()}")
                            print(str(price.iloc[handle_right])+" "+str(date[handle_right]))
                            fig,ax=plt.subplots()
                            ax.plot(price.iloc[left_idx:handle_right+1],label='Price')
                            ax.plot(date[p], price.iloc[p], 'ro', label='Cup Bottom')
                            ax.plot(date[handle_right], price.iloc[handle_right], 'bo', label='Right Edge')
                            ax.plot(date[left_idx], price.iloc[left_idx], 'go', label='Left High')
                            ax.legend()
                            y_min = price.iloc[left_idx:handle_right+1].min()
                            y_max = price.iloc[left_idx:handle_right+1].max()
                            ax.set_ylim(y_min * 0.95, y_max * 1.10)  # 下壓 5%、上留 10%
                            ax.yaxis.set_major_locator(mticker.MaxNLocator(nbins=30))  # 最多顯示 10 格
                            
                            
                            plt.show()
                            return True
    return False

dict = {'NVDA':('2015-12-30','2016-05-12')}
stocks = ['NVDA']#,'AMBA']
for stock in stocks:
    print("Is "+stock+" a good coffee? "+str(is_coffee_and_handle(stock,dict[stock][0],dict[stock][1])))
