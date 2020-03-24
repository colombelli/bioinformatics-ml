from DataManager import DataManager
from Evaluator import Evaluator
from InformationManager import InformationManager
import rpy2.robjects.packages as rpackages
from time import time


num_bootstraps = 50
num_folds = 5

aggregator = "mean"

ths = [0.01, 0.02, 0.03, 0.04, 0.06, 0.08, 0.1, 0.2, 0.4]
seed = 42

str_methods = ["ReliefF", "GeoDE", "Gain Ratio", "Symmetrical Uncertainty", "OneR"]
str_aggregators = ["Mean Aggregation", "Mean Aggregation"]


exp = ["Het_mean", "Hom_mean_geode", "Hom_mean_gr", "Hom_mean_oner", "Hom_mean_relieff",
        "Hom_mean_su", "sin_geode", "sin_gr", "sin_oner", "sin_relieff", "sin_su",
        "Hyb_mean_mean"]

exp_del_bs_folders = ["Het_mean", "sin_geode", "sin_gr", "sin_oner", "sin_relieff", "sin_su"]

experiment_path = "/home/colombelli/Documents/ExperimentsReeval/BRCA/"
dataset_path = "/home/colombelli/Documents/datasets/research/brca.rds"

import os

def del_bs_folders(dm):
    
    for fold in range(dm.num_folds):
        path = dm.results_path + "fold_" + str(fold+1) + "/bootstrap_" 
        
        for bs in range(dm.num_bootstraps):
            os.rmdir(path+str(bs+1))


for e in exp:

    exp_path = experiment_path + e + "/"
    dm = DataManager(exp_path, dataset_path, num_bootstraps, num_folds, seed)
    if e in exp_del_bs_folders:
        del_bs_folders(dm)
    ev = Evaluator(dm, ths)
    im = InformationManager(dm, ev, str_methods, str_aggregators)

    print("\n\nStarting evaluation process...")
    aucs, stabilities = ev.evaluate_final_rankings()

    print("\n\nAUCs:")
    print(aucs)

    print("\n\nStabilities:")
    print(stabilities)

    print("\n\nCreating csv files...")
    im.create_csv_tables()

    print("\nExperiment", e,"reevaluated!\n\n")