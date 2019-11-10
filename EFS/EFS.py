import pandas as pd
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
#import sys
#sys.path.insert(0, './feature-selection/svm_rfe.py')
#from svm_rfe import svmRFE

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



    def __bootStrap(self):

        print("something")


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
            self.svmRFERank = svmRFE(self.df)
            robjects.r['saveRDS'](self.svmRFERank, "./ranks/svmrfe.rds")



    def __callRFSelectionScript(self, rdsName, scriptName, featureSelector):

        outputPath = "./ranks/" + rdsName + ".rds"
        call = "./fs-algorithms/" + scriptName + ".r"
        robjects.r.source(call)
        
        return robjects.r[featureSelector](self.df, outputPath)
            
            

