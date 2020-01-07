from Selector import PySelector, RSelector
from Aggregator import Aggregator
from DataManager import DataManager

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



    def select_features(self):

        for i, (training_fold, testing_fold) in enumerate(self.dm.folds):
            print("\n\n################# Fold iteration:", i, "#################")
            self.dm.current_fold_iteration = i
            self.dm.update_bootstraps()

            snd_layer_rankings = []
            for j, (bootstrap, oob_observation) in enumerate(self.dm.current_bootstraps):
                print("\n\nBootstrap: ", j+1, "\n")
                output_path = self.dm.get_output_path(i, j)

                fst_layer_rankings = []
                for fs_method in self.fs_methods:
                    fst_layer_rankings.append(
                        fs_method.select(bootstrap, output_path)
                    )
                
                fs_aggregation = self.fst_aggregator.aggregate(fst_layer_rankings)
                self.dm.save_aggregated_ranking(fs_aggregation, output_path)
                snd_layer_rankings.append(fs_aggregation)
            
            output_path = self.dm.get_output_path(fold_iteration=i)
            final_ranking = self.snd_aggregator.aggregate(snd_layer_rankings)
            self.dm.save_aggregated_ranking(final_ranking, output_path)