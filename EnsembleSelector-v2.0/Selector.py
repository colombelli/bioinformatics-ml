from DataManager import DataManager as dm
import rpy2.robjects as robjects
from fs_algorithms.svm_rfe import svmRFE

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

        ranking = robjects.r[self.selector](dataframe, output_path+self.rds_name)
        ranking = dm.r_to_pandas(ranking)

        robjects.r['rm']('list = ls()')
        return ranking


class SVMRFE(FSelector):

    def select(self, dataframe, output_path):
        print("Using SVM-RFE...")
        ranking = svmRFE(dataframe)
            
        ranking = dm.pandas_to_r(ranking)
        print("Saving data...")
        robjects.r['saveRDS'](ranking, output_path+self.rds_name)
        return ranking