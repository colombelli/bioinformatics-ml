from DataManager import DataManager
from EFS import EFS
import rpy2.robjects.packages as rpackages


dataset_path = "/home/colombelli/Documents/datasets/iqrSelectedGenes.rds"
results_path = "/home/colombelli/Documents/bioinformatics-ml/EnsembleSelector-v2.0/results/"
#dataset_path = "/home/colombelli/Documents/datasets/merged80Samples.rds"

rpackages.importr('CORElearn')
rpackages.importr('FSelectorRcpp')
rpackages.importr('FSelector')


seed = 43
num_bootstraps = 10
num_folds = 3

fs_methods = [
    ("gain-ratio", "r", "gr"),
    ("symmetrical-uncertainty", "r", "su")
]

aggregator = "mean"

dm = DataManager(results_path, dataset_path, num_bootstraps, num_folds, seed)
ensemble = EFS(dm, fs_methods, aggregator, aggregator)

ensemble.select_features()