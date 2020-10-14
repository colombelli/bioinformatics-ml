from efsassembler.Experiments import Experiments
from copy import deepcopy

datasets = ["/home/colombelli/Documents/datasets/tcga_combat_qn.csv"]


relieff = ("reliefF", "python", "rf")
geode = ("geoDE", "python", "gd")
gr = ("gain-ratio", "r", "gr")
su = ("symmetrical-uncertainty", "r", "su")
wx = ("wx", "python", "wx")

all_fs = [relieff, geode, gr, su, wx]
ths = [1, 5, 10, 20, 50, 100]
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
#       HYBRID
# -----------------------------------

hyb1={
        "type": "hyb",
        "thresholds": ths,
        "bootstraps": num_bs,
        "seed": seed,
        "folds": k,
        "aggregators": ["borda", "borda"],
        "selectors": all_fs,
        "datasets": datasets
}

hyb2={
        "type": "hyb",
        "thresholds": ths,
        "bootstraps": num_bs,
        "seed": seed,
        "folds": k,
        "aggregators": ["stb_weightened_layer1", "borda"],
        "selectors": all_fs,
        "datasets": datasets
}


# -----------------------------------
#     HOMOGENEOUS and SINGLE
# -----------------------------------

hom_exps = []

hom_base={
        "type": "hom",
        "thresholds": ths,
        "bootstraps": num_bs,
        "seed": seed,
        "folds": k,
        "aggregators": ["borda"],
        "datasets": datasets
    }


for sel in all_fs:
        hom_exp = deepcopy(hom_base)
        hom_exp["selectors"] = [sel]
        hom_exps.append(hom_exp)




experiments = [het, hyb1]


results_path = "/home/colombelli/Documents/experiments/LUNG_TEST_NPN_TRUNC/rankingCombat"

print("STARTING PROCESS!!!")
exp = Experiments(experiments, results_path)
exp.run()


