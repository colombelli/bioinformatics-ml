import pandas as pd
import pickle
import glob
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import metrics
import numpy as np
import kuncheva_index as ki
from DataManager import DataManager
from Constants import *

class Evaluator:

    # th_in_fraction: bool  => if the threshold values are fractions or integers
    def __init__(self, data_manager:DataManager, thresholds, th_in_fraction):

        self.dm = data_manager
        
        self.thresholds = None
        self.frac_thresholds = None
        self.__init_thresholds(thresholds, th_in_fraction)

        self.aucs = None
        self.stabilities = None
        self.rankings = None
        self.training_x = None
        self.training_y = None
        self.testing_x = None
        self.testing_y = None

    
    def __init_thresholds(self, thresholds, th_in_fraction):
        if th_in_fraction:
            self.thresholds, self.frac_thresholds = self.get_int_thresholds(thresholds)
        else:
            self.thresholds, self.frac_thresholds = self.get_frac_thresholds(thresholds)
        return


    def get_int_thresholds(self, thresholds):

        dataset_len = len(self.dm.pd_df.columns)

        updated_fraction_thresholds = []
        int_thresholds = []
        for th in thresholds:

            int_th = int(dataset_len * th/100)
            if not(int_th):
                print("0 int threshold value detected for fraction", th, "- skipping.")
                continue

            updated_fraction_thresholds.append(th)
            int_thresholds.append(int_th)

        print("\nNumber of genes to select given the threshold percentages:")
        print(int_thresholds, "\n\n")
        return int_thresholds, updated_fraction_thresholds


    def get_frac_thresholds(self, thresholds):

        dataset_len = len(self.dm.pd_df.columns)

        updated_int_thresholds = []
        frac_thresholds = []
        for th in thresholds:

            if not(th):
                print("0 int threshold value detected for fraction", th, "- skipping.")
                continue

            if th > dataset_len - 1:
                print("Given threshold value,", str(th)+", is greater the number of features - skipping.")

            updated_int_thresholds.append(th)
            frac_th = (th * 100) / dataset_len
            frac_thresholds.append(frac_th)

        print("\nNumber of genes to select given the threshold percentages:")
        print(updated_int_thresholds, "\n\n")
        return updated_int_thresholds, frac_thresholds




    def __get_gene_lists(self, pd_rankings):
        gene_lists = []

        for ranking in pd_rankings:
            index_names_arr = ranking.index.values
            gene_lists.append(list(index_names_arr))
        
        return gene_lists


    def __get_x(self, df, genes):
        return df.loc[:, genes]
    
    def __get_y(self, df):
        return df.loc[:, ['class']].T.values[0]



    def get_auc(self):
        
        clf = SVC(gamma='auto', probability=True)
        clf.fit(self.training_x, self.training_y)

        y = self.testing_y
        pred = clf.predict_proba(self.testing_x)
        pred = self.__get_probs_positive_class(pred)

        return metrics.roc_auc_score(np.array(y, dtype=int), pred)



    def __get_probs_positive_class(self, pred):
        positive_probs = []

        for prediction in pred:
            positive_probs.append(prediction[1])
        return positive_probs


    def get_stability(self, threshold):
        return ki.get_kuncheva_index(self.rankings, threshold=threshold)




    def evaluate_final_rankings(self):

        final_rankings = self.__get_final_rankings()
        self.rankings = self.__get_gene_lists(final_rankings)

        print("Computing stabilities...")
        stabilities = self.__compute_stabilities()

        with open(self.dm.results_path+"fold_sampling.pkl", 'rb') as file:
                folds_sampling = pickle.load(file)
        print("Computing AUCs...")
        aucs = self.__compute_aucs(folds_sampling)
        
        self.aucs = aucs
        self.stabilities = stabilities

        return aucs, stabilities
    

    def __get_final_rankings(self):

        final_rankings = []
        for fold_iteration in range(self.dm.num_folds):
            ranking_path = self.dm.results_path + "fold_" + str(fold_iteration+1) + "/"
            file = ranking_path + AGGREGATED_RANKING_FILE_NAME
            ranking = self.dm.load_RDS(file)
            ranking = self.dm.r_to_pandas(ranking)
            final_rankings.append(ranking)

        return final_rankings


    def __compute_stabilities(self):
        
        th_stabilities = []
        for th in self.thresholds:
            th_stabilities.append(self.get_stability(th))
        return th_stabilities

    
    def __compute_aucs(self, folds_sampling):
        
        fold_aucs = []
        for i, (training, testing) in enumerate(folds_sampling):

            th_aucs = []
            for th in self.thresholds:
                genes = self.rankings[i][0:th]
                self.__set_data_axes(training, testing, genes)
                th_aucs.append(self.get_auc())

            fold_aucs.append(th_aucs)
        return fold_aucs


    def __set_data_axes(self, training, testing, genes):

        training_df = self.dm.pd_df.loc[training]
        testing_df = self.dm.pd_df.loc[testing]

        self.training_x = self.__get_x(training_df, genes)
        self.training_y = self.__get_y(training_df)
        self.testing_x = self.__get_x(testing_df, genes)
        self.testing_y = self.__get_y(testing_df)
        return


    def evaluate_intermediate_hyb_rankings(self):
        
        level1_rankings, level2_rankings = self.__get_intermediate_rankings()
        

        return

    
    def __get_intermediate_rankings(self):

        level2_rankings = []  # each item is a list representing each fold iteration
                              # these lists contain the rankings generated with each bootstrap

        level1_rankings = []  # each item is a list representing each fold iteration
                              # each item inside this list is also a list representing each bootstrap
                              # each item of the bootstrap list is single feature selection generated ranking
        # so it looks like:
        # level1_rankings = [
        #              fold1 = [
        #                       bootstrap1 = [r1, r2, r3, r4, r5],
        #                       bootstrap2 = [r1, r2, r3, r4, r5],
        #                       bootstrap3 = [r1, r2, r3, r4, r5],
        #                       ...
        #               ], 
        #               fold2 = [
        #                       bootstrap1 = [r1, r2, r3, r4, r5],
        #                       bootstrap2 = [r1, r2, r3, r4, r5],
        #                       bootstrap3 = [r1, r2, r3, r4, r5],
        #                       ...
        #               ],
        #               ...         
        # ]


        for fold_iteration in range(1, self.dm.num_folds+1):
            
            bs_rankings = []
            bs_single_rankings = []
            for bootstrap in range(1, self.dm.num_bootstraps+1):
                
                ranking_path = self.__build_ranking_path_string(fold_iteration, bootstrap)
                
                bs_rankings.append(self.__load_agg_rankings(ranking_path))
                

                single_ranking_file_names = self.__get_single_fs_ranking_file_names(
                                                        ranking_path) 
                single_fs_rankings = self.__load_single_fs_rankings(
                                                single_ranking_file_names)
                bs_single_rankings.append(single_fs_rankings)
                

            level1_rankings.append(bs_single_rankings)
            level2_rankings.append(bs_rankings)

        return level1_rankings, level2_rankings


    def __build_ranking_path_string(self, fold_iteration, bootstrap):
        return self.dm.results_path + "fold_" + str(fold_iteration) + "/" + \
                    "bootstrap_" + str(bootstrap) + "/"


    def __load_agg_rankings(self, ranking_path):
        file = ranking_path + AGGREGATED_RANKING_FILE_NAME
        ranking = self.dm.load_RDS(file)
        ranking = self.dm.r_to_pandas(ranking)
        return ranking

    
    def __load_single_fs_rankings(self, paths):
        rankings = []
        for file in paths:
            ranking = self.dm.load_RDS(file)
            ranking = self.dm.r_to_pandas(ranking)
            rankings.append(ranking)
        return rankings


    def __get_single_fs_ranking_file_names(self, path):
        file_names_style = path + "*.rds"
        return [f for f in glob.glob(f"{file_names_style}") 
                    if AGGREGATED_RANKING_FILE_NAME not in f]