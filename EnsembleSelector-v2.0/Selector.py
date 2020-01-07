from DataManager import DataManager as dm
import rpy2.robjects as robjects
import importlib

class FSelector:

    # rds_name: the name of the ranking output produced by the algorithm;
    #           by default, this file is saved in .rds format
    def __init__(self, rds_name, script_name):

        self.rds_name = rds_name
        self.script_name = script_name


class RSelector(FSelector):

    def select(self, dataframe, output_path):
        dataframe = dm.pandas_to_r(dataframe)

        call = "./fs_algorithms/" + self.script_name + ".r"
        robjects.r.source(call)

        ranking = robjects.r["select"](dataframe, output_path+self.rds_name+".rds")
        ranking = dm.r_to_pandas(ranking)

        robjects.r['rm']('list = ls()')
        return ranking


class PySelector(FSelector):

    def __init__(self, rds_name, script_name):
        FSelector.__init__(self, rds_name, script_name)
        self.py_selection = importlib.import_module("fs_algorithms."+script_name).select

    def select(self, dataframe, output_path):
        ranking = self.py_selection(dataframe)
        
        print("Saving data...")
        robjects.r['saveRDS'](dm.pandas_to_r(ranking), output_path+self.rds_name+".rds")
        return ranking