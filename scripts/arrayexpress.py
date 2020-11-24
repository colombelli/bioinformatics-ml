from efsassembler.Experiments import Experiments
from copy import deepcopy

base = "/home/colombelli/Documents/arrayexpress/"
datasets = [base+"liver.csv", base+"lung.csv", base+"breast.csv"]


relieff = ("reliefF", "python", "rf")
geode = ("geoDE", "python", "gd")
gr = ("gain-ratio", "r", "gr")
su = ("symmetrical-uncertainty", "r", "su")
wx = ("wx", "python", "wx")

all_fs = [relieff, geode, gr, su, wx]
ths = [i for i in range(1,51)] + [75, 100, 150, 200, 500]
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
        "rankers": all_fs,
        "datasets": datasets
    }


# -----------------------------------
#       HYBRID
# -----------------------------------

hyb1={
        "type": "hyb",
        "thresholds": ths,
        "bootstraps": num_bs,
        "seed": seed,
        "folds": k,
        "aggregators": ["borda", "borda"],
        "rankers": all_fs,
        "datasets": datasets
}

hyb2={
        "type": "hyb",
        "thresholds": ths,
        "bootstraps": num_bs,
        "seed": seed,
        "folds": k,
        "aggregators": ["stb_weightened_layer1", "borda"],
        "rankers": all_fs,
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
        hom_exp["rankers"] = [sel]
        hom_exps.append(hom_exp)

        sin_exp = deepcopy(sin_base)
        sin_exp["rankers"] = [sel]
        sin_exps.append(sin_exp)




experiments = [het, hyb1, hyb2] + hom_exps + sin_exps


results_path = base + "results/"

print("STARTING PROCESS!!!")
exp = Experiments(experiments, results_path)
exp.run()


