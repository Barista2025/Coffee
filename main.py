import yfinance as yf
import numpy as np
import pandas as pd
import sys
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from tensorflow import keras
import math
import time
from keras.utils import to_categorical
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np
import cv2
import glob
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from keras.layers import Dropout

np.set_printoptions(suppress=True)
file = './image3/AVA/cup1.png'
file2 = './BAD/cup52.png'
x_test1 = cv2.imread(file,0) / 255.0
x_test1 = np.array(x_test1)
x_test1 = x_test1.reshape(1,19200).astype('float32')
x_test_normalize1=x_test1/255
x_test2 = cv2.imread(file2,0) / 255.0
x_test2 = np.array(x_test2)
x_test2 = x_test2.reshape(1,19200).astype('float32')
x_test_normalize2=x_test2/255

model = keras.models.load_model("./model/coffee.keras")
prediction=model.predict(x_test_normalize1)
print(prediction)
prediction=model.predict(x_test_normalize2)
print(prediction)

