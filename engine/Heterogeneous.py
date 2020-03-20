from Selector import PySelector, RSelector
from Aggregator import Aggregator
from DataManager import DataManager
from Constants import *

class Heterogeneous:
    
    # fs_methods: a tuple (script name, language which the script was written, .rds output name)
    def __init__(self, data_manager:DataManager, fs_methods, aggregator):

        self.dm = data_manager
        self.fs_methods = self.__generate_fselectors_object(fs_methods)
        self.aggregator = Aggregator(aggregator, self.dm)


        
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



    def select_features(self):

        for i in range(self.dm.num_folds):
            print("\n\n################# Fold iteration:", i+1, "#################")
            
            self.dm.current_fold_iteration = i
            output_path = self.dm.get_output_path(fold_iteration=i)

            training_indexes, _ = self.dm.get_fold_data()
            training_data = self.dm.pd_df.loc[training_indexes]

            rankings = []
            for fs_method in self.fs_methods:   
                print("")
                rankings.append(
                    fs_method.select(training_data, output_path)
                )
                
            print("\nAggregating rankings...")
            aggregation = self.aggregator.aggregate(rankings)
            self.dm.save_encoded_ranking(aggregation, 
                                        output_path+AGGREGATED_RANKING_FILE_NAME)
            
        return