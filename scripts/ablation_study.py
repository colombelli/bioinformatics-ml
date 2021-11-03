from efsassembler import ExperimentRecyle
from copy import deepcopy
import os
import shutil


def run_ablation_study_for_cancer(cancer):
    print("RUNNING ABLATION STUDY FOR CANCER: ", cancer, "\n\n")
    base = "/home/colombelli/Documents/arrayexpress/"
    dataset = base+cancer+".csv"
    hyb_base_experiment_path = base+cancer+"/hyb_borda_borda/"
    het_base_experiment_path = base+cancer+"/het/"

    relieff = ("reliefF", "python", "rf")
    geode = ("geoDE", "python", "gd")
    gr = ("gain-ratio", "r", "gr")
    su = ("symmetrical-uncertainty", "r", "su")
    wx = ("wx", "python", "wx")

    all_fs = [relieff, geode, gr, su, wx]

    ths = [i for i in range(1,51)] + [75, 100, 150, 200, 500]
    #ths = [5,10,50,100]
    seed = 42
    num_bs = 50
    classifier= "gbc"


    for idx in range(len(all_fs)):
        fs_methods = [x for i,x in enumerate(all_fs) if i!=idx]
        hyb_experiment = {
            "type": "hyb",
            "thresholds": ths,
            "bootstraps": num_bs,
            "seed": seed,
            "aggregators": ["borda", "borda"],
            #"aggregators": ["stb_weightened_layer1", "borda"],
            "rankers": fs_methods,
            "dataset": dataset,
            "classifier": classifier
        }
        het_experiment = {
            "type": "het",
            "thresholds": ths,
            "seed": seed,
            "aggregators": ["borda"],
            "rankers": fs_methods,
            "dataset": dataset,
            "classifier": classifier
        }
        results_path = base+"ablation_study/"+cancer+"/"


        # Run hybrid
        exp = ExperimentRecyle(hyb_experiment, results_path, hyb_base_experiment_path)
        exp.run()
        # Delete unecessary/wrong files
        exp_dir = exp.dm.results_path
        os.remove(exp_dir+"experiment_info.txt")
        shutil.rmtree(exp_dir+"selection/")


        # Run heterogeneous
        exp = ExperimentRecyle(het_experiment, results_path, het_base_experiment_path)
        exp.run()
        # Delete unecessary/wrong files
        exp_dir = exp.dm.results_path
        os.remove(exp_dir+"experiment_info.txt")
        shutil.rmtree(exp_dir+"selection/")

        print("\n\n")


if __name__ == "__main__":
    
    for cancer in ["breast", "lung", "liver", "pancreas"]:
        run_ablation_study_for_cancer(cancer)