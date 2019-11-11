import pandas as pd
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from fs_algorithms.svm_rfe import svmRFE
import numpy as np


class EFS:

    def __init__(self, filePath, chosenFS, bags, folds):

        self.filePath = filePath
        self.chosenFS = chosenFS
        self.bags = bags
        self.folds = folds
        

        self.df = self.__loadRDS()

        
    
    def __loadRDS(self):
        
        print("Loading dataset...")
        readRDS = robjects.r['readRDS']
        return readRDS(self.filePath)



    def __bootStrapNoReplacement(self, data, bags=30, seed=None, trainFraction=0.8):
        
        np.random.seed(seed)

        pd_df = self.__rToPandas(self.df)

        return



    def buildRanks(self):
        

        rpackages.importr('CORElearn')
        rpackages.importr('FSelectorRcpp')
        rpackages.importr('FSelector')

        if self.chosenFS['relief']:
            self.reliefRank = self.__callRFSelectionScript("rf", "relief", "relief")


        if self.chosenFS['gainRatio']:
            self.gainRatioRank = self.__callRFSelectionScript("gr", 
                                                    "gain-ratio-cpp", "gainRatio")


        if self.chosenFS['symmetricalUncertainty']:
            self.symUncRank = self.__callRFSelectionScript("su", 
                                        "symmetrical-uncertainty", "symUnc")


        if self.chosenFS['oneR']:
            self.oneRRank = self.__callRFSelectionScript("or", "oneR", "oneRule")


        if self.chosenFS['svmRFE']:
            
            pdDF = self.__rToPandas(self.df)
            svmRFERank = svmRFE(pdDF)

            self.svmRFERank = self.__pandasToR(svmRFERank)

            print("Saving data...")
            robjects.r['saveRDS'](self.svmRFERank, "./ranks/svmrfe.rds")


    def __pandasToR(self, df):

        with localconverter(robjects.default_converter + pandas2ri.converter):
            rFromPandasDF = robjects.conversion.py2rpy(df)
        return rFromPandasDF


    def __rToPandas(self, df):
        
        with localconverter(robjects.default_converter + pandas2ri.converter):
                pdFromRDF = robjects.conversion.rpy2py(df)
        return pdFromRDF



    def __callRFSelectionScript(self, rdsName, scriptName, featureSelector):

        outputPath = "./ranks/" + rdsName + ".rds"
        call = "./fs-algorithms/" + scriptName + ".r"
        robjects.r.source(call)
        
        return robjects.r[featureSelector](self.df, outputPath)
            
            

"""

    for k in folds:

        self.bagPdDF, foldRDF = dm.getBootsrap(k)
        self.buildRanks()



    def __buildRanks(self):

        

"""