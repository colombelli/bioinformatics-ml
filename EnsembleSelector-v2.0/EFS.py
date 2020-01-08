from Selector import PySelector, RSelector
from Aggregator import Aggregator
from DataManager import DataManager
from Evaluate import Evaluate
import pickle

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

        for i in range(self.dm.num_folds):
            print("\n\n################# Fold iteration:", i+1, "#################")
            self.dm.current_fold_iteration = i
            self.dm.update_bootstraps()

            snd_layer_rankings = []
            for j, (bootstrap, _) in enumerate(self.dm.current_bootstraps):
                print("\n\nBootstrap: ", j+1, "\n")
                output_path = self.dm.get_output_path(i, j)
                bootstrap_data = self.dm.pd_df.iloc[bootstrap]

                fst_layer_rankings = []
                for fs_method in self.fs_methods:   
                    print("")
                    fst_layer_rankings.append(
                        fs_method.select(bootstrap_data, output_path)
                    )
                
                fs_aggregation = self.fst_aggregator.aggregate(fst_layer_rankings)
                self.dm.save_aggregated_ranking(fs_aggregation, output_path)
                snd_layer_rankings.append(fs_aggregation)
            
            output_path = self.dm.get_output_path(fold_iteration=i)
            final_ranking = self.snd_aggregator.aggregate(snd_layer_rankings)
            self.dm.save_aggregated_ranking(final_ranking, output_path)



    def evaluate_final_rankings(self, thresholds):
        
        final_rankings = self.__get_final_rankings()
        with open(self.dm.results_path, 'rb') as f:
                folds_sampling = pickle.load(f)
        
        aucs = self.__compute_aucs(final_rankings, thresholds, folds_sampling)
        stabilities = self.__compute_stabilities(final_rankings, thresholds)

        return aucs, stabilities

    

    def __get_final_rankings(self):

        final_rankings = []
        for fold_iteration in range(self.dm.num_folds):
            ranking_path = self.dm.results_path + "fold_" + str(fold_iteration+1) + "/"
            file = ranking_path + "aggregated_ranking.rds"
            ranking = self.dm.load_RDS(file)
            final_rankings.append(ranking)

        return final_rankings

    
    def __compute_aucs(self, final_rankings, thresholds, folds_sampling):
        
        fold_aucs = []
        i = 1
        for training, testing in folds_sampling:
            training_df = self.dm.pd_df.iloc[training]
            testing_df = self.dm.pd_df.iloc[testing]
            evaluator = Evaluate(final_rankings, None, training_df, testing_df)
            
            th_aucs = []
            for th in thresholds:
                evaluator.threshold = th
                th_aucs.append(evaluator.get_auc())
            fold_aucs.append(th_aucs)

            i+=1
        return fold_aucs


    def __compute_stabilities(self, final_rankings, thresholds):
        
        evaluator = Evaluate(final_rankings, None, None, None)
        th_stabilities = []
        for th in thresholds:
            evaluator.threshold = th
            th_stabilities.append(evaluator.get_stability())
        
        return th_stabilities