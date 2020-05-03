import importlib

class Aggregator:

    # heavy: tells whether to use the heavy selection method, i. e., for each fold
    #   iteration, build a dictionary containing all rankings from
    #   all fs methods and keep it in memory until the next fold iteration. This is
    #   useful if you want, for example, to measure the stability of the first layer
    #   rankings of each fs method(in the Hybrid ensemble, for example).
    def __init__(self, aggregation_method, data_manager):
        self.aggregation_method = aggregation_method
        self.dm = data_manager
        self.heavy = self.__is_heavy_required()
        
    def aggregate(self, rankings): 
        agg_foo = importlib.import_module("aggreg_algorithms."+self.aggregation_method).aggregate
        return agg_foo(self, rankings)

    def __is_heavy_required(self):
        try:
            return importlib.import_module("aggreg_algorithms."+self.aggregation_method).heavy
        except:
            return False