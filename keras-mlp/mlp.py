import numpy as np
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout, LeakyReLU
from keras.utils import np_utils
from keras.callbacks import Callback
import json
from keras import regularizers

from wandb.keras import WandbCallback
import wandb

run = wandb.init()
config = run.config
config.epochs = 10
config.hidden_nodes = 64
config.optimizer = "adam"
# load data
(X_train, y_train), (X_test, y_test) = mnist.load_data()
img_width = X_train.shape[1]
img_height = X_train.shape[2]

X_train = X_train.astype('float32')
X_train /= 255.
X_test = X_test.astype('float32')
X_test /= 255.

# one hot encode outputs
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
labels = range(10)

num_classes = y_train.shape[1]


# create model
model=Sequential()
model.add(Flatten(input_shape=(img_width,img_height)))
model.add(Dropout(0.3))
model.add(Dense(config.hidden_nodes, kernel_regularizer =regularizers.l2(0.02) ))
model.add(LeakyReLU(alpha=0.2))
model.add(Dropout(0.3))
model.add(Dense(num_classes, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer=config.optimizer,
                    metrics=['accuracy'])

# Fit the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), 
      epochs=config.epochs,
      callbacks=[WandbCallback(data_type="image", labels=labels)])
