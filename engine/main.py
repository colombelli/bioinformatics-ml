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

#ths = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
#ths = [0.01, 0.02, 0.03, 0.04, 0.06, 0.08, 0.1, 0.2, 0.4]
#ths = [0.2, 0.4, 1, 1.5, 2, 5, 10]
ths = [1, 5, 10, 15, 25, 50, 75, 100, 150, 200]
seed = 42

str_methods = ["ReliefF", "GeoDE", "Gain Ratio", "Symmetrical Uncertainty", "OneR"]
str_aggregators = ["Mean Aggregation", "Mean Aggregation"]



def perform_selection_hyb(dataset_path, results_path):
    
    dm = DataManager(results_path, dataset_path, num_bootstraps, num_folds, seed)
    dm.encode_main_dm_df()
    dm.create_results_dir()
    dm.init_data_folding_process()

    ev = Evaluator(dm, ths, False)
    im = InformationManager(dm, ev, str_methods, str_aggregators)
    ensemble = Hybrid(dm, fs_methods, aggregator, aggregator)

    st = time()
    ensemble.select_features()
    compute_print_time(st)

    print("\n\nDecoding dataframe...")
    dm.decode_main_dm_df()
    print("\nStarting evaluation process...")
    ev.evaluate_final_rankings()

    print("\n\nCreating csv files...")
    im.create_csv_tables()

    print("\nEvaluating inner levels...")
    level1_evaluation, level2_evaluation = ev.evaluate_intermediate_hyb_rankings()

    print("\n\nCreating csv files...")
    im.create_intermediate_csv_tables(level1_evaluation, level2_evaluation)

    print("\nDone!\n\n")
    print("#################################################################\n")
    return



def perform_selection_het(dataset_path, results_path):

    num_bootstraps = 0

    dm = DataManager(results_path, dataset_path, num_bootstraps, num_folds, seed)
    dm.encode_main_dm_df()
    dm.create_results_dir()
    dm.init_data_folding_process()
    
    ev = Evaluator(dm, ths, False)
    im = InformationManager(dm, ev, str_methods, str_aggregators)
    ensemble = Heterogeneous(dm, fs_methods, aggregator)

    st = time()
    ensemble.select_features()
    compute_print_time(st)

    print("\n\nDecoding dataframe...")
    dm.decode_main_dm_df()
    print("\nStarting evaluation process...")
    ev.evaluate_final_rankings()

    print("\n\nCreating csv files...")
    im.create_csv_tables()

    print("\nDone!\n\n")
    print("#################################################################\n")
    return



def perform_selection_hom(dataset_path, results_path, fs_method):

    dm = DataManager(results_path, dataset_path, num_bootstraps, num_folds, seed)
    dm.encode_main_dm_df()
    dm.create_results_dir()
    dm.init_data_folding_process()

    ev = Evaluator(dm, ths, False)
    im = InformationManager(dm, ev, str_methods, str_aggregators)
    ensemble = Homogeneous(dm, fs_method, aggregator)

    st = time()
    ensemble.select_features() 
    compute_print_time(st)

    print("\n\nDecoding dataframe...")
    dm.decode_main_dm_df()
    print("\nStarting evaluation process...")
    ev.evaluate_final_rankings()

    print("\n\nCreating csv files...")
    im.create_csv_tables()

    print("\nDone!\n\n")
    print("#################################################################\n")
    return



def perform_selection_single(dataset_path, results_path, fs_method):

    num_bootstraps = 0

    dm = DataManager(results_path, dataset_path, num_bootstraps, num_folds, seed)
    dm.encode_main_dm_df()
    dm.create_results_dir()
    dm.init_data_folding_process()

    ev = Evaluator(dm, ths, False)
    im = InformationManager(dm, ev, str_methods, str_aggregators)
    feature_selector = SingleFS(dm, fs_method)

    st = time()
    feature_selector.select_features()
    compute_print_time(st)

    print("\n\nDecoding dataframe...")
    dm.decode_main_dm_df()
    print("\nStarting evaluation process...")
    ev.evaluate_final_rankings()

    print("\n\nCreating csv files...")
    im.create_csv_tables()

    print("\nDone!\n\n")
    print("#################################################################\n")
    return




########### HYBRID EXPERIMENTS ##############

dataset_path = "/home/colombelli/Documents/datasets/research/kirp.rds"
results_path = "/home/colombelli/Documents/Experiments09_abr/KIRP/Hyb_mean_mean/"
perform_selection_hyb(dataset_path, results_path)

dataset_path = "/home/colombelli/Documents/datasets/research/ucec.rds"
results_path = "/home/colombelli/Documents/Experiments09_abr/UCEC/Hyb_mean_mean/"
perform_selection_hyb(dataset_path, results_path)

dataset_path = "/home/colombelli/Documents/datasets/research/thca.rds"
results_path = "/home/colombelli/Documents/Experiments09_abr/THCA/Hyb_mean_mean/"
perform_selection_hyb(dataset_path, results_path)

dataset_path = "/home/colombelli/Documents/datasets/research/brca.rds"
results_path = "/home/colombelli/Documents/Experiments09_abr/BRCA/Hyb_mean_mean/"
perform_selection_hyb(dataset_path, results_path)

"""

########### HETEROGENOUS EXPERIMENTS ##############

dataset_path = "/home/colombelli/Documents/datasets/research/kirp.rds"
results_path = "/home/colombelli/Documents/Experiments09_abr/KIRP/Het_mean/"
perform_selection_het(dataset_path, results_path)

dataset_path = "/home/colombelli/Documents/datasets/research/ucec.rds"
results_path = "/home/colombelli/Documents/Experiments09_abr/UCEC/Het_mean/"
perform_selection_het(dataset_path, results_path)

dataset_path = "/home/colombelli/Documents/datasets/research/thca.rds"
results_path = "/home/colombelli/Documents/Experiments09_abr/THCA/Het_mean/"
perform_selection_het(dataset_path, results_path)

dataset_path = "/home/colombelli/Documents/datasets/research/brca.rds"
results_path = "/home/colombelli/Documents/Experiments09_abr/BRCA/Het_mean/"
perform_selection_het(dataset_path, results_path)




########### HOMOGENEOUS EXPERIMENTS ##############

method_relief = ("reliefF", "python", "rf")
method_geode = ("geoDE", "python", "gd")
method_gr = ("gain-ratio", "r", "gr")
method_su = ("symmetrical-uncertainty", "r", "su")
method_oner = ("oneR", "r", "or")

############ KIRP HOMOGENEOUS ############
dataset_path = "/home/colombelli/Documents/datasets/research/kirp.rds"

results_path = "/home/colombelli/Documents/Experiments09_abr/KIRP/Hom_mean_gr/"
perform_selection_hom(dataset_path, results_path, method_gr)
results_path = "/home/colombelli/Documents/Experiments09_abr/KIRP/Hom_mean_su/"
perform_selection_hom(dataset_path, results_path, method_su)
results_path = "/home/colombelli/Documents/Experiments09_abr/KIRP/Hom_mean_geode/"
perform_selection_hom(dataset_path, results_path, method_geode)
results_path = "/home/colombelli/Documents/Experiments09_abr/KIRP/Hom_mean_relieff/"
perform_selection_hom(dataset_path, results_path, method_relief)
results_path = "/home/colombelli/Documents/Experiments09_abr/KIRP/Hom_mean_oner/"
perform_selection_hom(dataset_path, results_path, method_oner)



############ UCEC HOMOGENEOUS ############
dataset_path = "/home/colombelli/Documents/datasets/research/ucec.rds"

results_path = "/home/colombelli/Documents/Experiments09_abr/UCEC/Hom_mean_gr/"
perform_selection_hom(dataset_path, results_path, method_gr)
results_path = "/home/colombelli/Documents/Experiments09_abr/UCEC/Hom_mean_su/"
perform_selection_hom(dataset_path, results_path, method_su)
results_path = "/home/colombelli/Documents/Experiments09_abr/UCEC/Hom_mean_geode/"
perform_selection_hom(dataset_path, results_path, method_geode)
results_path = "/home/colombelli/Documents/Experiments09_abr/UCEC/Hom_mean_relieff/"
perform_selection_hom(dataset_path, results_path, method_relief)
results_path = "/home/colombelli/Documents/Experiments09_abr/UCEC/Hom_mean_oner/"
perform_selection_hom(dataset_path, results_path, method_oner)



############ THCA HOMOGENEOUS ############
dataset_path = "/home/colombelli/Documents/datasets/research/thca.rds"

results_path = "/home/colombelli/Documents/Experiments09_abr/THCA/Hom_mean_gr/"
perform_selection_hom(dataset_path, results_path, method_gr)
results_path = "/home/colombelli/Documents/Experiments09_abr/THCA/Hom_mean_su/"
perform_selection_hom(dataset_path, results_path, method_su)
results_path = "/home/colombelli/Documents/Experiments09_abr/THCA/Hom_mean_geode/"
perform_selection_hom(dataset_path, results_path, method_geode)
results_path = "/home/colombelli/Documents/Experiments09_abr/THCA/Hom_mean_relieff/"
perform_selection_hom(dataset_path, results_path, method_relief)
results_path = "/home/colombelli/Documents/Experiments09_abr/THCA/Hom_mean_oner/"
perform_selection_hom(dataset_path, results_path, method_oner)



############ BRCA HOMOGENEOUS ############
dataset_path = "/home/colombelli/Documents/datasets/research/brca.rds"

results_path = "/home/colombelli/Documents/Experiments09_abr/BRCA/Hom_mean_gr/"
perform_selection_hom(dataset_path, results_path, method_gr)
results_path = "/home/colombelli/Documents/Experiments09_abr/BRCA/Hom_mean_su/"
perform_selection_hom(dataset_path, results_path, method_su)
results_path = "/home/colombelli/Documents/Experiments09_abr/BRCA/Hom_mean_geode/"
perform_selection_hom(dataset_path, results_path, method_geode)
results_path = "/home/colombelli/Documents/Experiments09_abr/BRCA/Hom_mean_relieff/"
perform_selection_hom(dataset_path, results_path, method_relief)
results_path = "/home/colombelli/Documents/Experiments09_abr/BRCA/Hom_mean_oner/"
perform_selection_hom(dataset_path, results_path, method_oner)





########### SINGLE FS EXPERIMENTS ##############


######### KIRP
dataset_path = "/home/colombelli/Documents/datasets/research/kirp.rds"

results_path = "/home/colombelli/Documents/Experiments09_abr/KIRP/sin_gr/"
perform_selection_single(dataset_path, results_path, method_gr)
results_path = "/home/colombelli/Documents/Experiments09_abr/KIRP/sin_su/"
perform_selection_single(dataset_path, results_path, method_su)
results_path = "/home/colombelli/Documents/Experiments09_abr/KIRP/sin_geode/"
perform_selection_single(dataset_path, results_path, method_geode)
results_path = "/home/colombelli/Documents/Experiments09_abr/KIRP/sin_relieff/"
perform_selection_single(dataset_path, results_path, method_relief)
results_path = "/home/colombelli/Documents/Experiments09_abr/KIRP/sin_oner/"
perform_selection_single(dataset_path, results_path, method_oner)


######### UCEC
dataset_path = "/home/colombelli/Documents/datasets/research/ucec.rds"

results_path = "/home/colombelli/Documents/Experiments09_abr/UCEC/sin_gr/"
perform_selection_single(dataset_path, results_path, method_gr)
results_path = "/home/colombelli/Documents/Experiments09_abr/UCEC/sin_su/"
perform_selection_single(dataset_path, results_path, method_su)
results_path = "/home/colombelli/Documents/Experiments09_abr/UCEC/sin_geode/"
perform_selection_single(dataset_path, results_path, method_geode)
results_path = "/home/colombelli/Documents/Experiments09_abr/UCEC/sin_relieff/"
perform_selection_single(dataset_path, results_path, method_relief)
results_path = "/home/colombelli/Documents/Experiments09_abr/UCEC/sin_oner/"
perform_selection_single(dataset_path, results_path, method_oner)



######### THCA
dataset_path = "/home/colombelli/Documents/datasets/research/thca.rds"

results_path = "/home/colombelli/Documents/Experiments09_abr/THCA/sin_gr/"
perform_selection_single(dataset_path, results_path, method_gr)
results_path = "/home/colombelli/Documents/Experiments09_abr/THCA/sin_su/"
perform_selection_single(dataset_path, results_path, method_su)
results_path = "/home/colombelli/Documents/Experiments09_abr/THCA/sin_geode/"
perform_selection_single(dataset_path, results_path, method_geode)
results_path = "/home/colombelli/Documents/Experiments09_abr/THCA/sin_relieff/"
perform_selection_single(dataset_path, results_path, method_relief)
results_path = "/home/colombelli/Documents/Experiments09_abr/THCA/sin_oner/"
perform_selection_single(dataset_path, results_path, method_oner)


######### BRCA
dataset_path = "/home/colombelli/Documents/datasets/research/brca.rds"

results_path = "/home/colombelli/Documents/Experiments09_abr/BRCA/sin_gr/"
perform_selection_single(dataset_path, results_path, method_gr)
results_path = "/home/colombelli/Documents/Experiments09_abr/BRCA/sin_su/"
perform_selection_single(dataset_path, results_path, method_su)
results_path = "/home/colombelli/Documents/Experiments09_abr/BRCA/sin_geode/"
perform_selection_single(dataset_path, results_path, method_geode)
results_path = "/home/colombelli/Documents/Experiments09_abr/BRCA/sin_relieff/"
perform_selection_single(dataset_path, results_path, method_relief)
results_path = "/home/colombelli/Documents/Experiments09_abr/BRCA/sin_oner/"
perform_selection_single(dataset_path, results_path, method_oner)
"""