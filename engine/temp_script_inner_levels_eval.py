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
level1_evaluation, level2_evaluation = ev.evaluate_intermediate_hyb_rankings()


im.create_intermediate_csv_tables(level1_evaluation, level2_evaluation)
