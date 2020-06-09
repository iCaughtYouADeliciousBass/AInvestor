# ------------------  IMPORTS  -----------------------------------------------------------------------------------------
import numpy
import matplotlib
import pandas
import sklearn
import AInvestor.Logger as Logger
from AInvestor.config import DATABASE_NAME, USERNAME, PASSWORD, ENDPOINT, PORT
import pymysql

# ------------------------Connection to SQL Server----------------------------------------------------------------------

connection = pymysql.connect(host=ENDPOINT, user=USERNAME, passwd=PASSWORD, db=DATABASE_NAME, port=PORT)


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

class NeuralModel:
    def __init__(self, output_node: Neuron, hidden_nodes: list):
        self.output_node = output_node
        self.hidden_nodes = hidden_nodes

    def feed_forward(self):
        out_array = []
        out_neuron_out = 0.0
        self.hidden_nodes = self.hidden_nodes[0]
        for a in range(len(self.hidden_nodes)-1, -1, -1):
            self.output_node.input.append(self.hidden_nodes[a].feed_forward(self.hidden_nodes[a].input))
        return self.output_node.feed_forward(self.output_node.input)


# ------------------------Generate Model Shape Function-----------------------------------------------------------------


def generate_model(stock):
    try:
        db = pymysql.connect(host=ENDPOINT, user=USERNAME, passwd=PASSWORD, db=DATABASE_NAME, port=PORT)
        cursor = db.cursor()
        query = 'SELECT * FROM AInvestor.ML_Stock_Models where stock_and_itvl LIKE "%{}%";'.format(stock.name)
        cursor.execute(query)
        query_data = cursor.fetchall()
        if len(query_data) > 0:
            print("Machine Learning Model : {} was found!".format(stock.name))
            #stock.model_exists = True
            stock.model_data = query_data
        else:
            print("Machine Learning Model : {} was not found, I will generate one for you.".format(stock.name))

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        db.close()

    if stock.model_exists:
        # GENERATE FROM SQL DATA
        return 0

    else:
        shape = [[5], [0, len(stock.EMA), len(stock.MACD), len(stock.RSI), 0]],
        inputs = [[stock.MA], stock.EMA, stock.MACD, stock.RSI, [stock.Momentum]]
        shape = shape[0]
        hidden_node_array = []
        input_node_array = []
        out_node = 0

        for a in range(len(shape)):
            input_array = []
            if a == 0:
                # Lazy assumption this is output node
                try:
                    for i in range(len(shape[a + 1])):
                        if shape[a + 1][i] == 0:
                            if i == 0:
                                input_array.append(20 * (inputs[i][0] / stock.price - 1))
                            else:
                                input_array.append(inputs[i][0])

                    out_node = Neuron(weights=numpy.ones(shape[0][a]), inp=input_array, input_count=shape[a][0])
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
        return NeuralModel(out_node, hidden_node_array)