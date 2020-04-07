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
        
        self.classifier = None

        self.roc_aucs = None
        self.pr_aucs = None
        self.accuracies = None
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


    def __reset_classifier(self):
        self.classifier = SVC(gamma='auto', probability=True)
        return


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



    def get_prediction_performance(self):
        
        self.__reset_classifier()
        self.classifier.fit(self.training_x, self.training_y)
        
        accuracy = self.classifier.score(self.testing_x, self.testing_y)

        pred = self.classifier.predict_proba(self.testing_x)
        pred = self.__get_probs_positive_class(pred)

        roc_auc = metrics.roc_auc_score(np.array(self.testing_y, dtype=int), pred)

        precision, recall, _ = metrics.precision_recall_curve(self.testing_y, pred)
        pr_auc = metrics.auc(recall, precision)
        
        return accuracy, roc_auc, pr_auc

        
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
        print("Computing prediction performances...")
        prediction_performances = self.__compute_prediction_performances(folds_sampling)


        self.stabilities = stabilities
        self.accuracies = prediction_performances[ACCURACY_METRIC]
        self.roc_aucs = prediction_performances[ROC_AUC_METRIC]
        self.pr_aucs = prediction_performances[PRECISION_RECALL_AUC_METRIC]
        
        return self.stabilities, self.accuracies, self.roc_aucs, self.pr_aucs
    

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

    
    def __compute_prediction_performances(self, folds_sampling):
        
        prediction_performances = {
            ACCURACY_METRIC: [],
            ROC_AUC_METRIC: [],
            PRECISION_RECALL_AUC_METRIC: []
        }

        for i, (training, testing) in enumerate(folds_sampling):

            th_accuracies = []
            th_roc_aucs = []
            th_pr_aucs = []
            
            for th in self.thresholds:
                genes = self.rankings[i][0:th]
                self.__set_data_axes(training, testing, genes)
                acc, roc, pr = self.get_prediction_performance()
                th_accuracies.append(acc)
                th_roc_aucs.append(roc)
                th_pr_aucs.append(pr)

            prediction_performances[ACCURACY_METRIC].append(th_accuracies)
            prediction_performances[ROC_AUC_METRIC].append(th_roc_aucs)
            prediction_performances[PRECISION_RECALL_AUC_METRIC].append(th_pr_aucs)
        
        return prediction_performances



    def __set_data_axes(self, training, testing, genes):

        training_df = self.dm.pd_df.loc[training]
        testing_df = self.dm.pd_df.loc[testing]

        self.training_x = self.__get_x(training_df, genes)
        self.training_y = self.__get_y(training_df)
        self.testing_x = self.__get_x(testing_df, genes)
        self.testing_y = self.__get_y(testing_df)
        return


    #TO-DO: FIX THIS METHODS
    def evaluate_intermediate_hyb_rankings(self):
        
        level1_rankings, level2_rankings = self.__get_intermediate_rankings()
        
        print("\nEvaluating level 1 rankings...")
        level1_evaluation = self.__evaluate_level1_rankings(level1_rankings)
        print("\n\nEvaluating level 2 rankings...")
        level2_evaluation = self.__evaluate_intermediate_rankings(level2_rankings)        
        return level1_evaluation, level2_evaluation
        

    def __evaluate_level1_rankings(self, level1_rankings):
        
        level1_evaluation = {}  # a dict where each key is a single fs method
                                # and the value is a intermediate ranking like
                                # evaluation

        for fs_method in level1_rankings:
            print("\nEvaluating", fs_method, "FS method")
            level1_evaluation[fs_method] = self.__evaluate_intermediate_rankings(
                                                        level1_rankings[fs_method])
        return level1_evaluation


    def __evaluate_intermediate_rankings(self, final_rankings):
        
        with open(self.dm.results_path+"fold_sampling.pkl", 'rb') as file:
            folds_sampling = pickle.load(file)

        aucs = []
        stabilities = []
        for i, fold_rankings in enumerate(final_rankings):
            self.rankings = self.__get_gene_lists(fold_rankings)

            print("Computing stabilities...")
            stabilities.append(self.__compute_stabilities())

            
            print("Computing AUCs...")
            aucs = aucs + self.__compute_intermediate_aucs(folds_sampling[i])
                
        return aucs, stabilities

    
    def __get_intermediate_rankings(self):

        level2_rankings = []  # each item is a list representing each fold iteration
                              # these lists contain the rankings generated with each bootstrap

        level1_rankings = {}  # each key is a fs method
                              # each value is a level2_rankings kind-of-structure
                              
        # so it looks like:
        # level1_rankings = {
        #              fs1: [
        #                       fold1 = [r1, r2, r3, ...],
        #                       fold2 = [r1, r2, r3, ...],
        #                       fold3 = [r1, r2, r3, ...],
        #                       ...
        #               ], 
        #               fs2: [
        #                       fold1 = [r1, r2, r3, ...],
        #                       fold2 = [r1, r2, r3, ...],
        #                       fold3 = [r1, r2, r3, ...],
        #                       ...
        #               ],
        #               ...         
        # }

        self.__init_level1_rankings_dict(level1_rankings)
        print("Loading level 1 rankings...")
        self.__load_level1_rankings(level1_rankings)
        print("Loading level 2 rankings...")
        self.__load_level2_rankings(level2_rankings)

        return level1_rankings, level2_rankings
    

    def __init_level1_rankings_dict(self, level1_rankings):

        fs_names = self.__get_single_fs_names()
        for fs_name in fs_names:
            level1_rankings[fs_name] = []
        return


    def __get_single_fs_names(self):
        
        ranking_path = self.__build_ranking_path_string(1, 1)
        single_ranking_file_names = self.__get_single_fs_ranking_file_names(
                                                        ranking_path)
        single_fs_names = []
        for path in single_ranking_file_names:
            single_fs_names.append(
                self.__get_fs_method_name_by_its_path(path)
            )

        return single_fs_names


    def __build_ranking_path_string(self, fold_iteration, bootstrap):
        return self.dm.results_path + "fold_" + str(fold_iteration) + "/" + \
                    "bootstrap_" + str(bootstrap) + "/"


    def __get_fs_method_name_by_its_path(self, path):
        return path.split("/")[-1].split(".")[0]


    def __get_single_fs_ranking_file_names(self, path):
        file_names_style = path + "*.rds"
        return [f for f in glob.glob(f"{file_names_style}") 
                    if AGGREGATED_RANKING_FILE_NAME not in f]
    

    def __load_level1_rankings(self, level1_rankings):
        
        for fs_method in level1_rankings:
            for fold_iteration in range(1, self.dm.num_folds+1):
                
                bs_rankings = []
                for bootstrap in range(1, self.dm.num_bootstraps+1):
                    
                    ranking_path = self.__build_ranking_path_string(fold_iteration, bootstrap)
                    bs_rankings.append(self.__load_single_fs_ranking(ranking_path, fs_method))

                level1_rankings[fs_method].append(bs_rankings)
        return

    
    def __load_level2_rankings(self, level2_rankings):

        for fold_iteration in range(1, self.dm.num_folds+1):
            
            agg_rankings = []
            for bootstrap in range(1, self.dm.num_bootstraps+1):
                
                ranking_path = self.__build_ranking_path_string(fold_iteration, bootstrap)
                agg_rankings.append(self.__load_agg_rankings(ranking_path))

            level2_rankings.append(agg_rankings)
        return


    def __load_agg_rankings(self, ranking_path):
        file = ranking_path + AGGREGATED_RANKING_FILE_NAME
        ranking = self.dm.load_RDS(file)
        ranking = self.dm.r_to_pandas(ranking)
        return ranking

    
    def __load_single_fs_ranking(self, ranking_path, fs_method):
        file = ranking_path + fs_method + ".rds"
        ranking = self.dm.load_RDS(file)
        ranking = self.dm.r_to_pandas(ranking)
        return ranking


    
    #TO-DO: FIX THIS METHOD
    def __compute_intermediate_aucs(self, fold_sampling, curve=ROC_CURVE_SELECTION):
        
        training, testing = fold_sampling

        bs_aucs = []
        for ranking in self.rankings:

            th_aucs = []
            for th in self.thresholds:
                genes = ranking[0:th]
                self.__set_data_axes(training, testing, genes)
                th_aucs.append(self.get_auc(curve))

            bs_aucs.append(th_aucs)
        return bs_aucs