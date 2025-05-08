import yfinance as yf
import numpy as np
import pandas as pd
import sys
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import math
import time
import numpy as np
from selection import get_stock_list

stock_list = get_stock_list()
accounts = []
INITIAL_BAL = 10000
for i in range(len(stock_list)):
    accounts.append({'balance':INITIAL_BAL,'id':'','share':0,'cost':0}  
df = pd.read_csv('history/^GSPC.csv')
price = df.Close
index = 0
for stock in stock_list:
    print(stock)
    df = pd.read_csv('history/'+stock+'.csv', date_format="%m/%d/%Y")
    coffee_arr = is_coffee_and_handle(stock,df,mode,folder,bad_cup_id)
    print(coffee_arr)
    #drink coffee and spend money start
    #drink coffee and spend money done
    index += 1

total_money = 0
for account in accounts:
    total_money += account['balance']
    if account['share']>0:
        price = pd.read_csv('history/'+account['id']+'.csv').Close
        total_money += (account['share']*price./iloc[-1])

rev_rate = ((total_money-len(stock_list)*INITIAL_BAL)/(len(stock_list)*INITIAL_BAL)*100)
print("rev_rate = "+str(rev_rate)+" %")
