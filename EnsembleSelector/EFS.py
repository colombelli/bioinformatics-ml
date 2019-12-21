import pandas as pd
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
from fs_algorithms.svm_rfe import svmRFE
import numpy as np
import Evaluate


class EFS:

    def __init__(self, dataManager, chosenFS):

        self.dm = dataManager
        self.chosenFS = chosenFS
        self.currentFold = 0
        self.currentBag = 0
        self.rankings = []

        rpackages.importr('CORElearn')
        rpackages.importr('FSelectorRcpp')
        rpackages.importr('FSelector')

    def selectFeatures(self):

        for k in range(1, self.dm.folds+1):
            self.currentFold = k
            print("\n\n################# Fold iteration:", k, "#################\n\n")

            bootstrap = self.dm.getBootStrap(k)
            bagsRankings = []

            for idx, bag in enumerate(bootstrap):
                self.currentBag = idx+1
                print("Bag: ", idx+1, "\n")

                self.__buildRanks(bag["training"])
                bagsRankings.append(self.__meanAggregation())
                self.rankings = []

            finalRanking = self.__weightedAggregation(bagsRankings)
        
        return finalRanking



    def __buildRanks(self, df):
        
        
        pdDF = df
        rDF = self.dm.pandasToR(pdDF)


        if self.chosenFS['relief']:
            self.rankings.append(self.__callRFSelectionScript(rDF, "rf", "relief", "relief"))
            robjects.r['rm']('list = ls()')


        if self.chosenFS['gainRatio']:
            self.rankings.append(self.__callRFSelectionScript(rDF, "gr", 
                                                    "gain-ratio-cpp", "gainRatio"))
            robjects.r['rm']('list = ls()')


        if self.chosenFS['symmetricalUncertainty']:
            self.rankings.append(self.__callRFSelectionScript(rDF, "su", 
                                        "symmetrical-uncertainty", "symUnc"))
            robjects.r['rm']('list = ls()')


        if self.chosenFS['oneR']:
            self.rankings.append(self.__callRFSelectionScript(rDF, "or", "oneR", "oneRule"))
            robjects.r['rm']('list = ls()')


        if self.chosenFS['svmRFE']:
            
            svmRFERank = svmRFE(pdDF)
            self.rankings.append(svmRFERank)
            
            svmRFERank = self.dm.pandasToR(svmRFERank)
            print("Saving data...")
            outputPath = self.dm.resultsPath + "/fold_" + str(self.currentFold) + "/bag_" + \
                        str(self.currentBag) + "/svmrfe.rds"
            robjects.r['saveRDS'](svmRFERank, outputPath)



    def __callRFSelectionScript(self, df, rdsName, scriptName, featureSelector):

        outputPath =    self.dm.resultsPath + "/fold_" + str(self.currentFold) + "/bag_" + \
                        str(self.currentBag) + "/" + rdsName + ".rds"
        call = "./fs_algorithms/" + scriptName + ".r"
        robjects.r.source(call)

        return self.dm.rToPandas(robjects.r[featureSelector](df, outputPath))


    
    def __meanAggregation(self):
        
        aggregatedRanking = {}  # it's a dictionary where the keys 
                                # represent the genes and its values 
                                # are, at first, the sum of the ranking
                                # positions and, by the end, the mean
                                # value of the rankings 


        for gene in self.rankings[0].index.values:
            aggregatedRanking[gene] = 0

        for ranking in self.rankings:
            for gene in ranking.index.values: 
                aggregatedRanking[gene] += ranking.loc[gene, 'rank']

        num_rankings = len(self.rankings)
        for gene, ranking in aggregatedRanking.items():
            aggregatedRanking[gene] /= num_rankings 


        finalRanking = pd.DataFrame.from_dict(aggregatedRanking, orient='index')
        finalRanking.columns = ['rank']
       
        return finalRanking.sort_values(by='rank')
 

    def __unweightedAggregation(self):
        raise Exception('This method must be implemented')
        return 0


    def __weightedAggregation(self, bagsRanks):
        raise Exception('This method must be implemented')
        return 0
    