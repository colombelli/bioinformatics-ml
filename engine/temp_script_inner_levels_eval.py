from DataManager import DataManager
from Evaluator import Evaluator
from InformationManager import InformationManager
import rpy2.robjects.packages as rpackages
from time import time


num_bootstraps = 50
num_folds = 5

aggregator = "mean"

ths = [1, 5, 10, 15, 25, 50, 75, 100, 150, 200]
seed = 42

str_methods = ["ReliefF", "GeoDE", "Gain Ratio", "Symmetrical Uncertainty", "OneR"]
str_aggregators = ["Mean Aggregation", "Mean Aggregation"]


experiment_path = "/home/colombelli/Documents/ExperimentsNewTHs/THCA/test/"
dataset_path = "/home/colombelli/Documents/datasets/research/thca.rds"



dm = DataManager(experiment_path, dataset_path, num_bootstraps, num_folds, seed)

ev = Evaluator(dm, ths, False)
im = InformationManager(dm, ev, str_methods, str_aggregators)

print("\n\nStarting evaluation process...")
aucs, stabilities = ev.evaluate_intermediate_hyb_rankings()


print("\n\nAUCs:")
print(aucs)

print("\n\nStabilities:")
print(stabilities)

im.create_level2_csv_tables(aucs, stabilities)

"""
    print("\n\nCreating csv files...")
    im.create_csv_tables()

    print("\nExperiment", e,"reevaluated!\n\n")
"""