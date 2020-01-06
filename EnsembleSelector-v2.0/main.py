from Selector import RSelector
from Selector import PySelector
from DataManager import DataManager
from Aggregator import Aggregator
import rpy2.robjects.packages as rpackages


dataset_path = "/home/colombelli/Documents/datasets/iqrSelectedGenes.rds"
results_path = "/home/colombelli/Documents/bioinformatics-ml/EnsembleSelector-v2.0/results/"
#dataset_path = "/home/colombelli/Documents/datasets/merged80Samples.rds"

rpackages.importr('CORElearn')
rpackages.importr('FSelectorRcpp')
#rpackages.importr('FSelector')


seed = 43
num_bootstraps = 30
num_folds = 10


chosenFS = {
            "relief": False,
            "gainRatio": True,
            "symmetricalUncertainty": True,
            "oneR": False,
            "svmRFE": False
        }         
"""
dm = DataManager(results_path, dataset_path, num_bootstraps, num_folds, seed)
b0 = dm.get_bootstraps()
dm.save_bootstraps(b0)
dm.current_fold_iteration = 1
b1 = dm.get_bootstraps()
dm.current_fold_iteration = 2
b2 = dm.get_bootstraps()

print(b0[0])
print(b0[1])
print('#############')
print(b1[0])
print(b1[1])
print('#############')
print(b2[0])
print(b2[1])
print('#############')
"""

import pickle
file = results_path + "seed.pkl" 
with open(file, 'rb') as f:
    seed = pickle.load(f)
print(seed)
"""
bootstrap = dm.getBootStrap(1)
df = bootstrap[0]["training"]
#selector = PySelector("svm", "svm_rfe")
selector = RSelector("gr", "gain-ratio-cpp", "gainRatio")
ranking1 = selector.select(df, resultsPath)

selector2 = RSelector("su", "symmetrical-uncertainty", "symUnc")
ranking2 = selector2.select(df, resultsPath)
"""