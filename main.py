from neuron import *

if __name__ == '__main__':
    adam = Neuron(1, 3, 2, 2)
    adam.set_synapses("00 01 01")
    counter = 0
    vector = [True, True, True]
    print(adam.get_result([True, True, True]))

