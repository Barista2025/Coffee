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

def taste_coffee(STK,POS_ARR,DF=None,FOLDER='image'):
    price = DF.Close
    vol = DF.Volume
    price.index = pd.to_datetime(DF.Date,utc = True,format='ISO8601')
    l = len(price)
    tn = 0
    fn = 0
    r0 = 0.9
    r1 = 1.1
    if (len(POS_ARR)==1) and (POS_ARR[0]==''):
        return 0
    for p in POS_ARR:
        pos = int(p)
        p0 = price.iloc[pos]
        i = pos+1
        max_price = -1
        while i<l:
            if price.iloc[i]<=(p0*r0):
                break
            max_price = max(max_price,price.iloc[i]) 
            i += 1
        if max_price<(p0*r1):
            fn += 1
        else:
            tn += 1
    if (tn+fn)>0:
        return tn/(tn+fn)*100
    return 0

folder = sys.argv[1]
fp = open("history/stock_list.txt","r")
stocks = fp.read().split('\n')[:-1]
os.system("rm -rf review.txt")
candy = []
for stock in stocks:
    print(stock)
    df = pd.read_csv('history/'+stock+'.csv', date_format="%m/%d/%Y")
    fp2 = open(FOLDER+"/"+stock+"/report.txt","r")
    string = fp2.read()[1:-2]
    pos_arr = string.split(',')
    ret = taste_coffee(stock,pos_arr,df,folder)
    candy.append((ret,stock))
candy.sort(key=lambda x:x[0],reverse=False)
for C in candy:
    os.system("echo '"+C[1]+":"+str(C[0])+"%' >> review.txt")
