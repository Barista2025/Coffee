import yfinance as yf
import numpy as np
import pandas as pd
import sys
import os
import matplotlib as mpl
mpl.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import math
import time
from keras.utils import to_categorical
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np
import cv2
import glob
from sklearn.model_selection import train_test_split

file_list = glob.glob(r'./image2/*/*.png')
file_list.sort()
X = []
y = []
for file in file_list:
    data = cv2.imread(file,0) / 255.0
    label = 1
    X.append(data)
    y.append(label)

file_list = glob.glob(r'./BAD/*.png')
file_list.sort()
for file in file_list:
    print(file)
    data = cv2.imread(file,0) / 255.0
    label = 0 
    X.append(data)
    y.append(label)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

print(str(len(X_train))+" "+str(len(X_test))+" "+str(len(y_train))+" "+str(len(y_test)))
