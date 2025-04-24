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
for file in file_list:
    print(file)

#data = cv2.imread('zero.jpg',0) / 255.0
#label = 0 # label/class of the image
#X.append(data)
#y.append(label)
#for stock in stocks:
#    os.system("mkdir -p image/"+stock)
#    is_coffee_and_handle(stock)
