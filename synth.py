from efsassembler.Experiments import Experiments
from copy import deepcopy


datasets = ["/home/colombelli/Documents/datasets/synth_df700x57.csv"]

relieff = ("reliefF", "python", "rf")
geode = ("geoDE", "python", "gd")
gr = ("gain-ratio", "r", "gr")
su = ("symmetrical-uncertainty", "r", "su")
wx = ("wx", "python", "wx")

#all_fs = [relieff, geode, gr, su, wx]
all_fs = [wx]
ths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
seed = 42
k = 5
num_bs = 10


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




experiments = sin_exps + hom_exps + [het]


results_path = "/home/colombelli/Documents/experiments/synth_test700x57_2/"

print("STARTING PROCESS!!!")
exp = Experiments(experiments, results_path)
exp.run()


