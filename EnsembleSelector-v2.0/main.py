from DataManager import DataManager
from Hybrid import Hybrid
from Heterogeneous import Heterogeneous
from Homogeneous import Homogeneous
from SingleFS import SingleFS
from Evaluator import Evaluator
from InformationManager import InformationManager
import rpy2.robjects.packages as rpackages
from time import time



def compute_print_time(st):
    
    print("\n\nTIME TAKEN:")
    end = time()
    try:
        hours, rem = divmod(end-st, 3600)
        minutes, seconds = divmod(rem, 60)
 
        print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
    except:
        print(end-st)
    return




#dataset_path = "/home/colombelli/Documents/datasets/thyroid_log2.rds"

#ensemble = Hybrid(dm, fs_methods, aggregator, aggregator)
#ensemble = Heterogeneous(dm, fs_methods, aggregator)
#homo_method=("geoDE", "python", "gd")
#ensemble = Homogeneous(dm, homo_method, aggregator)
#method = ("geoDE", "python", "gd")
#single_fs = SingleFS(dm, method)


rpackages.importr('CORElearn')
rpackages.importr('FSelectorRcpp')
rpackages.importr('FSelector')


num_bootstraps = 50
num_folds = 5

fs_methods = [
    ("reliefF", "python", "rf"),
    ("geoDE", "python", "gd"),
    ("gain-ratio", "r", "gr"),
    ("symmetrical-uncertainty", "r", "su"),
    ("oneR", "r", "or")
]

aggregator = "mean"

ths = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
seed = 42

str_methods = ["ReliefF", "GeoDE", "Gain Ratio", "Symmetrical Uncertainty", "OneR"]
str_aggregators = ["Mean Aggregation", "Mean Aggregation"]



def perform_selection_hyb(dataset_path, results_path):
    
    dm = DataManager(results_path, dataset_path, num_bootstraps, num_folds, seed)
    ev = Evaluator(dm, ths)
    im = InformationManager(dm, ev, str_methods, str_aggregators)
    ensemble = Hybrid(dm, fs_methods, aggregator, aggregator)

    st = time()
    ensemble.select_features()
    compute_print_time(st)

    print("\n\nStarting evaluation process...")
    aucs, stabilities = ev.evaluate_final_rankings()

    print("\n\nAUCs:")
    print(aucs)

    print("\n\nStabilities:")
    print(stabilities)

    print("\n\nCreating csv files...")
    im.create_csv_tables()

    print("\nDone!\n\n")
    print("#################################################################\n")
    return


dataset_path = "/home/colombelli/Documents/datasets/research/kirp.rds"
results_path = "/home/colombelli/Documents/Experiments2/KIRP/Hyb_mean_mean/"
perform_selection_hyb(dataset_path, results_path)


dataset_path = "/home/colombelli/Documents/datasets/research/ucec.rds"
results_path = "/home/colombelli/Documents/Experiments2/UCEC/Hyb_mean_mean/"
perform_selection_hyb(dataset_path, results_path)

dataset_path = "/home/colombelli/Documents/datasets/research/thca.rds"
results_path = "/home/colombelli/Documents/Experiments2/THCA/Hyb_mean_mean/"
perform_selection_hyb(dataset_path, results_path)

dataset_path = "/home/colombelli/Documents/datasets/research/brca.rds"
results_path = "/home/colombelli/Documents/Experiments2/BRCA/Hyb_mean_mean/"
perform_selection_hyb(dataset_path, results_path)
