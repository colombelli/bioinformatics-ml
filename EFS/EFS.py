import pandas as pd
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
import subprocess


class EFS:

    def __init__(self, filePath):

        self.filePath = filePath

        self.bags = 30
        self.folds = 10

        self.relief = True
        self.gainRatio = True
        self.symmetricalUncertainty = True
        self.oneR = False
        self.svmRFE = False

        self.df = self.__loadRDS()
        
    
    def __loadRDS(self):
        
        readRDS = robjects.r['readRDS']
        return readRDS(self.filePath)



    def __bootStrap(self):

        print("something")


    def buildRanks(self):
        
        readRDS = robjects.r['readRDS']
        df = readRDS(self.filePath)

        rpackages.importr('CORElearn')

        if self.relief:
            
            outputPath = "rf.rds"
            robjects.r.source('./fs-algorithms/reliefNoDsReread.r')
            output = robjects.r['relief'](df, outputPath)
            print(output)
            

            

    def __getReliefRank(self):
        return
