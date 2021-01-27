from efsassembler import FeatureExtraction
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
num_bs = 3

# -----------------------------------
#       HETEROGENEOUS
# -----------------------------------

het={
        "type": "het",
        "thresholds": ths,
        "seed": seed,
        "aggregators": ["borda"],
        "rankers": all_fs,
        "datasets": datasets,
    }


# -----------------------------------
#       HYBRID
# -----------------------------------

hyb1={
        "type": "hyb",
        "thresholds": ths,
        "bootstraps": num_bs,
        "seed": seed,
        "aggregators": ["borda", "borda"],
        "rankers": all_fs,
        "datasets": datasets
}

hyb2={
        "type": "hyb",
        "thresholds": ths,
        "bootstraps": num_bs,
        "seed": seed,
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
        "balanced_selection": False,
        "aggregators": ["borda"],
        "datasets": datasets
    }

sin_base={
        "type": "sin",
        "thresholds": ths,
        "seed": seed,
        "balanced_selection": True,
        "datasets": datasets
    }

for sel in all_fs:
        hom_exp = deepcopy(hom_base)
        hom_exp["rankers"] = [sel]
        hom_exps.append(hom_exp)

        sin_exp = deepcopy(sin_base)
        sin_exp["rankers"] = [sel]
        sin_exps.append(sin_exp)



cfgs = [het, hom_exps[2], sin_exps[3], hyb1, hyb2]

results_path = "/home/colombelli/Documents/experiments/toy/extractions"

print("STARTING PROCESS!!!")
fe = FeatureExtraction(cfgs, results_path)
fe.run()


