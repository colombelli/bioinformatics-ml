import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from os import mkdir
import sys
import pickle


class DataManager:

    def __init__(self, results_path, file_path, num_bootstraps, 
                num_folds, seed):
        
        self.seed = seed
        np.random.seed(self.seed)

        self.file_path = file_path
        self.num_bootstraps = num_bootstraps
        self.num_folds = num_folds

        self.r_df = self.__load_RDS()
        self.pd_df = self.r_to_pandas(self.r_df)

        self.results_path = results_path
        try:
            self.__create_results_dir()
        except:
            print("Given directory already created, files will be replaced.")
            if input("Input c to cancel or any other key to continue... ") == "c":
                sys.exit()

        self.folds = None
        self.__calculate_folds()
        self.__save_folds()


    def __create_results_dir(self):
        print("Creating results directory...")
        mkdir(self.results_path)

        for i in range(1, self.num_folds+1):
            fold_dir = self.results_path+"/fold_"+str(i)
            mkdir(fold_dir)

            for j in range(1, self.num_bootstraps+1):
                bag_dir = fold_dir + "/bootstrap_"+str(j)
                mkdir(bag_dir)


    
    def __load_RDS(self):
        
        print("Loading dataset...")
        read_RDS = robjects.r['readRDS']
        return read_RDS(self.file_path)


    @classmethod
    def pandas_to_r(self, df):
        with localconverter(robjects.default_converter + pandas2ri.converter):
            r_from_pandas_df = robjects.conversion.py2rpy(df)
        return r_from_pandas_df


    @classmethod
    def r_to_pandas(self, df):
        with localconverter(robjects.default_converter + pandas2ri.converter):
                pandas_from_r_df = robjects.conversion.rpy2py(df)
        return pandas_from_r_df



    def __calculate_folds(self):

        k = self.num_folds
        kf = KFold(k, shuffle=True, random_state=self.seed)
        self.folds = list(kf.split(self.pd_df))
        return

    
    def __save_folds(self):
        
        file = self.results_path + "fold_sampling.pkl"
        with open(file, 'wb') as f:
            pickle.dump(self.folds, f)
        return




"""
    def __setTestFoldSubset(self, k):

        kIdx = self.foldIdx[k]
        self.testingFoldData = self.pdDF.iloc[kIdx]

        return


    def getBootStrap(self, k):
        
        self.__setTestFoldSubset(k)

        trainingFolds = pd.concat([self.pdDF, self.testingFoldData])
        trainingFolds = trainingFolds.drop_duplicates(keep=False, inplace=False)

        numTrainingSamples = round(len(trainingFolds) * self.bagTrainFraction)
        sampleRangeSequence = np.arange(0, len(trainingFolds))
        bootstrap = []    # a list containg tuples with two elements: 
                          # training data for that bag,
                          # testing data for that bag                                          


        for _ in range(self.bags):
            
            np.random.shuffle(sampleRangeSequence)

            trainingIdx =  sampleRangeSequence[0:numTrainingSamples]
            trainingDataBag = trainingFolds.iloc[trainingIdx]

            testingIdx = sampleRangeSequence[numTrainingSamples:]
            testingDataBag = trainingFolds.iloc[testingIdx]
            
            bootstrap.append({"training": trainingDataBag, 
                              "testing": testingDataBag})
            

        return bootstrap
"""

        
