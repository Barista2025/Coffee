import yfinance as yf
import numpy as np
import pandas as pd
import sys
import os
import time
import numpy as np
import requests

def get_stock_list(li = -1):
    time = stock_data['SP500'].Date
    stock_list = []
    for stock in stocks:
        df = stock_data[stock]
        price = df.Close
        li_list = df[df.Date == time.iloc[li]].index
        if len(li_list) == 0:
            continue
        li = li_list[0]
        volume = stock_data[stock].Volume
        MA20 = ma20_cache[stock]
        if price.iloc[li-1]>MA20[li-1]:
            stock_list.append((stock,volume.iloc[li-1]))
    stock_list = sorted(stock_list, key=lambda x: x[1],reverse=True)
    res = [x[0] for x in stock_list[:4]]
    #print(stock_list[:4])
    return res

start = time.time()
 
output_lines = [[]] * 251
stock_data = {}
gross_cache = {}
ma20_cache = {}
fn = "select_ma20.txt"
os.system("rm -rf "+fn)
fp = open("history/stock_list.txt","r")

stock_data['SP500'] = pd.read_csv('history/SP500.csv')
stocks = fp.read().split('\n')[:-1]
for stock in stocks:
    df = pd.read_csv('history/'+stock+'.csv')
    stock_data[stock] = df
    price = df.Close
    ma20_cache[stock] = price.rolling(20).mean().shift(1).tolist()

for i in range(251):
     with open(fn, "a") as f:
         f.write('[]\n') 
for t in range(251,len(stock_data['SP500'])):
    candy = get_stock_list(t)
    with open(fn, "a") as f:
        f.write(str(candy)+'\n')
    #print(output_lines)
    #print(type(output_lines))
 
end = time.time()
print(f"執行時間: {end - start:.4f} 秒")

