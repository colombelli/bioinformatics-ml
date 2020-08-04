import rpy2.robjects.packages as rpackages
from efsassembler.Experiments import Experiments
from copy import deepcopy

rpackages.quiet_require('FSelectorRcpp')

intersect = "/home/colombelli/Documents/up_files/brca_rnaseq_genes_intersec.csv"
no_intersect = "/home/colombelli/Documents/up_files/brca_rnaseq_npn.csv"
#datasets = [intersect, no_intersect]
datasets = [intersect]

relieff = ("reliefF", "python", "rf")
geode = ("geoDE", "python", "gd")
gr = ("gain-ratio", "r", "gr")
su = ("symmetrical-uncertainty", "r", "su")
wx = ("wx", "python", "wx")

all_fs = [relieff, geode, gr, su, wx]
ths = [1, 5, 10, 15, 25, 50, 75, 100, 150, 200]
seed = 43
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




#experiments = [hyb1, hyb2] #[het, hyb1, hyb2]
#experiments += hom_exps + sin_exps
experiments = [sin_exps[0]]

results_path = "/home/colombelli/Documents/Experiments31_jul"

print("STARTING PROCESS!!!")
exp = Experiments(experiments, results_path)
exp.run()


