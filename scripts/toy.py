from efsassembler.Experiments import Experiments
from copy import deepcopy

datasets = ["/home/colombelli/Documents/datasets/toy_prad_reduced.csv"]


relieff = ("reliefF", "python", "rf")
geode = ("geoDE", "python", "gd")
gr = ("gain-ratio", "r", "gr")
su = ("symmetrical-uncertainty", "r", "su")
wx = ("wx", "python", "wx")

all_fs = [relieff, geode, gr, su, wx]
ths = [1,3,5,10,15,20,30,50]
seed = 42
k = 3
num_bs = 3
classifier = "gbc"

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
        "datasets": datasets,
        "classifier": classifier
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
        "datasets": datasets,
        "classifier": classifier
}

hyb2={
        "type": "hyb",
        "thresholds": ths,
        "bootstraps": num_bs,
        "seed": seed,
        "folds": k,
        "aggregators": ["stb_weightened_layer1", "borda"],
        "rankers": all_fs,
        "datasets": datasets,
        "classifier": classifier
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
        "datasets": datasets,
        "classifier": classifier
    }

sin_base={
        "type": "sin",
        "thresholds": ths,
        "seed": seed,
        "folds": k,
        "datasets": datasets,
        "classifier": classifier
    }

for sel in all_fs:
        hom_exp = deepcopy(hom_base)
        hom_exp["rankers"] = [sel]
        hom_exps.append(hom_exp)

        sin_exp = deepcopy(sin_base)
        sin_exp["rankers"] = [sel]
        sin_exps.append(sin_exp)




experiments = [het, hom_exps[2], sin_exps[3], hyb1]


results_path = "/home/colombelli/Documents/experiments/toy"

print("STARTING PROCESS!!!")
exp = Experiments(experiments, results_path)
exp.run()


