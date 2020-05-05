from engine.DataManager import DataManager as dm
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

        call = "./engine/fs_algorithms/" + self.script_name + ".r"
        robjects.r.source(call)

        ranking = robjects.r["select"](dataframe)
        ranking = dm.r_to_pandas(ranking)
        
        dm.save_encoded_ranking(ranking, output_path+self.rds_name)

        robjects.r['rm']('list = ls()')
        return ranking


class PySelector(FSelector):

    def __init__(self, rds_name, script_name):
        FSelector.__init__(self, rds_name, script_name)
        self.py_selection = importlib.import_module("engine.fs_algorithms."+script_name).select

    def select(self, dataframe, output_path):
        ranking = self.py_selection(dataframe)
        dm.save_encoded_ranking(ranking, output_path+self.rds_name)
        return ranking