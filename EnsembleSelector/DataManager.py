import numpy as np
import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter


MAX_SEED = 99999999

class DataManager:

    def __init__(self, filePath, bags, folds, seed=None, bagTrainFraction=0.8):
        
        self.seed = seed
        self.__validateSeed()

        self.filePath = filePath
        self.bags = bags
        self.folds = folds
        self.bagTrainFraction = bagTrainFraction

        self.rDF = self.__loadRDS()
        self.pdDF = self.__rToPandas(self.rDF)

        self.__calculateFolds()


    def __validateSeed(self):
        if self.seed is not None:
            if self.seed >= MAX_SEED:
                raise("Seed must be less than"+str(MAX_SEED))
        return

    
    def __loadRDS(self):
        
        print("Loading dataset...")
        readRDS = robjects.r['readRDS']
        return readRDS(self.filePath)


    def __pandasToR(self, df):

        with localconverter(robjects.default_converter + pandas2ri.converter):
            rFromPandasDF = robjects.conversion.py2rpy(df)
        return rFromPandasDF


    def __rToPandas(self, df):
        
        with localconverter(robjects.default_converter + pandas2ri.converter):
                pdFromRDF = robjects.conversion.rpy2py(df)
        return pdFromRDF



    def __calculateFolds(self):

        samplesPerFold = len(self.pdDF) // self.folds

        self.foldIdx = {}
        previousFold = 0

        for f in range(1, self.folds+1):
            self.foldIdx[str(f)] = range(previousFold, previousFold + samplesPerFold)
            previousFold = previousFold + samplesPerFold
            
        
        # fix last fold 
        lastFoldFirstIdx = self.foldIdx[str(self.folds)][0]
        self.foldIdx[str(self.folds)] = range(lastFoldFirstIdx, len(self.pdDF))




    def getBootStrap(self, k):
        
        
        kIdx = self.foldIdx[str(k)]
        foldData = self.pdDF.iloc[kIdx]


        numTrainingSamples = round(len(foldData) * self.bagTrainFraction)
        sampleRangeSequence = np.arange(0, len(foldData))
        bootstrap = []   # a list containg tuples with two elements: 
                          # training indexes for that bag,
                          # testing indexes for that bag                                          

        
        np.random.seed(self.seed)

        for _ in range(self.bags):
            
            np.random.shuffle(sampleRangeSequence)
            training =  sampleRangeSequence[0:numTrainingSamples]
            testing = sampleRangeSequence[numTrainingSamples:]
            
            bootstrap.append({"training": training, 
                              "testing": testing})
            
            # in order to keep shuffling randomly (but to maintain reproducibility),
            # we use the given seed to generate another seed which will be used in the
            # next iteration shuffling; and we change the attribute seed in order to 
            # continuously perform a random shuffling for the next folds.
            self.seed = np.random.randint(0, MAX_SEED) 
            np.random.seed(self.seed)


        return bootstrap



