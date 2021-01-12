# -*- coding: utf-8 -*-
"""moadel1Heartbeat Classification Subject-Oriented.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/161qLewmgia-A9H84NivvQfcX2RlprJ_6

Imports
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x

from sklearn.utils import shuffle
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
######## Keras #########
from keras.models import Sequential
from keras.layers import Input , MaxPool1D , GlobalMaxPool1D , AvgPool1D , GlobalAvgPool1D , BatchNormalization
from keras.layers.core import Flatten, Dense, Dropout 
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D ,Convolution1D ,MaxPooling1D,ZeroPadding1D 
from keras.optimizers import SGD 
from keras import optimizers , activations
from keras import losses
from keras import metrics
from keras import models
import numpy as np
from numpy import  newaxis

from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

import keras
from keras.layers.core import Layer

from keras.models import Model , Sequential

from keras.layers import Conv1D , MaxPool1D , Dropout , Flatten , Dense ,\
 Input ,concatenate , GlobalAveragePooling1D , AveragePooling1D  , MaxPooling1D , BatchNormalization , Activation , GlobalAveragePooling2D

from keras.layers.convolutional import Convolution1D
from keras import optimizers , activations

from keras.optimizers import *
from keras.utils import plot_model

import torch
import pandas as pd

from google.colab import drive
drive.mount('/content/drive')

!unzip "/content/drive/My Drive/Preprocessed Dataset/Subject-Oriented.zip"

# Make Y Train or Test based on class number ,  #classes , #samples in this class
    def One_Hot_Encoded_Y(classNumber,NumberOfClasses,NumberOfSamples):
      if NumberOfSamples == 0:
        Y = np.empty((0,NumberOfClasses))
        return Y
      Yi = np.zeros(NumberOfClasses)
      Yi[classNumber] = 1
      Y = np.vstack([Yi]*NumberOfSamples)
      return Y
    # Read Class from Text file and return X , Y
    def ReadClassData(path,ZeroBased_classNumber,NumOfClasses):
      Data = open(path, "r").readlines()
      X = []
      for i in Data:
          row = i.split('|')
          row.remove('\n')
          row = list(map(float, row))
          X.append(row)
      X = np.array(X)
      if X.shape[0] == 0:
        X = np.empty((0,300))
      Y = One_Hot_Encoded_Y(ZeroBased_classNumber,NumOfClasses,X.shape[0])
      return X,Y

    # concatenate classes training data & testing data and make Y for this category
    def Prepare_Category(ClassesTrainData,ClassesTestData, classNumber,NumberOfCategories,MultiClassCategory=True):
      if MultiClassCategory:
      
        Ncat_X_train= np.concatenate(ClassesTrainData, axis=0)
        Ncat_X_test = np.concatenate(ClassesTestData, axis=0)
      else:
        print('category of one class')
        Ncat_X_train = ClassesTrainData
        Ncat_X_test = ClassesTestData
      
      Ncat_Y_train = One_Hot_Encoded_Y(classNumber,NumberOfCategories,Ncat_X_train.shape[0])
    
      
      Ncat_Y_test = One_Hot_Encoded_Y(classNumber,NumberOfCategories,Ncat_X_test.shape[0])

      #Ncat_X_train,Ncat_Y_train = shuffle(Ncat_X_train,Ncat_Y_train)
      #Ncat_X_test , Ncat_Y_test = shuffle(Ncat_X_test , Ncat_Y_test)
      return Ncat_X_train , Ncat_X_test , Ncat_Y_train , Ncat_Y_test

    def Model_Y(NumberOfSamplesEachClass = []):
      NumberOfClasses = len(NumberOfSamplesEachClass)
      Ys = []
      for i in range(NumberOfClasses):
          Ys.append(One_Hot_Encoded_Y(i,NumberOfClasses,NumberOfSamplesEachClass[i]))
      Ys = tuple(Ys)
      Y = np.concatenate(Ys,axis=0)
      return Y

"""Read Data From Text Files"""

files = {'N': 'Normal', 'L': 'Left_bundle_branch_block', 'R': 'Right_bundle_branch_block', 'A': 'Atrial_premature',
             'a': 'Aberrated_atrial_premature', 'J': 'Nodal(junctional)premature',
             'V': 'Premature_ventricular_contraction', 'F': 'Fusion_of_ventricular_and_normal',
             '!': 'Ventricular_flutter_wave', 'e': 'Atrial_escape', 'j': 'Nodal(junctional)escape',
             'E': 'Ventricular_escape',
             '/': 'Paced', 'f': 'Fusion_of_paced_and_normal', 'x': 'Non-conducted_P-wave', 'Q': 'Unclassifiable'}
    directory_train = '/content/Subject-Oriented/Train/'
    directory_test = '/content/Subject-Oriented/Test/'
    shuff = True
    NumOfClasses = 16
    
    path = directory_train + files['N'] + '.txt'
    XN_train , YN_train = ReadClassData(path,0,NumOfClasses)
    path = directory_test + files['N'] + '.txt'
    XN_test , YN_test = ReadClassData(path,0,NumOfClasses)

    


    path = directory_train + files['L'] + '.txt'
    XL_train , YL_train = ReadClassData(path,1,NumOfClasses)
    path = directory_test + files['L'] + '.txt'
    XL_test , YL_test = ReadClassData(path,1,NumOfClasses)
   

    path = directory_train + files['R'] + '.txt'
    XR_train , YR_train = ReadClassData(path,2,NumOfClasses)
    path = directory_test + files['R'] + '.txt'
    XR_test , YR_test = ReadClassData(path,2,NumOfClasses)

    path = directory_train + files['A'] + '.txt'
    XA_train , YA_train = ReadClassData(path,3,NumOfClasses)
    path = directory_test + files['A'] + '.txt'
    XA_test , YA_test = ReadClassData(path,3,NumOfClasses)


    path = directory_train + files['a'] + '.txt'
    Xa_train , Ya_train = ReadClassData(path,4,NumOfClasses)
    path = directory_test + files['a'] + '.txt'
    Xa_test , Ya_test = ReadClassData(path,4,NumOfClasses)

    path = directory_train + files['J'] + '.txt'
    XJ_train, YJ_train = ReadClassData(path,5,NumOfClasses)
    path = directory_test + files['J'] + '.txt'
    XJ_test, YJ_test = ReadClassData(path,5,NumOfClasses)



    path = directory_train + files['V'] + '.txt'
    XV_train , YV_train = ReadClassData(path,6,NumOfClasses)
    path = directory_test + files['V'] + '.txt'
    XV_test , YV_test = ReadClassData(path,6,NumOfClasses)

    path = directory_train + files['F'] + '.txt'
    XF_train , YF_train = ReadClassData(path,7,NumOfClasses)
    path = directory_test + files['F'] + '.txt'
    XF_test , YF_test = ReadClassData(path,7,NumOfClasses)


    path = directory_train + files['!'] + '.txt'
    Xvfw_train , Yvfw_train = ReadClassData(path,8,NumOfClasses)
    path = directory_test + files['!'] + '.txt'
    Xvfw_test , Yvfw_test = ReadClassData(path,8,NumOfClasses)


    path = directory_train + files['e'] + '.txt'
    Xe_train , Ye_train= ReadClassData(path,9,NumOfClasses)
    path = directory_test + files['e'] + '.txt'
    Xe_test , Ye_test= ReadClassData(path,9,NumOfClasses)


    path = directory_train + files['j'] + '.txt'
    Xj_train , Yj_train = ReadClassData(path,10,NumOfClasses)
    path = directory_test + files['j'] + '.txt'
    Xj_test , Yj_test = ReadClassData(path,10,NumOfClasses)

    path = directory_train + files['E'] + '.txt'
    XE_train , YE_train = ReadClassData(path,11,NumOfClasses)
    path = directory_test + files['E'] + '.txt'
    XE_test , YE_test = ReadClassData(path,11,NumOfClasses)

    path = directory_train + files['/'] + '.txt'
    XP_train , YP_train = ReadClassData(path,12,NumOfClasses)
    path = directory_test + files['/'] + '.txt'
    XP_test , YP_test = ReadClassData(path,12,NumOfClasses)

    path = directory_train + files['f'] + '.txt'
    Xf_train , Yf_train = ReadClassData(path,13,NumOfClasses)
    path = directory_test + files['f'] + '.txt'
    Xf_test , Yf_test = ReadClassData(path,13,NumOfClasses)

    path = directory_train + files['x'] + '.txt'
    Xx_train , Yx_train = ReadClassData(path,14,NumOfClasses)
    path = directory_test + files['x'] + '.txt'
    Xx_test , Yx_test = ReadClassData(path,14,NumOfClasses)

    path = directory_train + files['Q'] + '.txt'
    XQ_train , YQ_train = ReadClassData(path,15,NumOfClasses)
    path = directory_test + files['Q'] + '.txt'
    XQ_test , YQ_test = ReadClassData(path,15,NumOfClasses)

"""Prepare Models Training & Testing Data"""

#-------------------------One Stage Data------------------------
    X_TRAIN= np.concatenate((XA_train,Xa_train,XE_train,Xe_train,XF_train,Xf_train,XJ_train,Xj_train,XL_train,XN_train,XQ_train,XR_train,XV_train,Xx_train,XP_train,Xvfw_train), axis=0)
    Y_TRAIN= np.concatenate((YA_train,Ya_train,YE_train,Ye_train,YF_train,Yf_train,YJ_train,Yj_train,YL_train,YN_train,YQ_train,YR_train,YV_train,Yx_train,YP_train,Yvfw_train), axis=0)
    
    
    X_TEST= np.concatenate((XA_test,Xa_test,XE_test,Xe_test,XF_test,Xf_test,XJ_test,Xj_test,XL_test,XN_test,XQ_test,XR_test,XV_test,Xx_test,XP_test,Xvfw_test), axis=0)
    Y_TEST= np.concatenate((YA_test,Ya_test,YE_test,Ye_test,YF_test,Yf_test,YJ_test,Yj_test,YL_test,YN_test,YQ_test,YR_test,YV_test,Yx_test,YP_test,Yvfw_test), axis=0)

    X_train , Y_train = shuffle(X_TRAIN , Y_TRAIN)
    X_test,Y_test = shuffle( X_TEST,Y_TEST)
    X_train = np.expand_dims(X_train,axis=2)
    X_test = np.expand_dims(X_test,axis=2)

    #-------------------Two Stages Data-------------------------------
    
    # Categories Data
    Ncat_X_train , Ncat_X_test , Ncat_Y_train , Ncat_Y_test = Prepare_Category((XN_train,XL_train,XR_train,Xe_train,Xj_train), (XN_test,XL_test,XR_test,Xe_test,Xj_test) , 0 , 5)
    Scat_X_train , Scat_X_test  , Scat_Y_train  , Scat_Y_test = Prepare_Category((XA_train,Xa_train,XJ_train,Xx_train) , (XA_test,Xa_test,XJ_test,Xx_test) , 1 ,5)
    Vcat_X_train, Vcat_X_test, Vcat_Y_train ,Vcat_Y_test = Prepare_Category((XV_train,Xvfw_train,XE_train),(XV_test,Xvfw_test,XE_test),2,5)
    Fcat_X_train , Fcat_X_test, Fcat_Y_train ,  Fcat_Y_test = Prepare_Category((XF_train),(XF_test) , 3 , 5,False)
    Qcat_X_train ,  Qcat_X_test, Qcat_Y_train ,Qcat_Y_test = Prepare_Category((XP_train,Xf_train,XQ_train) , (XP_test,Xf_test,XQ_test) , 4 , 5)
   
    # First Stage Data
    first_stage_model_X_train = np.concatenate((Ncat_X_train , Scat_X_train , Vcat_X_train , Fcat_X_train , Qcat_X_train),axis=0)
    first_stage_model_X_test = np.concatenate((Ncat_X_test , Scat_X_test , Vcat_X_test , Fcat_X_test , Qcat_X_test),axis=0)

    first_stage_model_Y_train = np.concatenate((Ncat_Y_train , Scat_Y_train , Vcat_Y_train , Fcat_Y_train , Qcat_Y_train),axis=0)
    first_stage_model_Y_test = np.concatenate((Ncat_Y_test , Scat_Y_test , Vcat_Y_test , Fcat_Y_test , Qcat_Y_test),axis=0)
    
    first_stage_model_X_train , first_stage_model_Y_train = shuffle(first_stage_model_X_train , first_stage_model_Y_train)
    first_stage_model_X_test , first_stage_model_Y_test = shuffle(first_stage_model_X_test , first_stage_model_Y_test)

    first_stage_model_X_train = np.expand_dims(first_stage_model_X_train,axis=2)
    first_stage_model_X_test = np.expand_dims(first_stage_model_X_test,axis=2)
    #------------------------------------------------------------------------------------------------------------------------
    
    #Each Model Data in the second stage
    model1_Y_train = Model_Y([XN_train.shape[0] ,XL_train.shape[0] ,XR_train.shape[0] ,Xe_train.shape[0] ,Xj_train.shape[0]])
    model1_Y_test = Model_Y([XN_test.shape[0] ,XL_test.shape[0] ,XR_test.shape[0] ,Xe_test.shape[0] ,Xj_test.shape[0]])

    Ncat_X_train , model1_Y_train = shuffle(Ncat_X_train , model1_Y_train)     
    Ncat_X_test , model1_Y_test = shuffle(Ncat_X_test , model1_Y_test)         

    Ncat_X_train = np.expand_dims(Ncat_X_train,axis=2)
    Ncat_X_test = np.expand_dims(Ncat_X_test,axis=2)
    
    model2_Y_train = Model_Y([XA_train.shape[0] ,Xa_train.shape[0] ,XJ_train.shape[0] ,Xx_train.shape[0]])
    model2_Y_test = Model_Y([XA_test.shape[0] ,Xa_test.shape[0] ,XJ_test.shape[0] ,Xx_test.shape[0]])

    Scat_X_train , model2_Y_train = shuffle(Scat_X_train , model2_Y_train)
    Scat_X_test , model2_Y_test = shuffle(Scat_X_test , model2_Y_test)

    Scat_X_train = np.expand_dims(Scat_X_train,axis=2)
    Scat_X_test = np.expand_dims(Scat_X_test,axis=2)
    
    model3_Y_train = Model_Y([ XV_train.shape[0], Xvfw_train.shape[0], XE_train.shape[0]])
    model3_Y_test = Model_Y([XV_test.shape[0], Xvfw_test.shape[0] ,XE_test.shape[0]])
    
    Vcat_X_train , model3_Y_train = shuffle(Vcat_X_train , model3_Y_train)
    Vcat_X_test , model3_Y_test = shuffle(Vcat_X_test , model3_Y_test)

    Vcat_X_train = np.expand_dims(Vcat_X_train,axis=2)
    Vcat_X_test = np.expand_dims(Vcat_X_test,axis=2)

    model5_Y_train = Model_Y([XP_train.shape[0],Xf_train.shape[0],XQ_train.shape[0]])
    model5_Y_test = Model_Y([XP_test.shape[0] ,Xf_test.shape[0] ,XQ_test.shape[0]])

    Qcat_X_train , model5_Y_train = shuffle(Qcat_X_train , model5_Y_train)
    Qcat_X_test , model5_Y_test = shuffle(Qcat_X_test , model5_Y_test)

    Qcat_X_train = np.expand_dims(Qcat_X_train,axis=2)
    Qcat_X_test = np.expand_dims(Qcat_X_test,axis=2)

    # key is the class number in the category model and the value is the class number between all classes
    model1_lookup = {0:0,1:1,2:2,3:9,4:10}
    model2_lookup = {0:3,1:4,2:5,3:14}
    model3_lookup = {0:6,1:8,2:11}
    model5_lookup = {0:12,1:13,2:15}

"""To Validate Number of Samples Only"""

print(first_stage_model_X_train.shape , first_stage_model_Y_train.shape ,first_stage_model_X_test.shape , first_stage_model_Y_test.shape)

print(Ncat_X_train.shape , model1_Y_train.shape,Ncat_X_test.shape , model1_Y_test.shape)
print(Scat_X_train.shape , model2_Y_train.shape,Scat_X_test.shape , model2_Y_test.shape)
print(Vcat_X_train.shape , model3_Y_train.shape,Vcat_X_test.shape , model3_Y_test.shape)
print(Fcat_X_train.shape , Fcat_X_test.shape)
print(Qcat_X_train.shape , model5_Y_train.shape,Qcat_X_test.shape , model5_Y_test.shape)

"""Model Construction"""

def Build_Confusion_Matrix(y_test,y_pred,num_of_classes):
  confusion_matrix = np.zeros((num_of_classes,num_of_classes))
  for i in range(len(y_test)):
    confusion_matrix[y_test[i],y_pred[i]]+=1
  return confusion_matrix

def Calculate_Accuracy(confusion_matrix):
  acc = (np.sum(confusion_matrix.diagonal())/np.sum(confusion_matrix))*100
  accuracies = []
  for i in range(len(confusion_matrix)):
    class_count = confusion_matrix[i,i]
    if class_count == 0:
      accuracies.append(0)
    else:
      ac = (confusion_matrix[i,i]/np.sum(confusion_matrix[i,:]))*100
      accuracies.append(ac)
  print(accuracies)
  average_accuracy = np.average(accuracies)
  print('Average Accuracy', average_accuracy )
  print('Overall Accuracy',acc)
  
  return acc , average_accuracy

def Evaluate(y_test,y_pred,num_of_classes):
  confusion_matrix = Build_Confusion_Matrix(y_test,y_pred,num_of_classes)
  confusion_matrix = np.int64(confusion_matrix)
  print(confusion_matrix)
  return Calculate_Accuracy(confusion_matrix)

def Predict_and_Evaluate(model,X_test,Y_test,NumOfClasses):
  Y_predict = model.predict(X_test)
  inds = np.argmax(Y_test,axis=1)
  pred = np.argmax(Y_predict,axis=1)
  accuracy = sum([np.argmax(Y_predict[i])==np.argmax(Y_test[i]) for i in range(len(Y_test))])/len(Y_test)
  print(accuracy)
  return Evaluate( inds , pred , NumOfClasses)

def Two_Stages_Predict(X_Test , models = {} , lockups = {}):
  first_stage_model = models['first_stage']
  y_pred = []
  for xtest in X_Test:
    first_model_prediction = first_stage_model.predict(xtest)
    first_model_prediction = np.argmax(first_model_prediction,axis = 1)
    if (first_model_prediction != 3):
      second_stage_prediction = models[first_model_prediction].predict(xtest)
      second_stage_prediction = np.argmax(second_stage_prediction, axis = 1)
      current_model_lockup = lockups[first_model_prediction]
      y_pred.append(current_model_lockup[second_stage_prediction])
  return y_pred

def CNN(nclass = 16):
    inp = Input(shape=(300, 1))
    lay = Convolution1D(32, kernel_size=5, activation=activations.relu, padding="valid")(inp)
    lay = Convolution1D(32, kernel_size=5, activation=activations.relu, padding="valid")(lay)
    lay = AvgPool1D(pool_size=2)(lay)
    
    

    lay = Convolution1D(64, kernel_size=3, activation=activations.relu, padding="valid")(lay)
    lay = Convolution1D(64, kernel_size=3, activation=activations.relu, padding="valid")(lay)
    lay = Convolution1D(64, kernel_size=3, activation=activations.relu, padding="valid")(lay)
    lay = AvgPool1D(pool_size=2)(lay)
    lay = Dropout(rate=0.1)(lay)
    lay = BatchNormalization() (lay)

    lay = Convolution1D(64, kernel_size=3, activation=activations.relu, padding="valid")(lay)
    lay = Convolution1D(64, kernel_size=3, activation=activations.relu, padding="valid")(lay)
    lay = Convolution1D(64, kernel_size=3, activation=activations.relu, padding="valid")(lay)
    lay = AvgPool1D(pool_size=2)(lay)
    lay = Dropout(rate=0.1)(lay)
    lay = BatchNormalization() (lay)

    lay = Convolution1D(128, kernel_size=3, activation=activations.relu, padding="valid")(lay)
    lay = Convolution1D(128, kernel_size=3, activation=activations.relu, padding="valid")(lay)
    lay = Convolution1D(128, kernel_size=3, activation=activations.relu, padding="valid")(lay)
    lay = AvgPool1D(pool_size=2)(lay)
    lay = Dropout(rate=0.1)(lay)
    lay = BatchNormalization() (lay)

    lay = Convolution1D(256, kernel_size=3, activation=activations.relu, padding="valid")(lay)
    lay = Convolution1D(256, kernel_size=3, activation=activations.relu, padding="valid")(lay)
    lay = Convolution1D(256, kernel_size=3, activation=activations.relu, padding="valid")(lay)
    lay = GlobalMaxPool1D()(lay)
    lay = Dropout(rate=0.1)(lay)
    lay = BatchNormalization() (lay)
    
    dense_1 = Dense(64, activation=activations.relu)(lay)
    dense_1 = Dense(64, activation=activations.relu)(dense_1)
    dense_1 = Dense(nclass, activation=activations.softmax)(dense_1)


    model = models.Model(inputs=inp, outputs=dense_1)
    #model.compile(optimizer=optimizers.Adam(lr=0.00001), loss= losses.categorical_crossentropy,metrics=['acc'])
    model.compile(loss='categorical_crossentropy', optimizer=optimizers.Adam(lr=0.0001), metrics=['accuracy'])
    model.summary()
    return model

"""**Inception Module**"""

def inception_module2(layer_in, f1, f2_in, f2_out, f3_in, f3_out, f4_out):
	# 1x1 conv
	conv1 = Conv1D(f1, 1, padding='same', activation='relu')(layer_in)
	# 3x3 conv
	conv3 = Conv1D(f2_in, 1, padding='same', activation='relu')(layer_in)
	conv3 = Conv1D(f2_out, 3, padding='same', activation='relu')(conv3)
	# 5x5 conv
	conv5 = Conv1D(f3_in, 1, padding='same', activation='relu')(layer_in)
	conv5 = Conv1D(f3_out, 5, padding='same', activation='relu')(conv5)
	# 3x3 max pooling
	pool = MaxPooling1D(1, strides=None, padding='same')(layer_in)
	pool = Conv1D(f4_out, 1, padding='same', activation='relu')(pool)
	# concatenate filters, assumes filters/channels last
	layer_out = concatenate([conv1, conv3, conv5, pool], axis=-1)
	return layer_out

def inception(nclass = 16):
    inp = Input (shape=(300,1))
    conv1 = Conv1D(32, 3, padding='same', activation='relu')(inp)
    conv2 = Conv1D(64, 3, padding='same', activation='relu')(conv1)
    Module= inception_module2(conv2 , 64, 96, 128, 16, 32, 32)
    Module2 = inception_module2(Module, 64, 96,128,   16, 32, 32) 
    batch = BatchNormalization() (Module2)
    Module3 = inception_module2(batch,  128, 128 , 192,32,96,64) 
    Module4 = inception_module2(Module3,  128, 128 ,192,32,96,64) 
    batch2 = BatchNormalization() (Module4)
    Module5 = inception_module2(batch2,  196 ,128,  256  ,64, 128,   96)
    Module6 = inception_module2(Module5, 196 ,128,  256  ,64, 128,   96)
    GAP = GlobalAveragePooling1D() (Module6) 
    layer = Dense(128 , activation='relu' ) (GAP)
    Dense_layer_ouput = Dense(16, activation='softmax') (layer)
    Dense_layer_ouput = Dense(nclass, activation='softmax') (layer)
    model = Model (inputs = inp , outputs = Dense_layer_ouput) 

    model.compile(loss='categorical_crossentropy', optimizer=optimizers.Adam(lr=0.0001), metrics=['accuracy'])

    model .summary()
    return model

model = inception(5)

model.load_weights('/content/drive/My Drive/Preprocessed Dataset/Subject-Oriented Weights/incep/Subject-Oriented_inceptrain_45.990657994754905##91.58484428648876#Epoch : 5')

model.load_weights('/content/drive/My Drive/Preprocessed Dataset/Subject-Oriented Weights/incep/Subject-Oriented_inceptrain_48.645984637732724##86.0430094572616#Epoch : 73')
Predict_and_Evaluate(model,first_stage_model_X_test,first_stage_model_Y_test,5)

model.load_weights('/content/drive/My Drive/Preprocessed Dataset/Subject-Oriented Weights/incep/Subject-Oriented_inceptrain_50.1181895868928##81.16780113647772#Epoch : 56')
Predict_and_Evaluate(model,first_stage_model_X_test,first_stage_model_Y_test,5)

model.compile(loss='categorical_crossentropy', optimizer=optimizers.Adam(lr=0.00001), metrics=['accuracy'])
#model.fit(x =first_stage_model_X_train , y =first_stage_model_Y_train  ,  batch_size=32 , epochs= 50)
epochs = []
accuracies =[]
trainedEpochs = 90
maxi , max_avg = Predict_and_Evaluate(model,first_stage_model_X_test,first_stage_model_Y_test,5) 
!mkdir "/content/drive/My Drive/Preprocessed Dataset/Subject-Oriented Weights/incep/"
weights_dir = '/content/drive/My Drive/Preprocessed Dataset/Subject-Oriented Weights/incep/'
s = "Subject-Oriented_incep_" + str (max_avg) + "##" + str (maxi) + "#Epoch : " + str (trainedEpochs) 
#model.save_weights(s)
#model.save_weights("/content/drive/My Drive/Preprocessed Dataset/Trial6/First_Stage_CNN/"+s)
for i in range (20) :
  print('Epoch',i+1)
  model.fit(x =first_stage_model_X_train, y =first_stage_model_Y_train  ,  batch_size=32 , epochs= 1)
  acc , avg = Predict_and_Evaluate(model,first_stage_model_X_test,first_stage_model_Y_test,5) 
  if ( avg > max_avg or acc > maxi) :
    s = "Subject-Oriented_inceptrain_" + str (avg) + "##" + str (acc) + "#Epoch : " + str (i+ trainedEpochs +1) 
    model.save_weights(s)
    model.save_weights(weights_dir+s)
    if avg > max_avg:
        max_avg = avg 
    if acc > maxi:
        maxi = acc
        epochs.append(i) 
        accuracies.append (acc) 
print ('Maximum Average',max_avg)