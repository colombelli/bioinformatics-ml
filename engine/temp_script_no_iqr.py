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
]

aggregator = "mean"

ths = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
#ths = [0.01, 0.02, 0.03, 0.04, 0.06, 0.08, 0.1, 0.2, 0.4]
#ths = [0.2, 0.4, 1, 1.5, 2, 5, 10]
seed = 42

str_methods = ["ReliefF", "GeoDE", "Gain Ratio", "Symmetrical Uncertainty", "OneR"]
str_aggregators = ["Mean Aggregation", "Mean Aggregation"]



def perform_selection_hyb(dataset_path, results_path):
    
    dm = DataManager(results_path, dataset_path, num_bootstraps, num_folds, seed)
    dm.encode_main_dm_df()
    dm.create_results_dir()
    dm.init_data_folding_process()
    ev = Evaluator(dm, ths, True)
    im = InformationManager(dm, ev, str_methods, str_aggregators)
    ensemble = Hybrid(dm, fs_methods, aggregator, aggregator)

    st = time()
    ensemble.select_features()
    compute_print_time(st)

    print("\n\nDecoding dataframe...")
    dm.decode_main_dm_df()
    print("\nStarting evaluation process...")
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



dataset_path = "/home/colombelli/Desktop/processedBRCA.rds"
results_path = "/home/colombelli/Desktop/BRCA_no_IQR/"
perform_selection_hyb(dataset_path, results_path)
