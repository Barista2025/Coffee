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

loss = [0,0,0,0]
fail = [0,0,0,0]
success = [0,0,0,0]
reward = [0,0,0,0]


for i in range(0,1259):
    catg = 0
    stock_list = get_stock_list(i,4)
    index = 0

    for account in accounts:
        balance = account['balance']
        ID = account['id']
        share = account['share']
        last_price = account['last_price']
        total_cost += balance
        df = pd.read_csv('history/'+ID+'.csv', date_format="%m/%d/%Y")
        price = df.Close
        r1 = 0.9 #stop loss
        r2 = 2.0 #take profit
        if ID == '':
            ID = stock_list[index]
            index += 1
        res = is_coffee_and_handle(ID,df):wq
        if (share>0) and ((price.iloc[i]<=(last_price*r1)) or (price.iloc[i]>=(last_price*r2))):
            if price.iloc[i]<last_price:
                rate = ((last_price-price.iloc[i])/last_price*100)
                print("debug rate = "+str(rate))
                loss[index] += rate
                fail[index] += 1
            else:
                success[index] += 1
                rate = ((price.iloc[i]-last_price)/last_price*100)
                reward[index] += rate
            balance += (price.iloc[i]*share)
            share = 0 
            last_price = 0 
        elif (res == 'Y') and (share==0):
            last_price = price.iloc[i]
            share = balance // price.iloc[i]
            balance -= (last_price*share)
            print('Let\'s drink!! '+str(i))

        account['balance'] = balance
        account['id'] = ID
        account['share'] = share
        account['last_price'] = last_price
 
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
