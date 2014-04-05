import image_sae
import cPickle, gzip, numpy, random

# Load the dataset
f = gzip.open('mnist.pkl.gz', 'rb')
train_set, valid_set, test_set = cPickle.load(f)
f.close()
dataset, labelset  = train_set
data = dataset[0:50]
label = labelset[0:50]
alpha = 100
m = 2
theta = 0.001
costfunc = []
weights = []
nhidden = 14
for i in range(0, len(data)):
	w0, w1, b0, b1 = [], [], [], []
	for i in range(0,28):
		temp = []
		for j in range(0,nhidden):
			temp.append(random.uniform(-0.1,0.1))
			b0.append(random.uniform(-0.1,0.1))
		w0.append(temp)
	for i in range(0,nhidden):
		temp = []
		for j in range(0,28):
			temp.append(random.uniform(-0.1,0.1))
			b1.append(random.uniform(-0.1,0.1))
		w1.append(temp)
	weights.append([w0,w1])
bias = [b0,b1]
for i in range(0,len(data)):
	costfunc.append(image_sae.main(data[i],weights[i], bias,alpha,m,theta))
print costfunc
	

