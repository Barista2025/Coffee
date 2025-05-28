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
import json
import numpy as np
from selection import get_stock_list
from utility_bt import is_coffee_and_handle

#stock_list = get_stock_list()
input_file = open ('accounts.json')
accounts = json.load(input_file)
total_cost = 0
total_earn = 0
hit_rate = 0
success = 0
fail = 0
reward = 0
loss = 0
for account in accounts:
    balance = account['balance']
    ID = account['id']
    share = account['share']
    last_price = account['last_price']
    total_cost += balance
    print(ID)
    df = pd.read_csv('history/'+ID+'.csv', date_format="%m/%d/%Y")
    price = df.Close
    drink = {}
    coffee_arr = is_coffee_and_handle(ID,df)
    for c in coffee_arr:
        drink[c] = 1
    r1 = 0.9
    r2 = 2.0
    #MA20 = price.rolling(20).mean()
    for i in range(0,1259):
        if (share>0) and ((price.iloc[i]<=(last_price*r1)) or (price.iloc[i]>=(last_price*r2))):
            if price.iloc[i]<last_price:
                rate = ((last_price-price.iloc[i])/last_price*100)
                print("debug rate = "+str(rate))
                loss += rate
                fail += 1
            else:
                success += 1
                rate = ((price.iloc[i]-last_price)/last_price*100)
                reward += rate
            balance += (price.iloc[i]*share)
            share = 0
            last_price = 0
        elif (i in drink) and (share==0):
            last_price = price.iloc[i]
            share = balance // price.iloc[i]
            balance -= (last_price*share)
            print('Let\'s drink!! '+str(i))
    if share>0:
        balance += (price.iloc[1258]*share)
        if price.iloc[i]<last_price:
            rate = ((last_price-price.iloc[i])/last_price*100)
            loss += rate
            fail += 1
        else:
            success += 1
            rate = ((price.iloc[i]-last_price)/last_price*100)
            reward += rate
    total_earn += balance

num = success+fail
rev_rate = ((total_earn-total_cost)/total_cost*100)
print("rev_rate = "+str(rev_rate)+" %, reward = "+str(reward/success)+" %, loss = "+str(loss/fail)+" %, hit rate = "+str(success/num*100)+" %")
