import numpy as np
import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter


MAX_SEED = 99999999

class DataManager:

    def __init__(self, filePath, bags, folds, seed=None):

        self.filePath = filePath
        self.bags = bags
        self.folds = folds
        

        self.rDF = self.__loadRDS()
        self.pdDF = self.__rToPandas(self.rDF)
    
        if seed is not None:
            if seed >= MAX_SEED:
                raise("Seed must be less than"+str(MAX_SEED))
        self.seed = seed

    
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




    def getBootStrap(self, data, seed=None, trainFraction=0.8):
        
        

        np.random.seed(seed)

        numTrainingSamples = round(len(data)*trainFraction)
        sampleRangeSequence = np.arange(0, len(data))
        bootstrap = []   # a list containg tuples with two elements: 
                          # training indexes for that bag,
                          # testing indexes for that bag                                          

      
        for _ in range(self.bags):
            
            np.random.shuffle(sampleRangeSequence)
            training =  sampleRangeSequence[0:numTrainingSamples]
            testing = sampleRangeSequence[numTrainingSamples:]
            
            bootstrap.append((training, testing))
            
            # in order to keep shuffling randomly (but to maintain reproducibility),
            # we use the given seed to generate another seed which will be used in the
            # next iteration shuffling
            newSeed = np.random.randint(0, MAX_SEED) 
            np.random.seed(newSeed)


        return bootstrap



    def getFoldIndexes(self, fold):

        return