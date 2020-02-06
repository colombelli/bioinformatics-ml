from Selector import PySelector, RSelector
from Aggregator import Aggregator
from DataManager import DataManager
import time
from Constants import *

class EFS:
    
    # fs_methods: a tuple (script name, language which the script was written, .rds output name)
    def __init__(self, data_manager:DataManager, fs_methods, first_aggregator, second_aggregator):

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




    def end_time_and_print(self, start):
        end = time.time()
        hours, rem = divmod(end-start, 3600)
        minutes, seconds = divmod(rem, 60)
        print("\nTime taken:")
        print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
        print("\n")
        return


    def select_features(self):

        for i in range(self.dm.num_folds):
            print("\n\n################# Fold iteration:", i+1, "#################")
            self.dm.current_fold_iteration = i
            self.dm.update_bootstraps()

            snd_layer_rankings = []
            for j, (bootstrap, _) in enumerate(self.dm.current_bootstraps):
                print("\n\nBootstrap: ", j+1, "\n")
                start = time.time()
                output_path = self.dm.get_output_path(i, j)
                bootstrap_data = self.dm.pd_df.loc[bootstrap]

                fst_layer_rankings = []
                for fs_method in self.fs_methods:   
                    print("")
                    fst_layer_rankings.append(
                        fs_method.select(bootstrap_data, output_path)
                    )
                
                print("\nAggregating Level 1 rankings...")
                fs_aggregation = self.fst_aggregator.aggregate(fst_layer_rankings)
                self.dm.save_encoded_ranking(fs_aggregation, 
                                            output_path+AGGREGATED_RANKING_FILE_NAME)
                snd_layer_rankings.append(fs_aggregation)
                self.end_time_and_print(start)
            
            file_path = self.dm.get_output_path(fold_iteration=i) + \
                            AGGREGATED_RANKING_FILE_NAME
            print("\nAggregating Level 2 rankings...")
            final_ranking = self.snd_aggregator.aggregate(snd_layer_rankings)
            self.dm.save_encoded_ranking(final_ranking, file_path)
        return