from efsassembler import Experiments
from copy import deepcopy

base = "/home/colombelli/Documents/pmlb_efs_experiments/"
datasets = [
        base+"clean2.csv",
        base+"Hill_Valley_without_noise.csv",
        base+"sonar.csv",
        base+"spambase.csv",
        base+"spectf.csv"
        ]


relieff = ("reliefF", "python", "rf")
geode = ("geoDE", "python", "gd")
gr = ("gain-ratio", "r", "gr")
su = ("symmetrical-uncertainty", "r", "su")
wx = ("wx", "python", "wx")

fss = [gr, su, wx]
all_fs = [relieff, geode, gr, su, wx]
ths = [0.05, 0.1, 0.25, 0.5]
seed = 42
k = 5
num_bs = 50
classifier= "gbc"



# -----------------------------------
#       HETEROGENEOUS
# -----------------------------------
"""
het={
        "type": "het",
        "thresholds": ths,
        "seed": seed,
        "folds": k,
        "aggregators": ["borda"],
        "rankers": all_fs,
        "datasets": datasets,
        "classifier": "gbc"
    }

het2={
        "type": "het",
        "thresholds": ths,
        "seed": seed,
        "folds": k,
        "aggregators": ["borda"],
        "rankers": fss,
        "datasets": datasets,
        "classifier": "gbc"
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
        "classifier": "gbc"
}
"""
hyb2={
        "type": "hyb",
        "thresholds": ths,
        "bootstraps": num_bs,
        "seed": seed,
        "folds": k,
        "aggregators": ["stb_weightened_layer1", "borda"],
        "rankers": all_fs,
        "datasets": datasets,
        "classifier": "gbc"
}

hyb3={
        "type": "hyb",
        "thresholds": ths,
        "bootstraps": num_bs,
        "seed": seed,
        "folds": k,
        "aggregators": ["stb_weightened_layer1", "borda"],
        "rankers": fss,
        "datasets": datasets,
        "classifier": "gbc"
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
        "classifier": "gbc"
    }

sin_base={
        "type": "sin",
        "thresholds": ths,
        "seed": seed,
        "folds": k,
        "datasets": datasets,
        "classifier": "gbc"
    }

for sel in all_fs:
        hom_exp = deepcopy(hom_base)
        hom_exp["rankers"] = [sel]
        hom_exps.append(hom_exp)

        sin_exp = deepcopy(sin_base)
        sin_exp["rankers"] = [sel]
        sin_exps.append(sin_exp)




#experiments = [het, het2, hyb1, hyb2, hyb3] + hom_exps + sin_exps
experiments = [hyb2, hyb3] + hom_exps + sin_exps
results_path = base + "results/"

print("STARTING PROCESS!!!")
exp = Experiments(experiments, results_path)
exp.run()