from DataManager import DataManager
from EFS import EFS
from Evaluator import Evaluator
import rpy2.robjects.packages as rpackages


dataset_path = "/home/colombelli/Documents/datasets/iqrSelectedGenes.rds"
results_path = "/home/colombelli/Documents/bioinformatics-ml/EnsembleSelector-v2.0/results/"
#dataset_path = "/home/colombelli/Documents/datasets/merged80Samples.rds"

rpackages.importr('CORElearn')
rpackages.importr('FSelectorRcpp')
rpackages.importr('FSelector')


seed = 43
num_bootstraps = 5
num_folds = 3

fs_methods = [
    ("gain-ratio", "r", "gr"),
    ("symmetrical-uncertainty", "r", "su")
]

aggregator = "mean"

dm = DataManager(results_path, dataset_path, num_bootstraps, num_folds, seed)

ensemble = EFS(dm, fs_methods, aggregator, aggregator)
ensemble.select_features()

ev = Evaluator(dm, [0.1, 0.5, 1, 2, 5])
aucs, stabilities = ev.evaluate_final_rankings()

print("\n\nAUCs:")
print(aucs)

print("\n\nStabilities:")
print(stabilities)