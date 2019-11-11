import pandas as pd
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from fs_algorithms.svm_rfe import svmRFE
import numpy as np


class EFS:

    def __init__(self, dataManager, chosenFS, folds):

        self.dm = dataManager
        self.chosenFS = chosenFS
        self.folds = folds
        



    def selectFeatures(self):

        for k in self.folds:

            bootsrap = self.dm.getBootsrap(k)
            bagsRanks = []

            for bag in bootsrap:

                ranks = self.__buildRanks(bag["train"])
                bagsRanks.append(self.__unweightedAggregation(ranks))

            finalRank = self.__weightedAggregation(bagsRanks)



    def __buildRanks(self, samplesIdx):
        

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



    def __callRFSelectionScript(self, rdsName, scriptName, featureSelector):

        outputPath = "./ranks/" + rdsName + ".rds"
        call = "./fs-algorithms/" + scriptName + ".r"
        robjects.r.source(call)
        
        return robjects.r[featureSelector](self.df, outputPath)


    
    def __unweightedAggregation(self, ranks):

        return 0


    def __weightedAggregation(self, bagsRanks):

        return 0
    