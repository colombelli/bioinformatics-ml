from DataManager import DataManager
from Hybrid import Hybrid
from Heterogeneous import Heterogeneous
from Homogeneous import Homogeneous
from SingleFS import SingleFS
from Evaluator import Evaluator
from InformationManager import InformationManager
import rpy2.robjects.packages as rpackages


#dataset_path = "/home/colombelli/Documents/THCA/iqrSelectedGenes.rds"
#results_path = "/home/colombelli/Documents/bioinformatics-ml/EnsembleSelector-v2.0/resultsTHCA/"
#dataset_path = "/home/colombelli/Documents/datasets/thyroid_log2.rds"
#results_path = "/home/colombelli/Documents/single2/"
dataset_path = "/home/colombelli/Documents/datasets/brca.rds"
results_path = "/home/colombelli/Documents/BRCA_Hybrid_mean_mean/"


rpackages.importr('CORElearn')
rpackages.importr('FSelectorRcpp')
rpackages.importr('FSelector')


seed = 42
#num_bootstraps = 2
num_bootstraps = 0
num_bootstraps = 10
num_folds = 5


fs_methods = [
    #("reliefF", "python", "rf"),
    ("geoDE", "python", "gd"),
    ("gain-ratio", "r", "gr")#,
    #("symmetrical-uncertainty", "r", "su"),
    #("oneR", "r", "or")
]

aggregator = "mean"

dm = DataManager(results_path, dataset_path, num_bootstraps, num_folds, seed)

ensemble = Hybrid(dm, fs_methods, aggregator, aggregator)
#ensemble = Heterogeneous(dm, fs_methods, aggregator)
#homo_method=("geoDE", "python", "gd")
#ensemble = Homogeneous(dm, homo_method, aggregator)

str_methods = ["GeoDE", "Gain Ratio"]
str_aggregators = ["Mean Aggregation", "Mean Aggregation"]
im = InformationManager(dm, str_methods)


from time import time
st = time()
ensemble.select_features()
ed = time()

try:
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)

    print("\n\nTIME TAKEN:") 
    print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
except:
    pass
"""
#method = ("gain-ratio", "r", "gr")#("geoDE", "python", "gd")
#single_fs = SingleFS(dm, method)
#single_fs.select_features()

print("\n\nStarting evaluation process...")
#ths = [0.1, 0.2, 0.3, 0.5, 0.8, 1, 1.5, 2, 3, 5]
ths = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07]
ev = Evaluator(dm, ths)
aucs, stabilities = ev.evaluate_final_rankings()

print("\n\nAUCs:")
print(aucs)

print("\n\nStabilities:")
print(stabilities)
"""