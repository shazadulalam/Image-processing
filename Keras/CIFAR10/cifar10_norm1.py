'''Train a simple deep CNN on the CIFAR10 small images dataset.

GPU run command:
    THEANO_FLAGS=mode=FAST_RUN,device=gpu,floatX=float32 python cifar10_cnn.py

It gets down to 0.65 test logloss in 25 epochs, and down to 0.55 after 50 epochs.
(it's still underfitting at that point, though).

Note: the data was pickled with Python 2, and some encoding issues might prevent you
from loading it in Python 3. You might have to load it in Python 2,
save it in a different format, load it in Python 3 and repickle it.
'''

from __future__ import print_function
from keras.datasets import cifar10
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
import matplotlib.pyplot as plt
from matplotlib.cm import binary
from keras.utils import np_utils
from random import randint, seed
import numpy as np
import os

#shazad // start
# plotting/visualizing layers weight
def plot_layer(layer, x, y):
    layer_config = layer.get_config()
    print("Layer Name: ", layer_config['name'])
    layer_weight, layer_bias = layer.get_weights()
    print(layer_weight.shape)
    print("-------")
    layer_weight = layer_weight.reshape((32,27))
    figure = plt.figure()
    for i in range(len(layer_weight)):
    #     ax = figure.add_subplot(y, x, i+1)
    #     ax.matshow(layer_weight[i][0], cmap=binary)
    #     plt.xticks(np.array([]))
    #     plt.yticks(np.array([]))
    # figure.set_tight_layout(True)
    # plt.show()
        x = np.arange(0,27)
        y = layer_weight[i]
        plt.plot(x,y)
        plt.ylabel("Image points")
        plt.show()
        # figure.savefig('test.png')
#// end

batch_size = 32
nb_classes = 10
nb_epoch = 1
data_augmentation = True

# input image dimensions
img_rows, img_cols = 32, 32
# the CIFAR10 images are RGB
img_channels = 3

# the data, shuffled and split between train and test sets
(X_train, y_train), (X_test, y_test) = cifar10.load_data()
print('X_train shape:', X_train.shape)
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

#shazad // start
#finding random patch from X_train
data_set=[]
for i in range(0, 32):


    	x=randint(0,49999)
    	dirran=randint(0, 23)
    	img_tem=X_train[x]
    	img=img_tem[:,dirran:dirran+3,dirran:dirran+3]
    	print(img.shape)
    	data_set.append(img)

data_set=np.asarray(data_set)
new_rshape = data_set.reshape(32,3,3,3)
new_rshape = np.asarray(new_rshape)
# print(new_rshape.shape)

#passing zscore data into weight
weight = new_rshape
bias = np.zeros(32)
#// end

# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

model = Sequential()

model.add(Convolution2D(32, 3, 3, border_mode='same',
                        input_shape=(img_channels, img_rows, img_cols),
			weights=[weight,bias], init = 'normal'))
model.summary()
model.add(Activation('relu'))
model.add(Convolution2D(32, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Convolution2D(64, 3, 3, border_mode='same'))
model.add(Activation('relu'))
model.add(Convolution2D(64, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

# let's train the model using SGD + momentum (how original).
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255


if not data_augmentation:
    print('Not using data augmentation.')
    model.fit(X_train, Y_train,
              batch_size=batch_size,
              nb_epoch=nb_epoch,
              validation_data=(X_test, Y_test),
              shuffle=True)
else:
    print('Using real-time data augmentation.')

    # this will do preprocessing and realtime data augmentation
    datagen = ImageDataGenerator(
        featurewise_center=False,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        rotation_range=0,  # randomly rotate images in the range (degrees, 0 to 180)
        width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
        horizontal_flip=True,  # randomly flip images
        vertical_flip=False)  # randomly flip images

    # compute quantities required for featurewise normalization
    # (std, mean, and principal components if ZCA whitening is applied)
    datagen.fit(X_train)

    # fit the model on the batches generated by datagen.flow()
    model.fit_generator(datagen.flow(X_train, Y_train,
                        batch_size=batch_size),
                        samples_per_epoch=X_train.shape[0],
                        nb_epoch=nb_epoch,
                        validation_data=(X_test, Y_test))

# visualizing weights for first layer
plot_layer(model.layers[0], 8, 4)