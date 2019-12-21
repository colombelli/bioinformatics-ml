import numpy as np
import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from os import mkdir
import sys


class DataManager:

    def __init__(self, resultsPath, filePath, bags, folds, seed=None, bagTrainFraction=0.8):
        
        self.seed = seed
        np.random.seed(self.seed)

        self.filePath = filePath
        self.bags = bags
        self.folds = folds
        self.bagTrainFraction = bagTrainFraction

        self.rDF = self.__loadRDS()
        self.pdDF = self.rToPandas(self.rDF)
        
        self.__calculateFolds()

        self.resultsPath = resultsPath
        try:
            self.__createResultsDir()
        except:
            print("Provided directory already created, files will be replaced.")
            if input("Continue? y/n ") == "n":
                sys.exit()


    def __createResultsDir(self):
        print("Creating result directory...")
        mkdir(self.resultsPath)

        for i in range(1, self.folds+1):
            foldDir = self.resultsPath+"/fold_"+str(i)
            mkdir(foldDir)

            for j in range(1, self.bags+1):
                bagDir = foldDir + "/bag_"+str(j)
                mkdir(bagDir)


    
    def __loadRDS(self):
        
        print("Loading dataset...")
        readRDS = robjects.r['readRDS']
        return readRDS(self.filePath)


    def pandasToR(self, df):

        with localconverter(robjects.default_converter + pandas2ri.converter):
            rFromPandasDF = robjects.conversion.py2rpy(df)
        return rFromPandasDF


    def rToPandas(self, df):
        
        with localconverter(robjects.default_converter + pandas2ri.converter):
                pdFromRDF = robjects.conversion.rpy2py(df)
        return pdFromRDF



    def __calculateFolds(self):

        samplesPerFold = len(self.pdDF) // self.folds

        self.foldIdx = {}
        previousFold = 0

        for f in range(1, self.folds+1):
            self.foldIdx[f] = list(range(previousFold, previousFold + samplesPerFold))
            previousFold = previousFold + samplesPerFold
        
        # fix last fold (which should get the remaining data without wasting 
        # it because of the round operation //)
        lastFoldFirstIdx = self.foldIdx[self.folds][0]
        self.foldIdx[self.folds] = list(range(lastFoldFirstIdx, len(self.pdDF)))


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


        
