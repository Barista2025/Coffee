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

                            #check gap < 40% and enough points near the bottom
                            bottom = price.iloc[p+1:r].min()
                            pivot = min(price.iloc[p],price.iloc[r])
                            max_ratio = (1-bottom/pivot)
                            inliner = 0
                            for x in range(p+1,r):
                                if ((1-bottom/price.iloc[x]) < (max_ratio/3)) and ((1-price.iloc[x]/pivot) > 0.05):
                                    inliner += 1
                            if (max_ratio>0.4) or ((inliner/(r-p-1))<0.05):
                                break
                            print('cup'+str(cup_id)+' max_ratio = '+str(max_ratio)+',in liner ratio = '+str(inliner/(r-p-1)))

                            left_idx = p
                            fig,ax=plt.subplots()
                            ax.plot(price.iloc[left_idx:handle_right+1],label='Price')
                            ax.plot(date[originR], price.iloc[originR], 'yo', label='Orginal Cup Right')
                            ax.plot(date[r], price.iloc[r], 'ro', label='Cup Right')
                            ax.plot(date[handle_right], price.iloc[handle_right], 'bo', label='Handle Right')
                            ax.plot(date[left_idx], price.iloc[left_idx], 'go', label='Cup Left')
                            ax.legend()
                            y_min = price.iloc[left_idx:handle_right+1].min()
                            y_max = price.iloc[left_idx:handle_right+1].max()
                            ax.set_ylim(y_min * 0.95, y_max * 1.10)  # 下壓 5%、上留 10%
                            ax.yaxis.set_major_locator(mticker.MaxNLocator(nbins=30))  # 最多顯示 10 格
                            plt.title(STK+" cup "+str(cup_id))
                            plt.savefig('image/'+STK+'_cup'+str(cup_id)+'.png')
                            cup_id += 1
                            #plt.show()
                            next_cup = True
                            i = p
                            break
                        if price.iloc[p]>(1.07*price.iloc[r]):
                            break
        i -= 1
    return False

dict = {'AMBA':('2020-04-03','2025-04-03'),'NVDA':('2015-12-30','2022-10-14'),'META':('2020-04-03','2025-04-03'),'TSM':('2020-04-03','2025-04-03'),'SBUX':('2020-04-03','2025-04-03'),'MCD':('2020-04-03','2025-04-03'),'RIVN':('2020-04-03','2025-04-03'),'INTC':('2020-04-03','2025-04-03')}
stocks = ['MCD']#'AMBA','NVDA','META']
os.system("rm -rf image/*")
for stock in stocks:
    is_coffee_and_handle(stock,dict[stock][0],dict[stock][1])
