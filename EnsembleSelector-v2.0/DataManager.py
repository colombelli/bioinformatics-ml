from StratifiedKFold import StratifiedKFold
import numpy as np
import pandas as pd
from sklearn.utils import resample
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from os import mkdir
import sys
import pickle


MAX_SEED = 9999999

class DataManager:

    def __init__(self, results_path, file_path, num_bootstraps, 
                num_folds, seed):
        
        self.seed = seed
        np.random.seed(self.seed)

        self.file_path = file_path
        self.num_bootstraps = num_bootstraps
        self.num_folds = num_folds

        self.r_df = self.load_RDS(self.file_path)
        self.pd_df = self.r_to_pandas(self.r_df)

        self.results_path = results_path
        try:
            self.__create_results_dir()
        except:
            print("Given directory already created, files will be replaced.")
            if input("Input c to cancel or any other key to continue... ") == "c":
                sys.exit()

        self.folds = None
        self.__calculate_folds()
        self.__save_folds()

        self.current_fold_iteration = 0
        self.current_bootstraps = None



    def __create_results_dir(self):
        print("Creating results directory...")
        mkdir(self.results_path)

        for i in range(1, self.num_folds+1):
            fold_dir = self.results_path+"/fold_"+str(i)
            mkdir(fold_dir)

            for j in range(1, self.num_bootstraps+1):
                bag_dir = fold_dir + "/bootstrap_"+str(j)
                mkdir(bag_dir)


    @classmethod
    def load_RDS(self, file_path):
        
        print("Loading data...")
        read_RDS = robjects.r['readRDS']
        return read_RDS(file_path)


    @classmethod
    def pandas_to_r(self, df):
        with localconverter(robjects.default_converter + pandas2ri.converter):
            r_from_pandas_df = robjects.conversion.py2rpy(df)
        return r_from_pandas_df


    @classmethod
    def r_to_pandas(self, df):
        with localconverter(robjects.default_converter + pandas2ri.converter):
                pandas_from_r_df = robjects.conversion.rpy2py(df)
        return pandas_from_r_df



    def __calculate_folds(self):

        k = self.num_folds
        skf = StratifiedKFold(self.seed, self.pd_df, "class", k)
        self.folds = list(skf.split())
        return

    
    def __save_folds(self):
        
        file = self.results_path + "fold_sampling.pkl"
        with open(file, 'wb') as f:
            pickle.dump(self.folds, f)
        return


    def update_bootstraps(self):
        self.current_bootstraps = self.__get_bootstraps()
        self.__save_bootstraps()


    # Output: A list of tuples containing n tuples representing the n 
    #           (bootstraps, out-of-bag) samples
    def __get_bootstraps(self):
        
        training_data = self.folds[self.current_fold_iteration][0]
        num_bs_samples = len(training_data)
        
        bootstraps_oob = []
        for _ in range(self.num_bootstraps):
            bootstrap = resample(training_data, replace=True, n_samples=num_bs_samples,
                                random_state=self.seed)
            oob = np.array([x for x in training_data if x not in bootstrap])
            bootstraps_oob.append((bootstrap, oob))
            self.update_seed()  # in order to keep deterministically (but "randomly") sampling

        return bootstraps_oob


    def __save_bootstraps(self):

        path = self.results_path + "fold_" + str(self.current_fold_iteration+1) + "/bootstrap_"
        for i, bootstrap in enumerate(self.current_bootstraps):
            file = path + str(i+1) + "/bootstrap_sampling.pkl" 
            with open(file, 'wb') as f:
                pickle.dump(bootstrap, f)
        return

    
    def update_seed(self):
        self.seed = np.random.randint(0, high=MAX_SEED)
        with open(self.results_path+"seed.pkl", 'wb') as f:
                pickle.dump(self.seed, f)


    def get_output_path(self, fold_iteration=None, bootstrap_iteration=None):
        
        path = self.results_path

        if fold_iteration is None:
            return path
        
        path += "fold_" + str(fold_iteration+1) + "/"
        if bootstrap_iteration is None:
            return path
        
        path += "bootstrap_" + str(bootstrap_iteration+1) + "/"
        return path


    def save_aggregated_ranking(self, ranking, output_path):
        file = output_path + "aggregated_ranking.rds"
        rds_format = self.pandas_to_r(ranking)
        robjects.r['saveRDS'](rds_format, file)
        return
