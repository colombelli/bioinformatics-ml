import importlib

class Aggregator:

    def __init__(self, aggregation_method, data_manager):
        self.aggregation_method = aggregation_method
        self.dm = data_manager
        
    def aggregate(self, rankings): 
        agg_foo = importlib.import_module("aggreg_algorithms."+self.aggregation_method).aggregate
        return agg_foo(self, rankings)