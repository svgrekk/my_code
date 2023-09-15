import numpy as np
import scipy.special


class Neuron:

    def __init__(self, input_size):
        self.weights = np.random.rand(input_size) * 0.1
        self.bias = np.random.randint(1) * 0.1
        self.output = None
        self.sigmoid = lambda x: scipy.special.expit(x)

        self.delta = None

    def recieve(self, input):
        res = np.sum(input * self.weights) + self.bias
        return res

    def acitvate(self, input):
        summed = self.recieve(input)
        self.output = self.sigmoid(summed)
        return self.output

    def get_error(self,expected):
        return self.output - expected

    def __repr__(self):
        res = 'weights: '
        res += str(self.weights)
        res += ' output: '
        res += str(self.output)
        res += 'delta'
        res += self.delta
        return res


class NeuroNetwork:

    def __init__(self, input_size, hidden_size, output_size):

        self.input = []
        self.hidden = [Neuron(input_size)] * hidden_size
        self.output = [Neuron(hidden_size)] * output_size

    def forward_propager(self, input_list):
        self.input = input_list
        for neuron in self.hidden:
            neuron.acitvate(input_list)

        for o_neur in self.output:
            for h_ner in self.hidden:
                o_neur.acitvate(h_ner.output)

        print('Hidden: ')
        print(self.hidden)
        print('Output')
        print(self.output)

    def transer_derivative(self,output):
        return output * (1 - output)


    def back_propagate_error(self, expected):
        expected = np.array(expected)
        output = [i.output for i in self.output]
        output = np.array(output)
        errors = expected - output

        for neour, err in zip(self.output,errors):
            neour.delta = err * self.transer_derivative(neour.output)

        for neour in self.output:
            neour.weights *= neour.delta

        h_output = [[i.output for i in self.hidden]]
        h_output = np.array(h_output)
        h_errors = expected - h_output

        for neour, h_err in zip(self.hidden,h_errors):
            neour.delta = h_err * self.transer_derivative(neour.output)

















a = [0.2, 0.8, 3]
n = NeuroNetwork(3, 3, 1)
n.forward_propager(a)
