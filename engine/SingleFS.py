from engine.Selector import FSelector, PySelector, RSelector
from engine.DataManager import DataManager
from engine.Constants import *

class SingleFS:
    
    # fs_method: a single elemet list (to maintain coherence) whose element is a tuple: 
    # (script name, language which the script was written, .csv output name)
    def __init__(self, data_manager:DataManager, fs_method):

        self.dm = data_manager
        self.fs_method = FSelector.generate_fselectors_object(fs_method)[0]



    def select_features(self):

        for i in range(self.dm.num_folds):
            print("\n\n################# Fold iteration:", i+1, "#################")
            
            self.dm.current_fold_iteration = i
            output_path = self.dm.get_output_path(fold_iteration=i)

            training_indexes, _ = self.dm.get_fold_data()
            training_data = self.dm.pd_df.loc[training_indexes]

            ranking = self.fs_method.select(training_data, output_path)

            # in order to reuse Evaluator class, we need an AGGREGATED_RANKING_FILE_NAME.rds
            # accessible inside each fold iteration folder, so we simply resave the only
            # ranking we have with the appropriate name
            self.dm.save_encoded_ranking(ranking, 
                                        output_path+AGGREGATED_RANKING_FILE_NAME)
            
        return