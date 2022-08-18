# Plot ad hoc CIFAR10 instances
from keras.datasets import cifar10
from matplotlib import pyplot
from scipy.misc import toimage
from random import randint
import numpy as np
# load data
(X_train, y_train), (X_test, y_test) = cifar10.load_data()
print(X_train.shape)
# create a grid of 3x3 images
for i in range(0, 9):
	pyplot.subplot(330 + 1 + i)
	pyplot.imshow(toimage(X_train[i]))
# show the plot
#pyplot.show()

data_set=[]
for i in range(0,20):
	
	x=randint(0,49999);
	dirran=randint(0,27)
	img_tem=X_train[x]
	print(img_tem.shape)
	img=img_tem[:,dirran:dirran+5]
	#print(img)
	data_set.append(img)
data_set=np.asarray(data_set)
#new_rshape = data_set.resize(20,3,5,5)
#print(new_rshape.shape)
print(data_set.shape)

