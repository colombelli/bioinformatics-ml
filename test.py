import rpy2.robjects.packages as rpackages
from efsassembler.Experiments import Experiments

rpackages.quiet_require('FSelectorRcpp')

micarr_npn = "/home/colombelli/Documents/datasets/assembler/brca_micarr_npn.csv"

sin={
        "type": "sin",
        "thresholds": [5, 10, 20],
        "seed": 14,
        "folds": 5,
        "selectors": [("wx", "python", "wx")],
        "datasets": [micarr_npn]
    }

het={
        "type": "het",
        "thresholds": [5, 10, 20],
        "seed": 14,
        "folds": 5,
        "aggregators": ["borda"],
        "selectors": [("wx", "python", "wx"), ("gain-ratio", "r", "gr"), ("geoDE", "python", "gd")],
        "datasets": [micarr_npn]
    }

hom={
        "type": "hom",
        "thresholds": [5, 10, 20],
        "bootstraps": 3,
        "seed": 14,
        "folds": 3,
        "aggregators": ["borda"],
        "selectors": [("wx", "python", "wx")],
        "datasets": [micarr_npn]
    }

hyb1={
        "type": "hyb",
        "thresholds": [5, 10, 20],
        "bootstraps": 3,
        "seed": 14,
        "folds": 3,
        "aggregators": ["borda", "borda"],
        "selectors": [("wx", "python", "wx"), ("gain-ratio", "r", "gr"), ("geoDE", "python", "gd")],
        "datasets": [micarr_npn]
}

hyb2={
        "type": "hyb",
        "thresholds": [5, 10, 20],
        "bootstraps": 3,
        "seed": 14,
        "folds": 3,
        "aggregators": ["stb_weightened_layer1", "borda"],
        "selectors": [("wx", "python", "wx"), ("gain-ratio", "r", "gr"), ("geoDE", "python", "gd")],
        "datasets": [micarr_npn]
}

experiments = [hyb1, hyb2]

results_path = "/home/colombelli/Documents/Exptest"

print("STARTING PROCESS!!!")
exp = Experiments(experiments, results_path)
exp.run()


