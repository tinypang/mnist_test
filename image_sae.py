import numpy as np
from scipy import misc
import random
import math

def activation(node): #activation fn
	return 1/(1+math.exp(-node.input)) 

def d_activation(node):	#derivative of activation fn
	t =  math.exp(-node.input)
	return t/((1+t)**2)

def main(in_img, weights, bias, alpha, m , theta):	#main function that creates all arrays and calls functions
	#in_img = input()
	#alpha = 100
	#m = 2
	#theta = 0.001
	w0, w1 = weights		#set weights and bias to those parsed in
	B0, B1 = bias
	input_layer = []
	for i in range(len(in_img)):		#initialises input layer for each pixel in the input image
			new_node = node(in_img[i],0,w0[i])			
			input_layer.append(new_node)
	ninput = len(input_layer)	
	nhidden = ninput/2		#sets number of hidden nodes
	#for i in input_layer:
	#	i.init_weights(init_weights)	
	hidden_layer = []	
	for i in range(0, nhidden):			#initialises hidden layer
			hidden_layer.append(node(0,1,w1[i]))
		#hidden_layer[i].init_weights(ninput)
			#B0.append((random.uniform(-0.1,0.1)))
	output_layer = []
	for i in range(0, ninput):			#initialises output layer
		output_layer.append(node(0,2))
		#B1.append((random.uniform(-0.1,0.1)))
	deltaW1 = np.zeros((ninput,nhidden))			#initialises deltaW matrices and deltaB vectors
	deltaW0 = np.zeros((nhidden,ninput))
	deltaB0 = np.zeros(nhidden)
	deltaB1 = np.zeros(ninput)
	hidden_layer = feed_forward(input_layer, hidden_layer, B0)	#perform feed forward pass
	output_layer = feed_forward(hidden_layer, output_layer, B1)
	error2 = output_error(output_layer, input_layer)		#perform error back propagation
	error1 = hidden_error(hidden_layer, error2)
	deltapartialW1, deltapartialB1 = compute_partials(error2, hidden_layer)		#calculate partial derivatives for W and B
	deltapartialW0, deltapartialB0 = compute_partials(error1, input_layer)
	deltaW0 = np.add(deltaW0, deltapartialW0)		#calculate new values of deltaW and deltaB
	deltaW1 = np.add(deltaW1, deltapartialW1)
	deltaB0 = np.add(deltaB0, deltapartialB0)
	deltaB1 = np.add(deltaB1, deltapartialB1)
	B0 = B0-alpha*((1.0/m)*deltaB0)				#calculate new values of W and B using deltaW and deltaB
	B1 = B1-alpha*((1.0/m)*deltaB1)
	W0, W1 = [], []
	test = 0
	for i in input_layer:
		for W00 in i.weights:	
			W00 = W00 - alpha*((1.0/m)*deltaW0+(theta*W00))
			test = test + 1
			print i.output, test 
		W0.append(i.weights)
	for i in hidden_layer:
		for W11 in i.weights:
			W11 = W11 - alpha*((1.0/m)*deltaW1+(theta*W11))
			print i.output
		W1.append(i.weights)
	return cost_function(input_layer, hidden_layer, output_layer,m,theta), W0, W1, B0, B1	#return value of cost function using new weights and bias

def feed_forward(layer1, layer2, biaslayer):	#feed forward function that applies weights and activation to all nodes in a layer and passes them to the next layer
	for i in range(0, len(layer2)):
		z = 0
		for j in layer1:			
			z=z+j.output*j.weights[i]
		z = z + biaslayer[i]
		layer2[i].input = z
		layer2[i].output=activation(layer2[i])
	return layer2

def output_error(output, input):	#function that works out the error for the output layer
	diff, fdash, error = [], [], []
	for i in range(0, len(output)):
		diff.append(-(input[i].output-output[i].output))
		fdash.append(d_activation(output[i]))
	for i in range(0, len(diff)):
		error.append([diff[i]*fdash[i]])
	return np.matrix(error)

def hidden_error(hidden, out_error):	#function that works out error for hidden layers
	fdash, weights = [], []
	for i in range(0, len(hidden)):
		weights.append(hidden[i].weights)
		fdash.append(d_activation(hidden[i]))
	W = np.matrix(weights)
	diff = np.dot(W, out_error)
	error = []
	for i in range(len(diff.A1)):
		error.append([diff.A1[i]*fdash[i]])
	return np.matrix(error)
	
def compute_partials(error_lplus1, layerl):	#compute partial derivatives for weights and bias
	a = []
	for i in range(0, len(layerl)):
		a.append([layerl[i].output])
	a_l = np.matrix(a)
	deltapW = np.dot(error_lplus1, a_l.T)
	deltapB = error_lplus1
	return deltapW, deltapB
		
def cost_function(inputl, hiddenl, outputl,m,theta):	#calculate value of cost function on current weights and bias
	left = 0
	for i in range(0,len(inputl)):
		left = left + 0.5*pow((outputl[i].output - inputl[i].output),2)
	left = left*(1.0/m)
	right = 0
	for i in inputl:
		for j in i.weights:
			right = right + pow(j,2)
	for i in hiddenl:
		for j in i.weights:
			right = right + pow(j,2)
	right = (theta/2.0)*right
	return left + right
		
class node(object):	#creates node object
	def __init__(self,output,layer, weights=[]):
		#assert input == float 	#check input is an int
		#assert layer == int
		self.input = 0 	#set input attribute to 0; input layer has no input so default is 0
		self.output = output	   	#set output to one given on creation
		self.layer = layer
		self.weights = weights

	def __str__(self):
		return str(self.output)
	def __repr__(self):
		return str(self)
	def __getitem__(self,y):
		return self.y
	def __setitem__(self,y,z):
		self.y = z
	def init_weights(self,nhidden):
		w = []
		for i in range(0,nhidden):
			w.append(random.uniform(-0.1,0.1))
		self.weights = w
if __name__ == "__main__":
	main()
