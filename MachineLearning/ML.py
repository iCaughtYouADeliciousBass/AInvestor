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
    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias
        self.log = Logger.Logger()
        self.log.append('info', 'Node created successfully')

    def feed_forward(self, inputs):
        # Weight inputs, add bias, then use the activation function
        total = numpy.dot(self.weights, inputs) + self.bias
        return sigmoid(total)


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


# ------------------------Generate Model Shape Function-----------------------------------------------------------------


def generate_model_shape(shape: list, inputs: list):
    shape = [[5], [0, 90, 100, 100, 0]]
    inputs = [[1], [90], [100], [100], [1]]
    # represents inputs to node, therefore one above would be 3 deep, 1 hidden, 1 in and 1 out

    #           [1]
    #   [90 ]   [1]
    #   [100]   [1]     [1]
    #   [100]   [1]
    #           [1]

    for a in range(shape):
        #       cnt = 0
        #       If range(shape) > a > 1 then Node.HiddenNode = True
        #       Node.Depth = a
        if len(shape[a]) == 1:
            pass
        #           Create Node w/ input # of value test[a]

        else:
            for b in range(len(shape[a])):
                pass
    #           Create len(test[a]) Nodes w/ test[a][b] inputs, if test[a][b] == 0 or a == range(shape), Node.inputNode
    #           is TRUE


    #           cnt++



    #           How do we give these inputs properly??
    #           for node in nodes
    #               for input in node.inputs
    #

    pass
