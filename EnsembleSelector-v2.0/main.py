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

dataset_path = "/home/colombelli/Documents/datasets/brca.rds"
results_path = "/home/colombelli/Documents/BRCA_Hybrid_mean_mean/"


rpackages.importr('CORElearn')
rpackages.importr('FSelectorRcpp')
rpackages.importr('FSelector')


seed = 42
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
ths = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07]
ev = Evaluator(dm, ths)

#ensemble = Hybrid(dm, fs_methods, aggregator, aggregator)
#ensemble = Heterogeneous(dm, fs_methods, aggregator)
#homo_method=("geoDE", "python", "gd")
#ensemble = Homogeneous(dm, homo_method, aggregator)
#method = ("geoDE", "python", "gd")
#single_fs = SingleFS(dm, method)


str_methods = ["GeoDE", "Gain Ratio"]
str_aggregators = ["Mean Aggregation", "Mean Aggregation"]
im = InformationManager(dm, ev, str_methods, str_aggregators)

"""
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

print("\n\nStarting evaluation process...")
aucs, stabilities = ev.evaluate_final_rankings()

print("\n\nAUCs:")
print(aucs)

print("\n\nStabilities:")
print(stabilities)

print("\n\nCreating csv files...")
im.create_csv_tables()

print("\nDone!")