from typing import List
from neuron import *
import pandas as pd


class Network:
    def __init__(self, df: pd.DataFrame):
        self.levels_amount = len(df['level'].unique())  # кол-во элементов
        self.levels = []
        for i in range(self.levels_amount):
            self.levels.append(self.get_neurons_of_this_level(df, i).copy())

    def get_neurons_of_this_level(self, df: pd.DataFrame, number: int) -> List[Neuron]:
        result = []
        needed = df[df['level'].isin([number])]
        needed = needed.to_dict('records')
        for line in needed:
            neuron = Neuron(line['id'], line['synapses'], line['threshold'], line['activators'])
            neuron.set_synapses(line['connections'])
            result.append(neuron)  # result[-1].set_synapses(line['connections'])
        return result

    def __str__(self):
        result = ""
        for level in self.levels:
            for neuron in level:
                for synapse in neuron.synapses:
                    result += str(int(synapse.type))
                result += ' '
            result += '\n'
        return result
