import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
import numpy as np
import matplotlib.pyplot as plt

def print_shape(name, tensor):
    print(name + " is a {}-d Tensor with shape: {}".format(tf.rank(tensor).numpy(), tf.shape(tensor)))
# Tensor Manipulation

# 0-D or scalar examples
sport = tf.constant("Tennis", tf.string)
number = tf.constant(1.44314312, tf.float64)

# rank returns a tensor 0-D tensor with the dimension
# not the same as mathematical rank
print("sport rank: ", tf.rank(sport).numpy())
print("number rank: ", tf.rank(number).numpy())

# lists as 1-d Tensors
sports = tf.constant(["Tennis", "Basketball"], tf.string)
numbers = tf.constant([3.141592, 1.414213, 2.7894], tf.float64)
print("`sports` is a {}-d Tensor with shape: {}".format(tf.rank(sports).numpy(), tf.shape(sports)))
print("`numbers` is a {}-d Tensor with shape: {}".format(tf.rank(numbers).numpy(), tf.shape(numbers)))

# 2D tensor or matrix
matrix = tf.constant([[0, 1, 4], [2, 3, 4], [5, 1, 3]], tf.int32)

assert isinstance(matrix, tf.Tensor), "matrix must be a tf Tensor object"
assert tf.rank(matrix).numpy() == 2
print_shape('matrix', matrix)

# 4-D tensor
# Can be a set of 3-D Tensors
images = tf.zeros([10, 256, 256, 3], tf.int32)

assert isinstance(images, tf.Tensor), "matrix must be a tf Tensor object"
assert tf.rank(images).numpy() == 4, "matrix must be of rank 4"
assert tf.shape(images).numpy().tolist() == [10, 256, 256, 3], "matrix is incorrect shape"
print_shape('images', images)

# Slicing
row_vector = matrix[0]
column_vector = matrix[:,0]
scalar = matrix[1, 2]

print("`row_vector`: {}".format(row_vector.numpy()))
print("`column_vector`: {}".format(column_vector.numpy()))
print("`scalar`: {}".format(scalar.numpy()))

# Tensor Computation
# Create the nodes in the graph, and initialize values
a = tf.constant(15)
b = tf.constant(61)

# Add them!
c1 = tf.add(a,b)
c2 = a + b # TensorFlow overrides the "+" operation so that it is able to act on Tensors
print(c1)
print(c2)

# Tensor computation function
# Construct a simple computation function
def func(a,b):
  c = a + b
  d = b - 1
  e = c * d
  return e

# Apply function
out = func(a, b)
print("Out Tensor: {}".format(out))

# Neural Network
# Custom Layers

# n_output_nodes: number of output nodes
# input_shape: shape of the input
# x: input to the layer

class OurDenseLayer(tf.keras.layers.Layer):
  def __init__(self, n_output_nodes):
    super(OurDenseLayer, self).__init__()
    self.n_output_nodes = n_output_nodes

  def build(self, input_shape):
    d = int(input_shape[-1])
    # Define and initialize parameters: a weight matrix W and bias b
    # Note that parameter initialization is random! This initializes random parameters
    self.W = self.add_weight("weight", shape=[d, self.n_output_nodes])
    self.b = self.add_weight("bias", shape=[1, self.n_output_nodes])
    # The dimensionality follows mat mul rules extends to tensors

  def call(self, x):
    z = tf.matmul(x, self.W)
    y = tf.sigmoid(z)
    return y

# Since layer parameters are initialized randomly, we will set a random seed for reproducibility
tf.random.set_seed(1)
layer = OurDenseLayer(3)
layer.build((1,2))
x_input = tf.constant([[1,2.]], shape=(1,2))
y = layer.call(x_input)

# test the output!
print(y.numpy())

# Sequential API
# Define the number of outputs
n_output_nodes = 3
# First define the model 
model = Sequential()
# defines a dense layer assuming batch size as dim0 
# output and input vectors such that 
# out shape: (batch_size, n_output_nodes) 
# in shape: (batch_size, n_inputs) ex [[1, 3, 5], [1, 3, 7]] : (2, 3) 
dense_layer = Dense(n_output_nodes, input_shape=(2,))
# Add the dense layer to the model
model.add(dense_layer)
# example input
x_input = tf.constant([[1,3.]], shape=(1,2))
# model ouput
model_out = model.predict(x_input)
print(model_out)

# Gradient Calculation
# Initialize a random value for our initial x
x = tf.Variable([tf.random.normal([1])])
print("Initializing x={}".format(x.numpy()))

learning_rate = 1e-2 # learning rate for SGD
history = []
# Define the target value
x_f = 4

# We will run SGD for a number of iterations. At each iteration, we compute the loss, 
#   compute the derivative of the loss with respect to x, and perform the SGD update.
for i in range(500):
  with tf.GradientTape() as tape:
    loss = (x - x_f) * (x - x_f)

  # loss minimization using gradient tape
  grad = tape.gradient(loss, x) # compute the derivative of the loss with respect to x
  new_x = x - learning_rate*grad # sgd update
  x.assign(new_x) # update the value of x
  history.append(x.numpy()[0])

# Plot the evolution of x as we optimize towards x_f!
plt.plot(history)
plt.plot([0, 500],[x_f,x_f])
plt.legend(('Predicted', 'True'))
plt.xlabel('Iteration')
plt.ylabel('x value')
plt.show()