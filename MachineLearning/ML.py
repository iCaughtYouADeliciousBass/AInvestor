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


# ------------------------Check for Children Function-------------------------------------------------------------------
def check_for_children(l: list):
    for i in l:
        if type(i) == str:
            if i.find(";"):
                return True
    return False


# ------------------------String to List Function-----------------------------------------------------------------------

def string_to_list(string: str, stock):
    out_list = []
    has_input_nodes = False
    try:
        string = string.replace("'", "")
        string = string.replace("[", "")
        string = string.replace("]", "")
        start_index = 0
        while start_index < len(string):
            end_index = string.find(',', start_index)
            if end_index == -1:
                out_list.append(string[start_index:])
                break
            out_list.append(string[start_index:end_index])
            start_index = end_index + 1
        for i in range(len(out_list)):
            if out_list[i].find('.') != -1 and type(out_list[i]) == str:
                if len(out_list) == 1:
                    out_list = eval(out_list[i])
                else:
                    out_list[i] = eval(out_list[i])
            elif out_list[i].find(';'):
                has_input_nodes = True
    except Exception as e:
        print(e)
    finally:
        return out_list


# ------------------------Sigmoid Function------------------------------------------------------------------------------

def sigmoid(x):
    return 1.0 / (1.0 + numpy.exp(-x))


# ------------------------Neuron Class----------------------------------------------------------------------------------

class Neuron:
    def __init__(self, weights, input_count, inp=None, bias=0.0, x=0, y=0, input_as_string=None):
        self.weights = weights
        self.bias = bias
        self.x = x
        self.y = y
        self.input = inp
        self.input_count = input_count
        self.input_as_string = input_as_string

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
        for a in range(len(self.hidden_nodes) - 1, -1, -1):
            self.output_node.input.append(self.hidden_nodes[a].feed_forward(self.hidden_nodes[a].input))
        return self.output_node.feed_forward(self.output_node.input)


# ------------------------Generate Model Shape Function-----------------------------------------------------------------


def generate_model(stock):
    hidden_node_array = []
    out_node = None
    try:
        db = pymysql.connect(host=ENDPOINT, user=USERNAME, passwd=PASSWORD, db=DATABASE_NAME, port=PORT)
        cursor = db.cursor()
        query = 'SELECT * FROM AInvestor.ML_Stock_Models where stock_and_itvl LIKE "%{}%";'.format(stock.name)
        cursor.execute(query)
        model_exists = cursor.fetchall()
        if len(model_exists) > 0:
            print("Machine Learning Model : {} was found!".format(stock.name))
            stock.model_exists = True
            model_query = 'SELECT sm.stock_and_itvl, sn.x, sn.y, sn.bias, sn.input, sn.weight ' \
                          + 'FROM AInvestor.ML_Stock_Models sm INNER JOIN AInvestor.ML_Stock_Nodes sn ' \
                          + 'ON sm.stock_and_itvl = sn.stock_and_itvl ' \
                          + 'where sm.stock_and_itvl LIKE "%{}%" ' \
                            'ORDER BY sn.x DESC, sn.y DESC;'.format(stock.name)
            cursor.execute(model_query)
            stock.model_data = cursor.fetchall()
        else:
            print("Machine Learning Model : {} was not found, I will generate one for you.".format(stock.name))
        cursor.close()
        db.close()

    except Exception as e:
        print(e)

    if stock.model_exists:
        # GENERATE FROM SQL DATA
        for s in stock.model_data:
            inp = string_to_list(s[4], stock)
            weights = list(map(int, string_to_list(s[5], stock)))
            has_children = check_for_children(inp)
            if has_children:
                for i in inp:
                    if type(i) == str:
                        if ";" in i:
                            split = i.find(";")
                            x_val = int(i[:split])
                            y_val = int(i[split + 1:])
                            for n in hidden_node_array:
                                if n.x == x_val and n.y == y_val:
                                    inp[inp.index(i)] = n.feed_forward(n.input)
                if s[1] == 0 and s[2] == 0:
                    out_node = Neuron(weights, len(inp), inp, float(s[3]), int(s[1]), int(s[2]))
                else:
                    hidden_node_array.append(Neuron(weights, len(inp), inp, float(s[3]), int(s[1]), int(s[2])))
            else:
                hidden_node_array.append(Neuron(weights, len(inp), inp, float(s[3]), int(s[1]), int(s[2])))

    else:
        shape = [[5], [0, len(stock.EMA), len(stock.MACD), len(stock.RSI), 0]]
        inputs = ["stock.MA", "stock.EMA", "stock.MACD", "stock.RSI", "stock.Momentum"]

        for a in range(len(shape) - 1, -1, -1):
            input_array = []
            input_string_array = []
            if a == 0:
                # Lazy assumption this is output node
                try:
                    for i in range(len(shape[a + 1])):
                        if shape[a + 1][i] == 0:
                            input_array.append(eval(inputs[i]))
                            input_string_array.append(inputs[i])
                    for h in hidden_node_array[0]:
                        if h.x == a + 1:
                            input_string_array.append("{};{}".format(h.x, h.y))
                            input_array.append(h.feed_forward(h.input))
                    out_node = Neuron(weights=numpy.ones(shape[0][a]), inp=input_array, input_count=shape[a][0],
                                      input_as_string=input_string_array)
                except ValueError:
                    print("Out of Index when searching for next Neurons list for inputs")

            elif len(shape[a]) > 1:
                # Assume all between first and last are hidden nodes
                temp_array = []
                for b in range(len(shape[a])):
                    if shape[a][b] != 0:
                        temp_array.append(Neuron(x=a, y=b, weights=numpy.ones(shape[a][b]), inp=eval(inputs[b]),
                                                 input_count=shape[a][b], input_as_string=inputs[b]))
                hidden_node_array.append(temp_array)
        model_insert_query = "INSERT INTO AInvestor.ML_Stock_Models (stock_and_itvl, stock, itvl) " \
                             + 'VALUES ("{}", {}, "{}");'.format(stock.name, stock.name[:stock.name.find("_")],
                                                                 stock.interval)
        node_insert_list = []
        hidden_node_array = hidden_node_array[0]
        hidden_node_array.append(out_node)
        for n in hidden_node_array:
            node_insert_query = "INSERT INTO AInvestor.ML_Stock_Nodes " \
                                + "(stock_key, stock, itvl, x, y, bias, input, stock_and_itvl, weight) " \
                                + 'VALUES ("{}", "{}", {}, {}, {}, {}, "{}", "{}", "{}");'.format(stock.name + "_" +
                                                                                                  str(n.x) + "_" +
                                                                                                  str(n.y),
                                                                                                  stock.name[
                                                                                                  :stock.name.find(
                                                                                                      "_")],
                                                                                                  stock.interval, n.x,
                                                                                                  n.y, n.bias,
                                                                                                  n.input_as_string,
                                                                                                  stock.name,
                                                                                                  list(n.weights))
            node_insert_list.append(node_insert_query)

        try:
            db = pymysql.connect(host=ENDPOINT, user=USERNAME, passwd=PASSWORD, db=DATABASE_NAME, port=PORT)
            cursor = db.cursor()
            cursor.execute(model_insert_query)
            for q in node_insert_list:
                cursor.execute(q)
            db.commit()
            cursor.close()
            db.close()

        except Exception as e:
            print(e)

    return NeuralModel(out_node, hidden_node_array)
