import importlib

class Aggregator:

    def __init__(self, aggregation_method):
        self.aggregate = importlib.import_module("aggreg_algorithms."+aggregation_method).aggregate