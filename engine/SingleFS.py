from Selector import PySelector, RSelector
from DataManager import DataManager
from Constants import *

class SingleFS:
    
    # fs_method: a tuple (script name, language which the script was written, .rds output name)
    def __init__(self, data_manager:DataManager, fs_method):

        self.dm = data_manager
        self.fs_method = self.__generate_fselector_object(fs_method)


        
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