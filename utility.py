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

def is_coffee_and_handle(STK,DF=None,MODE=0):
    if (MODE == 1) or (MODE == 3): 
        os.system("rm -rf image/"+STK+"/*.png")
    if MODE>=2:
        os.system("rm -rf image/"+STK+"/report.txt")
    if DF is None:
        time.sleep(2)  # 每支股票之間等 2 秒
        price = yf.Ticker(STK).history(period='5y', interval='1d').Close
        vol = yf.Ticker(STK).history(period='5y', interval='1d').Volume
    else:
        price = DF.Close
        vol = DF.Volume
        price.index = pd.to_datetime(DF.Date,utc = True,format='ISO8601')
        #price.index = DF.index.strftime("%d/%m/%Y")
    price50 = price.rolling(50).mean()
    l = len(price)
    handle_arr = []
    next_cup = False
    cup_id = 1 
    i = l-1 
    while i>0:
        if price.iloc[i]>price.iloc[i-1]:
            j = i-1 #pivot1
            # 條件：往前推35天內，是否有價格 >= price[j]
            lookback_window = 35
            handle_right=j
            for k in range(j-1,0,-1):
                if next_cup:
                    next_cup = False
                    break
                if price.iloc[k]<price.iloc[j]:
                    break
                if price.iloc[k]>price.iloc[k-1]:
                    r = k #cup right point
                    if ((j-r)>10) or ((handle_right-r)<5) or (price.iloc[r]>(price.iloc[handle_right]*1.12)):
                        continue
                    for p in range(r-1,-1,-1):
                        if ((r-p)<lookback_window and (price.iloc[p] > price.iloc[r])):
                            break

                        if ((r-p)>=lookback_window) and (price.iloc[p] > price.iloc[r]) and (price.iloc[p]<=(1.07*price.iloc[r])):
                            originR = r
                            tmpR = r
                            max_R_idx = tmpR
                            max_price_R = price.iloc[tmpR]
                            while tmpR<handle_right:
                                if price.iloc[tmpR]>max_price_R:
                                    max_price_R = max(price.iloc[tmpR],max_price_R)
                                    max_R_idx = tmpR
                                tmpR += 1
                            r = max_R_idx

                            bottom = price.iloc[p+1:r].min()
                            pivot = min(price.iloc[p],price.iloc[r])
                            #handle right must > MA50 and in the upper part of cup
                            pivot2 = (bottom + max(price.iloc[p],price.iloc[r]))/2
                            if (price.iloc[handle_right]<pivot2) or (price.iloc[handle_right]<price50.iloc[handle_right]):
                                break
                            #handle volume not too much
                            handle_avg = vol[r+1:handle_right+1].mean()
                            cup_avg = vol[p:r+1].mean()
                            if handle_avg>cup_avg:
                                break
                            #check gap < 40% and enough points near the bottom
                            max_ratio = (1-bottom/pivot)
                            inliner = 0
                            for x in range(p+1,r):
                                if ((1-bottom/price.iloc[x]) < (max_ratio/3)) and ((1-price.iloc[x]/pivot) > 0.05):
                                    inliner += 1
                            if (max_ratio>0.4) or ((inliner/(r-p-1))<0.05):
                                break
                            left_idx = p
                            if MODE>=2:
                                handle_arr.append(handle_right)
                            if (MODE == 1) or (MODE == 3):
                                fig,ax=plt.subplots()
                                ax.plot(price.iloc[left_idx:handle_right+1],label='Price')
                                ax.plot(price.index[originR], price.iloc[originR], 'yo', label='Orginal Cup Right')
                                ax.plot(price.index[r], price.iloc[r], 'ro', label='Cup Right')
                                ax.plot(price.index[handle_right], price.iloc[handle_right], 'bo', label='Handle Right')
                                ax.plot(price.index[left_idx], price.iloc[left_idx], 'go', label='Cup Left')
                                ax.legend()
                                y_min = price.iloc[left_idx:handle_right+1].min()
                                y_max = price.iloc[left_idx:handle_right+1].max()
                                ax.set_ylim(y_min * 0.95, y_max * 1.10)  # 下壓 5%、上留 10%
                                ax.yaxis.set_major_locator(mticker.MaxNLocator(nbins=30))  # 最多顯示 10 格
                                plt.title(STK+" cup "+str(cup_id))
                                plt.savefig('image/'+STK+'/cup'+str(cup_id)+'.png')
                                plt.close()
                            cup_id += 1
                            next_cup = True
                            i = p
                            break
                        if price.iloc[p]>(1.07*price.iloc[r]):
                            break
        i -= 1
    if MODE>=2:
        os.system("echo '"+str(handle_arr)+"' >> image/"+STK+"/report.txt")
