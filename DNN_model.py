import pickle
import pandas as pd
import numpy as np
import tensorflow, os
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv1D, MaxPool1D, Flatten
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import tensorflow.keras.backend as K
from sklearn.metrics import mean_absolute_error
from tensorflow.keras.callbacks import ModelCheckpoint
from time import time
from tensorflow.python.keras.callbacks import TensorBoard


pickle_dir = 'C:/NDVI_DATA/pickle_pixel/'

picklx = open(pickle_dir+'X_pixle.pickle', 'rb')
pickly = open(pickle_dir+'y_pixle.pickle', 'rb')


X = pickle.load(picklx)
y = pickle.load(pickly)

os.chdir('C:/Users/user/PycharmProjects/NDVI')


tensorboard = TensorBoard(log_dir="logs/{}".format(time()))


print(X.shape)
print(y.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=20)

print("X_train shape: ", X_train.shape)
print("y_train shape: ", y_train.shape)
print("X_test shape: ", X_test.shape)
print("y_test shape: ", y_test.shape)

opt = keras.optimizers.SGD(lr=0.01, nesterov=True)

def root_mean_squared_error(y_true, y_pred):
    return K.sqrt(K.mean(K.square(y_pred - y_true), axis=-1))

model = Sequential()
model.add(Dense(units=128, kernel_initializer='normal', input_dim=X_train.shape[1], activation='relu'))
model.add(Dense(units=256, kernel_initializer='normal', activation='relu'))
model.add(Dense(units=256, kernel_initializer='normal', activation='relu'))
model.add(Dense(units=256, kernel_initializer='normal', activation='relu'))
model.add(Dense(units=1, kernel_initializer='normal', activation='linear'))


model.compile(loss='mean_absolute_error', optimizer='adam', metrics=[root_mean_squared_error])

model.summary()


checkpoint_name = 'Weights-{epoch:03d}--{val_loss:.5f}.hdf5'
checkpoint = ModelCheckpoint(checkpoint_name, monitor='val_loss', verbose = 1, save_best_only = True, mode ='auto')
callbacks_list = [checkpoint]

model.fit(X_train, y_train, epochs=2000, batch_size=30, validation_split=0.2, callbacks=[tensorboard])

model.evaluate(X_test, y_test)