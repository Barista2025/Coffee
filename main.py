import yfinance as yf
import numpy as np
import pandas as pd
import sys
import os
import matplotlib as mpl
mpl.use('Qt5Agg')
import matplotlib.pyplot as plt
import utility as util
import talib
import math

from sklearn.metrics import confusion_matrix, classification_report

# 假设 y_true 是真实标签，y_pred 是模型预测标签
y_true = [1, 0, 1, 1, 0, 1, 0, 0, 1, 0]  # 实际值
y_pred = [1, 0, 1, 0, 0, 1, 1, 0, 1, 0]  # 预测值

# 计算混淆矩阵
cm = confusion_matrix(y_true, y_pred)
print("Confusion Matrix:\n", cm)

price = yf.Ticker("AMBA").history(start="2017-06-01",end='2019-04-24', interval='1d').Close
date = yf.Ticker("AMBA").history(start="2017-06-01",end='2019-04-24', interval='1d').index

l = len(price)

for i in range(l-2,0,-1):
    if price.iloc[i] >= price.iloc[-1]:
        break

print(str(price.iloc[i])+" "+str(date[i]))
