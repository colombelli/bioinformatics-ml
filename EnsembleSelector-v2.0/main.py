from DataManager import DataManager
from EFS import EFS
from Heterogeneous import Heterogeneous
from Homogeneous import Homogeneous
from Evaluator import Evaluator
import rpy2.robjects.packages as rpackages


#dataset_path = "/home/colombelli/Documents/THCA/iqrSelectedGenes.rds"
#results_path = "/home/colombelli/Documents/bioinformatics-ml/EnsembleSelector-v2.0/resultsTHCA/"
dataset_path = "/home/colombelli/Documents/datasets/thyroid_log2.rds"
results_path = "/home/colombelli/Documents/geoDE_homo/"


rpackages.importr('CORElearn')
rpackages.importr('FSelectorRcpp')
rpackages.importr('FSelector')


seed = 42
#num_bootstraps = 2
#num_bootstraps = 0
num_bootstraps = 50
num_folds = 3


fs_methods = [
    ("gain-ratio", "r", "gr"),
    ("geoDE", "python", "gd"),
    ("symmetrical-uncertainty", "r", "su")#,
    #("relief", "r", "rf"),
    #("oneR", "r", "or"),
    #("svm_rfe", "python", "svmrfe")
]

aggregator = "mean"

dm = DataManager(results_path, dataset_path, num_bootstraps, num_folds, seed)

#ensemble = Heterogeneous(dm, fs_methods, aggregator)
homo_method=("geoDE", "python", "gd")
ensemble = Homogeneous(dm, homo_method, aggregator)
ensemble.select_features()

print("\n\nStarting evaluation process...")
ev = Evaluator(dm, [0.0001, 0.1, 0.5, 1, 2, 5])
aucs, stabilities = ev.evaluate_final_rankings()

print("\n\nAUCs:")
print(aucs)

print("\n\nStabilities:")
print(stabilities)
