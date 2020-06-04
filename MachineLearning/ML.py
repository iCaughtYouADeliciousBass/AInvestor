# ------------------  IMPORTS  -----------------------------------------------------------------------------------------
import numpy
import matplotlib
import pandas
import sklearn
import AInvestor.Logger as Logger


# ------------------------Sigmoid Function------------------------------------------------------------------------------

def sigmoid(x):
    return 1.0 / (1.0 + numpy.exp(-x))


# ------------------------Neuron Class----------------------------------------------------------------------------------

class Neuron:
    def __init__(self, weights, input_count, inp=[], bias=0.0, x=0, y=0):
        self.weights = weights
        self.bias = bias
        self.x = x
        self.y = y
        self.input = inp
        self.input_count = input_count

    def feed_forward(self, inputs):
        # Weight inputs, add bias, then use the activation function
        if len(inputs) != len(self.weights):
            inputs = inputs[:len(self.weights)]
        if type(inputs) == 'list':
            inputs = numpy.array(inputs)
        total = numpy.dot(self.weights, inputs) + self.bias
        return sigmoid(total)


# ------------------------Neuron Connection Class-----------------------------------------------------------------------

class NeuronConnection:
    def __init__(self, inp, out_x, out_y):
        self.input = inp
        self.out_x = out_x
        self.out_y = out_y

# ------------------------Neural Network Class--------------------------------------------------------------------------


class NeuralNetwork:
    def __init__(self):
        self.weights_h1 = numpy.array([1.0, 1.0, 1.0])
        self.weights_h2 = numpy.array([1.0, 1.0, 1.0])
        self.weights_h3 = numpy.array([1.0, 1.0, 1.0])
        self.weights_h4 = numpy.array([1.0, 1.0, 1.0])
        self.weights_h5 = numpy.array([1.0, 1.0, 1.0])
        self.weights_o1 = numpy.array([1.0, 1.0, 1.0, 1.0, 1.0])
        self.bias_h1 = 0.0
        self.bias_h2 = 0.0
        self.bias_h3 = 0.0
        self.bias_h4 = 0.0
        self.bias_h5 = 0.0
        self.bias_o1 = 0.0

        self.h1 = Neuron(self.weights_h1, self.bias_h1)
        self.h2 = Neuron(self.weights_h2, self.bias_h2)
        self.h3 = Neuron(self.weights_h3, self.bias_h3)
        self.h4 = Neuron(self.weights_h4, self.bias_h4)
        self.h5 = Neuron(self.weights_h5, self.bias_h5)
        self.o1 = Neuron(self.weights_o1, self.bias_o1)

        self.log = Logger.Logger()
        self.log.append('info', 'Network created successfully')

    def feed_forward(self, x1, x2, x3, x4, x5):
        out_h1 = self.h1.feed_forward(x1)
        out_h2 = self.h2.feed_forward(x2)
        out_h3 = self.h3.feed_forward(x3)
        out_h4 = self.h4.feed_forward(x4)
        out_h5 = self.h5.feed_forward(x5)
        out_o1 = self.o1.feed_forward(numpy.array([out_h1, out_h2, out_h3, out_h4, out_h5]))
        return out_o1


# ------------------------Neural Network Class--------------------------------------------------------------------------

class NeuralModel:
    def __init__(self, output_node: Neuron, hidden_nodes: list):
        self.output_node = output_node
        self.hidden_nodes = hidden_nodes

    def feed_forward(self):
        out_array = []
        out_neuron_out = 0.0
        for a in range(len(self.hidden_nodes), -1, -1):
            if a != 0:
                for b in range(len(self.hidden_nodes[a-1])):
                    self.output_node.input.append(self.hidden_nodes[a-1][b].feed_forward(self.hidden_nodes[a-1][b].input))
#            else:
#                for i in out_array:
#                    self.hidden_nodes[a-1][0].input.append(i)
#                out_neuron_out = self.hidden_nodes[a-1][0].feed_forward(self.hidden_nodes[a-1][0].input)
        return self.output_node.feed_forward(self.output_node.input)


# ------------------------Generate Model Shape Function-----------------------------------------------------------------


def generate_model(shape: list, inputs: list):
    #shape = [[5], [0, 90, 100, 100, 0]]
    #inputs = [[1], [90], [100], [100], [1]]
    # represents inputs to node, therefore one above would be 3 deep, 1 hidden, 1 in and 1 out

    #           [1]
    #   [90 ]   [1]
    #   [100]   [1]     [1]
    #   [100]   [1]
    #           [1]
    hidden_node_array = []
    input_node_array = []
    for a in range(len(shape)):
        input_array = []
        if a == 0:
            # Lazy assumption this is output node
            try:
                for i in range(len(shape[a+1])):
                    if shape[a+1][i] == 0:
                        input_array.append(inputs[i][0])

                out_node = Neuron(weights=numpy.ones(shape[a]), inp=input_array, input_count=shape[a][0])
            except ValueError:
                print("Out of Index when searching for next Neurons list for inputs")

        elif len(shape[a]) > 1:
            # Assume all between first and last are hidden nodes
            temp_array = []
            for b in range(len(shape[a])):
                if shape[a][b] != 0:
                    temp_array.append(Neuron(x=a, y=b, weights=numpy.ones(shape[a][b]), inp=inputs[b],
                                                    input_count=shape[a][b]))
            hidden_node_array.append(temp_array)
    model = NeuralModel(out_node, hidden_node_array)
    return model.feed_forward()