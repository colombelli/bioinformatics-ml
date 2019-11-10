import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
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

        if self.relief:
            rScript = "./fs-algorithms/relief.r"
            outputPath = "rf.rds"


            subprocess.call (["/usr/bin/Rscript", "--vanilla", rScript,
                                "-i", self.filePath, "-o", outputPath])
            
            readRDS = robjects.r['readRDS']
            df = readRDS('./fs-algorithms/rf.rds')
            print(df.head())

    def __getReliefRank(self):
        return
