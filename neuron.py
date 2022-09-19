class Synapse:
    def __init__(self, type: bool, source_id: int = 0):
        self.type = type  # True - возбуждающий
        self.source_id = source_id  # 0 - внешний (нет источника)


class Neuron:
    def __init__(self, ID: int, synapses_amount: int, threshold: int, activators: int):
        self.ID = ID
        self.threshold = threshold  # порог вхождения
        self.synapses_amount = synapses_amount  # количество входов
        self.synapses = []
        self.activators = activators  # количество возбуждающих
        self.freezers = synapses_amount - activators  # количество тормозящих
        self.exit = False  # Результат нейрона

    def set_synapses(self, connections: str):  # 21 10 241 - последний символ это тип, остальное ID
        connections = connections.strip().split(" ")
        if len(connections) != self.synapses_amount:
            print("Неверное количество синапсов!")
            return

        for connection in connections:  # заполнение массива синапсов
            synapse_type = bool(int(connection[-1]))
            source_id = int(connection[:-1])
            self.synapses.append(Synapse(synapse_type, source_id))

    def get_result(self, signals: list) -> bool:  # принимает сигналы
        counter = 0
        for i in range(self.synapses_amount):
            if not self.synapses[i].type and signals[i]:
                return False
            elif self.synapses[i].type and signals[i]:
                counter += 1
        if counter >= self.threshold:
            return True
        return False
