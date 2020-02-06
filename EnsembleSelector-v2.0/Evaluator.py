import pandas as pd
import pickle
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import metrics
import numpy as np
import kuncheva_index as ki
from DataManager import DataManager
from Constants import *

class Evaluator:

    def __init__(self, data_manager:DataManager, thresholds):

        self.dm = data_manager
        self.thresholds = self.__get_int_thresholds(thresholds)
        
        self.rankings = None
        self.training_x = None
        self.training_y = None
        self.testing_x = None
        self.testing_y = None


    def __get_int_thresholds(self, thresholds):

        dataset_len = len(self.dm.pd_df.columns)

        int_thresholds = []
        for th in thresholds:
            int_thresholds.append(
                    int(dataset_len * th/100)
                )
        print("\nNumber of genes to select given the threshold percentages:")
        print(int_thresholds, "\n\n")
        return int_thresholds


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
        
        # DEBUGGING CODE!!
        print("TRAINING:")
        tr = self.training_x.index.values
        print(tr)
        print("\nTESTING:")
        ts = self.testing_x.index.values
        print(ts)
        print("\nCOMMON ELEMENT?")
        print(not set(tr).isdisjoint(ts))
        print("\ntesting with two lists one common element to see if it works:")
        l1 = [
            'TCGA.BH.A0B3.11B.21R.A089.07', 'TCGA.C8.A1HO.01A.11R.A13Q.07',
            'TCGA.B6.A402.01A.11R.A239.07', 'TCGA.BH.A0BT.01A.11R.A12P.07',
            'TCGA.A7.A13D.01A.13R.A277.07', 'TCGA.AR.A0TU.01A.31R.A109.07'
        ]
        l2 = [
            'TCGA.BH.A0E1.11A.13R.A089.07', 'TCGA.AN.A041.01A.11R.A034.07',
            'TCGA.BH.A0B8.01A.21R.A056.07', 'TCGA.AO.A03V.01A.11R.A115.07',
            'TCGA.BH.A0AZ.11A.22R.A12P.07', 'TCGA.BH.A0C0.11A.21R.A089.07',
            'TCGA.A7.A13D.01A.13R.A277.07'
        ]
        print(not set(l1).isdisjoint(l2))
        input()

        print("\ny tr:")
        print(self.training_y)
        print("\ny tst:")
        print(self.testing_y)
        input()

        accuracyy = clf.score(self.testing_x, self.testing_y, sample_weight=None)
        print("\n\nACCURACY:", accuracyy)
        input()
        # END OF DEBUGGING CODE!!


        y = self.testing_y
        pred = clf.predict_proba(self.testing_x)
        pred = self.__get_probs_positive_class(pred)
        
        fpr, tpr, _ = metrics.roc_curve(np.array(y, dtype=int)+1, pred, pos_label=2)
        return metrics.auc(fpr, tpr)


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