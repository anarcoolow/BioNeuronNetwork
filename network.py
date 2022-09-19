from typing import List
from neuron import *
import pandas as pd


class Network:
    def __init__(self, df: pd.DataFrame):
        self.levels_amount = len(df['level'].unique())  # кол-во элементов
        self.levels = []
        for i in range(self.levels_amount):
            self.levels.append(self.get_neurons_of_this_level(df, i))

    def get_neurons_of_this_level(self, df: pd.DataFrame, number: int) -> List[Neuron]:
        result = []
        needed = df[df['level'].isin([number])]
        for line in needed:
            result.append(Neuron(line['id'], line['synapses'], line['threshold'], line['activators']).set_synapses(
                line['connections']))  # result[-1].set_synapses(line['connections'])

        return result
