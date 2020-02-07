from StratifiedKFold import StratifiedKFold
from Constants import *
import numpy as np
import pandas as pd
from sklearn.utils import resample
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from os import mkdir
import sys
import pickle
import urllib.parse
from copy import deepcopy


class DataManager:

    def __init__(self, results_path, file_path, num_bootstraps, 
                num_folds, seed):
        
        self.seed = seed
        np.random.seed(self.seed)
        robjects.r['set.seed'](self.seed)

        self.file_path = file_path
        self.num_bootstraps = num_bootstraps
        self.num_folds = num_folds

        r_df = self.load_RDS(self.file_path)
        self.pd_df = self.encode_df(self.r_to_pandas(r_df))
        self.r_df = self.pandas_to_r(self.pd_df)

        self.results_path = results_path
        try:
            self.__create_results_dir()
        except:
            print("Given directory already created, files will be replaced.")
            print("Note that if there's any missing folder inside this existent one, the execution will fail.")
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


    # The above alnum encode and decode methods were taken from a StackOverflow's 
    # topic answer and sligthly modified. Their original versions are available in:
    # https://stackoverflow.com/questions/32035520/how-to-encode-utf-8-strings-with-only-a-z-a-z-0-9-and-in-python
    @classmethod
    def alnum_encode(self, text):
        if text == "class":
            return text
        return "X" + urllib.parse.quote(text, safe='')\
            .replace('-', '%2d').replace('.', '%2e').replace('_', '%5f')\
            .replace('%', '_')

    @classmethod
    def alnum_decode(self, underscore_encoded):
        if underscore_encoded == "class":
            return underscore_encoded
        underscore_encoded = underscore_encoded[1:]
        return urllib.parse.unquote(underscore_encoded.replace('_','%'), errors='strict')


    @classmethod
    def encode_df(self, df):
        
        print("Encoding dataframe attributes...")
        columns = []
        for attribute in df.columns:
            columns.append(self.alnum_encode(attribute))

        df.columns = columns
        return df

    
    @classmethod
    def decode_df(self, df):

        print("Decoding dataframe attributes...")
        columns = []
        for attribute in df.columns:
            columns.append(self.alnum_decode(attribute))

        df.columns = columns
        return df


    @classmethod
    def save_encoded_ranking(self, ranking, file_name_and_dir):
        encoded_ranking = deepcopy(ranking)
        decoded_ranking = self.decode_df(encoded_ranking)
        print("Saving ranking...")
        r_decoded_ranking = self.pandas_to_r(decoded_ranking)
        robjects.r["saveRDS"](r_decoded_ranking, file_name_and_dir)
        return


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


    def get_fold_data(self):
        training_data = self.folds[self.current_fold_iteration][0]
        testing_data = self.folds[self.current_fold_iteration][1]
        return (training_data, testing_data)