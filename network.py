from typing import List
from neuron import *
import pandas as pd


class Network:
    def __init__(self, df: pd.DataFrame):
        self.levels_amount = len(df['level'].unique())  # кол-во элементов
        self.levels = []
        for i in range(self.levels_amount):
            self.levels.append(self._get_neurons_of_this_level(df, i).copy())
        self.amount_of_external = self._get_amount_of_external_synapses()

    def __str__(self):
        result = ""
        for level in self.levels:
            for neuron in level:
                for synapse in neuron.synapses:
                    result += str(int(synapse.type))
                result += ' '
            result += '\n'
        return result

    def _get_amount_of_external_synapses(self):
        result = 0
        for level in self.levels:
            for neuron in level:
                for synapses in neuron.synapses:
                    result += 1 if not synapses.source_id else result
        return result

    def _get_neurons_of_this_level(self, df: pd.DataFrame, number: int) -> List[Neuron]:
        result = []
        needed = df[df['level'].isin([number])]
        needed = needed.to_dict('records')
        for line in needed:
            neuron = Neuron(line['id'], line['synapses'], line['threshold'], line['activators'])
            neuron.set_synapses(line['connections'])
            result.append(neuron)  # result[-1].set_synapses(line['connections'])
        return result

    def process(self, external_signals: str = None) -> bool:
        if external_signals is None:
            external_signals = [False] * self.amount_of_external
        else:
            external_signals = list(external_signals)
            external_signals = [bool(int(i)) for i in external_signals]

        if len(external_signals) != self.amount_of_external:
            raise ValueError("Количество сигналов не совпадает с количеством внешних синапсов")

        external_signals = self.calc_neuron_value(self.levels[0][0], external_signals, 0)

        for i in range(1, self.levels_amount):  # уровень
            for k in range(len(self.levels[i])):  # нейрон
                external_signals = self.calc_neuron_value(self.levels[i][k], external_signals, i)

        return self.levels[0][0].exit

    def calc_neuron_value(self, neuron: Neuron, external_signals: list, level: int) -> list:
        signals = []
        for synapse in neuron.synapses:
            if synapse.source_id == 0:
                signals.append(external_signals[0])
                external_signals = external_signals[1:]
            else:
                signals.append(self.levels[level + 1][self._get_index_on_level(synapse.source_id, level + 1)].exit)

        neuron.get_result(signals)
        return external_signals

    def _get_index_on_level(self, source_id, level) -> int:
        for i in range(len(self.levels[level])):
            if self.levels[level][i].ID == source_id:
                return i
        raise ValueError("Некорректный адрес")


    def print_conditions(self):
        for level in self.levels:
            for neuron in level:
                print(int(neuron.exit), end='')
            print(" ")
