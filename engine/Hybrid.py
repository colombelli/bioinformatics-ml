from Selector import PySelector, RSelector
from Aggregator import Aggregator
from DataManager import DataManager
from Constants import *
import multiprocessing as mp

class Hybrid:
    
    # fs_methods: a tuple (script name, language which the script was written, .rds output name)
    def __init__(self, data_manager:DataManager, fs_methods, 
    first_aggregator, second_aggregator, thresholds):

        self.dm = data_manager
        self.thresholds = thresholds

        self.fs_methods = self.__generate_fselectors_object(fs_methods)
        self.fst_aggregator = Aggregator(first_aggregator)
        self.snd_aggregator = Aggregator(second_aggregator)

        if self.fst_aggregator.heavy or self.snd_aggregator.heavy:
            self.select_features = self.select_features_heavy
        else:
            self.select_features = self.select_features_light

        self.rankings_to_aggregate = None
            


        
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



    def select_features_light(self):
    
        for i in range(self.dm.num_folds):
            
            print("\n\n################# Fold iteration:", i+1, "#################")
            self.dm.current_fold_iteration = i
            self.dm.update_bootstraps()

            snd_layer_rankings = []
            for j, (bootstrap, _) in enumerate(self.dm.current_bootstraps):
                print("\n\nBootstrap: ", j+1, "\n")
                output_path = self.dm.get_output_path(i, j)
                bootstrap_data = self.dm.pd_df.loc[bootstrap]

        
                fst_layer_rankings = []
                for fs_method in self.fs_methods:   
                    print("")
                    fst_layer_rankings.append(
                        fs_method.select(bootstrap_data, output_path)
                    )
                
                print("\nAggregating Level 1 rankings...")
                self.__set_rankings_to_aggregate(fst_layer_rankings)
                fs_aggregation = self.fst_aggregator.aggregate(self)
                self.dm.save_encoded_ranking(fs_aggregation, 
                                            output_path+AGGREGATED_RANKING_FILE_NAME)
                snd_layer_rankings.append(fs_aggregation)
            

            file_path = self.dm.get_output_path(fold_iteration=i) + \
                            AGGREGATED_RANKING_FILE_NAME
            print("\n\nAggregating Level 2 rankings...")
            self.__set_rankings_to_aggregate(snd_layer_rankings)
            final_ranking = self.snd_aggregator.aggregate(self)
            self.dm.save_encoded_ranking(final_ranking, file_path)
        return



    def select_features_heavy(self):
    
        for i in range(self.dm.num_folds):
            
            print("\n\n################# Fold iteration:", i+1, "#################")
            self.dm.current_fold_iteration = i
            self.dm.update_bootstraps()

            bs_rankings = {}
            for j, (bootstrap, _) in enumerate(self.dm.current_bootstraps):
                print("\n\nBootstrap: ", j+1, "\n")
                output_path = self.dm.get_output_path(i, j)
                bootstrap_data = self.dm.pd_df.loc[bootstrap]

        
                fst_layer_rankings = []
                for fs_method in self.fs_methods:   
                    print("")
                    fst_layer_rankings.append(
                        fs_method.select(bootstrap_data, output_path)
                    )
                
                bs_rankings[j] = fst_layer_rankings
                
            print("\nAggregating Level 1 rankings...")
            fs_aggregations = self.fst_aggregator.aggregate(self)
            snd_layer_rankings = []
            for fs_aggregation in fs_aggregations:
                self.dm.save_encoded_ranking(fs_aggregation, 
                                                output_path+AGGREGATED_RANKING_FILE_NAME)
                snd_layer_rankings.append(fs_aggregation)
            
            self.dm.bs_rankings = bs_rankings
            file_path = self.dm.get_output_path(fold_iteration=i) + \
                            AGGREGATED_RANKING_FILE_NAME
            print("\n\nAggregating Level 2 rankings...")
            self.__set_rankings_to_aggregate(snd_layer_rankings)
            final_ranking = self.snd_aggregator.aggregate(self)
            self.dm.save_encoded_ranking(final_ranking, file_path)
        return



    def __set_rankings_to_aggregate(self, rankings):
        self.rankings_to_aggregate = rankings
        return