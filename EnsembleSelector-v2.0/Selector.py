from DataManager import DataManager as dm
import rpy2.robjects as robjects
import importlib

class FSelector:

    # selector: if an r script is used, then this parameter must have the same name
    #           as the r function which implements the feature selection algorithm
    #           -> see examples in fs_scripts directory

    # rds_name: the name of the ranking output produced by the algorithm;
    #           by default, this file is saved in .rds format
    def __init__(self, rds_name, script_name, selector = None):

        self.rds_name = rds_name
        self.script_name = script_name
        self.selector = selector


class RSelector(FSelector):

    def select(self, dataframe, output_path):
        dataframe = dm.pandas_to_r(dataframe)

        call = "./fs_algorithms/" + self.script_name + ".r"
        robjects.r.source(call)

        ranking = robjects.r[self.selector](dataframe, output_path+self.rds_name+".rds")
        ranking = dm.r_to_pandas(ranking)

        robjects.r['rm']('list = ls()')
        return ranking


class PySelector(FSelector):

    def __init__(self, rds_name, script_name, selector = None):
        FSelector.__init__(self, rds_name, script_name, selector)
        self.py_selection = importlib.import_module("fs_algorithms."+script_name).select

    def select(self, dataframe, output_path):
        ranking = self.py_selection(dataframe)
        
        print("Saving data...")
        robjects.r['saveRDS'](dm.pandas_to_r(ranking), output_path+self.rds_name+".rds")
        return ranking