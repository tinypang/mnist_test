import image_sae
import numpy as np, random
from struct import *

def importMNIST(startN,howMany,bTrain=True,only01=False):	#import MNIST
	if bTrain:
		fImages = open('train-images.idx3-ubyte','rb')
		fLabels = open('train-labels.idx1-ubyte','rb')
	else:
		fImages = open('t10k-images.idx3-ubyte','rb')
		fLabels = open('t10k-labels.idx1-ubyte','rb')

	# read the header information in the images file.
	s1, s2, s3, s4 = fImages.read(4), fImages.read(4), fImages.read(4), fImages.read(4)
	mnIm = unpack('>I',s1)[0]
	numIm = unpack('>I',s2)[0]
	rowsIm = unpack('>I',s3)[0]
	colsIm = unpack('>I',s4)[0]
	# seek to the image we want to start on
	fImages.seek(16+startN*rowsIm*colsIm)

	# read the header information in the labels file and seek to position
	# in the file for the image we want to start on.
	mnL = unpack('>I',fLabels.read(4))[0]
	numL = unpack('>I',fLabels.read(4))[0]
	fLabels.seek(8+startN)

	T = [] # list of (input, correct label) pairs

	for blah in range(0, howMany):
	# get the input from the image file
		x = []
		for i in range(0, rowsIm*colsIm):
			val = unpack('>B',fImages.read(1))[0]
			x.append(val/255.0)

	# get the correct label from the labels file.
		val = unpack('>B',fLabels.read(1))[0]
		y = []
		for i in range(0,10):
			if val==i: y.append(1)
			else: y.append(0)

	# if only01 is True, then only add this example if 0 or 1 is the
	# correct label.
		if not only01 or y[0]==1 or y[1]==1:
			T.append([x,y])
	    
	fImages.close()
	fLabels.close()

	return T

dataset= importMNIST(0,50)	#get first 50 images
alpha = 100			#set various parametes
m = 2
theta = 0.001
costfunc = []
weights = []
ninput = len(dataset[0][0])
nhidden = ninput/2
for i in range(0, len(dataset)):	#initialise weights and bias
	w0, w1, b0, b1 = [], [], [], []		#w0 and w1 are arrays of arrays ie. array of weights
	for i in range(0,ninput):
		temp = []
		for j in range(0,nhidden):
			temp.append(random.uniform(-0.1,0.1))
			b0.append(random.uniform(-0.1,0.1))
		w0.append(temp)
	for i in range(0,nhidden):
		temp = []
		for j in range(0,ninput):
			temp.append(random.uniform(-0.1,0.1))
			b1.append(random.uniform(-0.1,0.1))
		w1.append(temp)
	weights.append([w0,w1])
bias = [b0,b1]
for i in range(0,len(dataset)):		#run first iteration of network
	print i
	costfunc.append(image_sae.main(dataset[i][0],weights[i], bias,alpha,m,theta))
print costfunc
	

