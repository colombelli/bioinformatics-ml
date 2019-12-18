import pandas as pd
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
from fs_algorithms.svm_rfe import svmRFE
import numpy as np


class EFS:

    def __init__(self, dataManager, chosenFS):

        self.dm = dataManager
        self.chosenFS = chosenFS
        


    def selectFeatures(self):

        for k in range(1, self.dm.folds+1):
            
            bootstrap = self.dm.getBootStrap(k)
            bagsRanks = []

            for bag in bootstrap:

                ranks = self.__buildRanks(bag["training"])
                bagsRanks.append(self.__unweightedAggregation(ranks))

            finalRank = self.__weightedAggregation(bagsRanks)
        
        return finalRank



    def __buildRanks(self, df):
        
        
        pdDF = df
        rDF = self.dm.pandasToR(pdDF)

        rpackages.importr('CORElearn')
        rpackages.importr('FSelectorRcpp')
        rpackages.importr('FSelector')


        if self.chosenFS['relief']:
            self.reliefRank = self.__callRFSelectionScript(rDF, "rf", "relief", "relief")


        if self.chosenFS['gainRatio']:
            self.gainRatioRank = self.__callRFSelectionScript(rDF, "gr", 
                                                    "gain-ratio-cpp", "gainRatio")


        if self.chosenFS['symmetricalUncertainty']:
            self.symUncRank = self.__callRFSelectionScript(rDF, "su", 
                                        "symmetrical-uncertainty", "symUnc")


        if self.chosenFS['oneR']:
            self.oneRRank = self.__callRFSelectionScript(rDF, "or", "oneR", "oneRule")


        if self.chosenFS['svmRFE']:
            
            svmRFERank = svmRFE(pdDF)
            self.svmRFERank = self.dm.pandasToR(svmRFERank)

            print("Saving data...")
            robjects.r['saveRDS'](self.svmRFERank, "./ranks/svmrfe.rds")

        return 0


    def __callRFSelectionScript(self, df, rdsName, scriptName, featureSelector):

        outputPath = "./ranks/" + rdsName + ".rds"
        call = "./fs_algorithms/" + scriptName + ".r"
        robjects.r.source(call)
        
        return robjects.r[featureSelector](df, outputPath)


    
    def __unweightedAggregation(self, ranks):

        return 0


    def __weightedAggregation(self, bagsRanks):

        return 0
    