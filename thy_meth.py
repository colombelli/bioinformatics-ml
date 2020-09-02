import rpy2.robjects.packages as rpackages
from efsassembler.Experiments import Experiments
from copy import deepcopy

rpackages.quiet_require('FSelectorRcpp')

datasets = ["/home/colombelli/Documents/up_files/GSE86961.csv"]


relieff = ("reliefF", "python", "rf")
geode = ("geoDE", "python", "gd")
gr = ("gain-ratio", "r", "gr")
su = ("symmetrical-uncertainty", "r", "su")
wx = ("wx", "python", "wx")

#all_fs = [relieff, geode, gr, su, wx]
all_fs = [geode, gr, su]
ths = [1, 5, 10, 15, 25, 50, 75, 100, 150, 200]
seed = 42
k = 5
num_bs = 50


# -----------------------------------
#       HETEROGENEOUS
# -----------------------------------

het={
        "type": "het",
        "thresholds": ths,
        "seed": seed,
        "folds": k,
        "aggregators": ["borda"],
        "selectors": all_fs,
        "datasets": datasets
    }




# -----------------------------------
#     HOMOGENEOUS and SINGLE
# -----------------------------------

hom_exps = []
sin_exps = []

hom_base={
        "type": "hom",
        "thresholds": ths,
        "bootstraps": num_bs,
        "seed": seed,
        "folds": k,
        "aggregators": ["borda"],
        "datasets": datasets
    }

sin_base={
        "type": "sin",
        "thresholds": ths,
        "seed": seed,
        "folds": k,
        "datasets": datasets
    }


for sel in all_fs:
        hom_exp = deepcopy(hom_base)
        hom_exp["selectors"] = [sel]
        hom_exps.append(hom_exp)

        sin_exp = deepcopy(sin_base)
        sin_exp["selectors"] = [sel]
        sin_exps.append(sin_exp)




experiments = [het]
#experiments += hom_exps + sin_exps


results_path = "/home/colombelli/Documents/Experiments02_set"

print("STARTING PROCESS!!!")
exp = Experiments(experiments, results_path)
exp.run()


