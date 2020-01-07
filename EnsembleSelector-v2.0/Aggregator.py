import importlib

class Aggregator:

    def __init__(self, aggregation_method, data_manager):
        self.dm = data_manager #TODO: TEST IF THIS IS VISIBLE FOR IMPORTABLE SCRIPTS
        self.aggregate = importlib.import_module("aggreg_algorithms."+aggregation_method).aggregate