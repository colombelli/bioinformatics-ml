from Selector import PySelector, RSelector
from Aggregator import Aggregator
from DataManager import DataManager
from Constants import *

class Homogeneous:
    
    # fs_methods: a tuple (script name, language which the script was written, .rds output name)
    def __init__(self, data_manager:DataManager, fs_method, aggregator):

        self.dm = data_manager
        self.fs_method = self.__generate_fselector_object(fs_method)
        self.aggregator = Aggregator(aggregator, self.dm)


        
    def __generate_fselector_object(self, method):
        
        (script, language, rds_name) = method
        if language == "python":
            return PySelector(rds_name, script)
            
        elif language == "r":
            return RSelector(rds_name, script)



    def select_features(self):

        for i in range(self.dm.num_folds):
            print("\n\n################# Fold iteration:", i+1, "#################")
            self.dm.current_fold_iteration = i
            self.dm.update_bootstraps()

            rankings = []
            for j, (bootstrap, _) in enumerate(self.dm.current_bootstraps):
                print("\n\nBootstrap: ", j+1, "\n")
                
                output_path = self.dm.get_output_path(i, j)
                bootstrap_data = self.dm.pd_df.loc[bootstrap]
                rankings.append(self.fs_method.select(bootstrap_data, output_path))

                
            print("\nAggregating rankings...")
            output_path = self.dm.get_output_path(fold_iteration=i)
            aggregation = self.aggregator.aggregate(rankings)
            self.dm.save_encoded_ranking(aggregation, 
                                        output_path+AGGREGATED_RANKING_FILE_NAME)
            
        return