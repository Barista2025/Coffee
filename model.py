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
from keras.utils import to_categorical
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np
import cv2
import glob
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from keras.layers import Dropout

def show_train_history(train_history,train,validation):
    plt.plot(train_history.history[train])
    plt.plot(train_history.history[validation])
    plt.title('Train history')
    plt.ylabel('train')
    plt.xlabel('epoch')
    plt.legend(['train','validation'],loc='upper left')
    plt.show()

def plot_images_labels_prediction(images,labels,prediction,idx,num=10): 
    fig= plt.gcf()
    fig.set_size_inches(12,14)
    num = min(num,25)
    for i in range(0,num):
        ax=plt.subplot(5,5,i+1)
        ax.imshow(images[idx],cmap='binary')
        title="label=" +str(labels[idx])
        if len(prediction)>0:
            title+=",predict="+str(prediction[idx])
        ax.set_title(title,fontsize=10)
        ax.set_xticks([]);ax.set_yticks([])  
        idx+=1
    plt.show()

file_list = glob.glob(r'./image3/*/*.png')
file_list.sort()
X = []
y = []
for file in file_list:
    data = cv2.imread(file,0) / 255.0
    label = 1
    X.append(data)
    y.append(label)

print("good finish.")

file_list = glob.glob(r'./BAD/*.png')
file_list.sort()
for file in file_list:
    data = cv2.imread(file,0) / 255.0
    label = 0 
    X.append(data)
    y.append(label)
print("bad finish.")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
print(str(type(X_train))+" "+str(len(X_test))+" "+str(len(y_train))+" "+str(len(y_test)))
plot_images_labels_prediction(X_train,y_train,[],0,10)

x_train = np.array(X_train)
x_test = np.array(X_test)
x_Train=x_train.reshape(16419,19200).astype('float32')
x_Test=x_test.reshape(8088,19200).astype('float32')
x_Train_normalize=x_Train/255
x_Test_normalize=x_Test/255
# 標註資料--------------------------------------
y_TrainOneHot=to_categorical(y_train)
y_TestOneHot=to_categorical(y_test)

model = Sequential()
model.add(Dense(units=1000,input_dim=19200,kernel_initializer='normal',activation='relu'))
model.add(Dense(units=1000,kernel_initializer='normal',activation='relu'))
model.add(Dense(units=2,kernel_initializer='normal',activation='softmax'))
print(model.summary())
model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
train_history=model.fit(x=x_Train_normalize,y=y_TrainOneHot,
            validation_split=0.2,epochs=20,batch_size=200,verbose=2)
show_train_history(train_history,'accuracy','val_accuracy')
show_train_history(train_history,'loss','val_loss')
scores=model.evaluate(x_Test_normalize,y_TestOneHot)
print()
print('accuracy',scores[1])
prediction=model.predict(x_Test_normalize)
predict = np.argmax(prediction, axis=1)
print(str(predict.shape))
matrix = pd.crosstab(y_test,predict)
print(matrix)
model.save('./model/coffee.keras')
