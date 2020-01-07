from Selector import PySelector, RSelector
from Aggregator import Aggregator

class EFS:
    
    # fs_methods: a tuple (script name, language which the script was written, .rds output name)
    def __init__(self, data_manager, fs_methods, first_aggregator, second_aggregator):

        self.dm = data_manager
        self.fs_methods = self.__generate_fselectors_object(fs_methods)
        self.fst_aggregator = Aggregator(first_aggregator, self.dm)
        self.snd_aggregator = Aggregator(second_aggregator, self.dm)
        

    def __generate_fselectors_object(self, methods):
        
        fs_methods = []
        for script, language, rds_name in methods:
            if language == "python":
                fs_methods.append(
                    PySelector(rds_name, script)
                )
            elif language == "r":
                fs_methods.append(
                    RSelector(rds_name, script)
                )

        return fs_methods

"""
    def selectFeatures(self):

        for k in range(1, self.dm.folds+1):
            self.currentFold = k
            print("\n\n################# Fold iteration:", k, "#################")

            bootstrap = self.dm.getBootStrap(k)
            bagsRankings = []

            for idx, bag in enumerate(bootstrap):
                self.currentBag = idx+1
                print("\n\nBag: ", idx+1, "\n")

                self.__buildRanks(bag["training"])
                bagsRankings.append(self.__meanAggregation(self.rankings))
                self.rankings = []

            finalRanking = self.__meanAggregation(bagsRankings)
            print(finalRanking)

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


    
    def __meanAggregation(self, rankings):
        
        aggregatedRanking = {}  # it's a dictionary where the keys 
                                # represent the genes and its values 
                                # are, at first, the sum of the ranking
                                # positions and, by the end, the mean
                                # value of the rankings 


        for gene in rankings[0].index.values:
            aggregatedRanking[gene] = 0

        for ranking in rankings:
            for gene in ranking.index.values: 
                aggregatedRanking[gene] += ranking.loc[gene, 'rank']

        num_rankings = len(rankings)
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
            rpackages.importr('CORElearn')
        rpackages.importr('FSelectorRcpp')
        rpackages.importr('FSelector')
"""