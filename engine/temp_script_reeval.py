from engine.DataManager import DataManager
from engine.Evaluator import Evaluator
from engine.InformationManager import InformationManager
import rpy2.robjects.packages as rpackages
from time import time
import pickle


num_bootstraps = 50
num_folds = 4

aggregator = "mean"

ths = [1, 5, 10, 15, 25, 50, 75, 100, 150, 200]
seed = 42

str_methods = ["ReliefF", "GeoDE", "Gain Ratio", "Symmetrical Uncertainty", "Wx"]
str_aggregators = ["Mean Aggregation", "Mean Aggregation"]

'''
exp = ["Het_mean", "Hom_mean_geode", "Hom_mean_gr", "Hom_mean_oner", "Hom_mean_relieff",
        "Hom_mean_su", "sin_geode", "sin_gr", "sin_oner", "sin_relieff", "sin_su",
        "Hyb_mean_mean"]
'''
exp=["Hyb_borda_borda"]
exp_del_bs_folders = ["Het_mean", "sin_geode", "sin_gr", "sin_oner", "sin_relieff", "sin_su"]

experiment_path = "/home/colombelli/Documents/Experiments08_jul/BRCA/rna-seq/"
dataset_path = "/home/colombelli/Documents/datasets/assembler/brca_rna_symb.csv" 

import os

def del_bs_folders(dm):
    
    for fold in range(dm.num_folds):
        path = dm.results_path + "fold_" + str(fold+1) + "/bootstrap_" 
        
        for bs in range(dm.num_bootstraps):
            os.rmdir(path+str(bs+1))


def run():
    for e in exp:

        exp_path = experiment_path + e + "/"
        dm = DataManager(exp_path, dataset_path, num_bootstraps, num_folds, seed)
        
        print("Loading fold sampling...")
        with open(exp_path+"fold_sampling.pkl", "rb") as samp:
            fsampling = pickle.load(samp)
        dm.folds = fsampling

        #if e in exp_del_bs_folders:
        #    del_bs_folders(dm)
        ev = Evaluator(dm, ths, False)
        im = InformationManager(dm, ev, str_methods, str_aggregators)

        print("\n\nStarting evaluation process...")
        ev.evaluate_final_rankings()

        print("\n\nCreating csv files...")
        im.create_csv_tables()

        print("\nExperiment", e,"reevaluated!\n\n")