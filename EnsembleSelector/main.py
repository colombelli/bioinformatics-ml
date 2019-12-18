from EFS import EFS
from DataManager import DataManager
from subprocess import call
from os import popen

datasetPath = "/home/colombelli/Documents/datasets/iqrSelectedGenes.rds"
resultsPath = "/home/colombelli/Documents/bioinformatics-ml/EnsembleSelector/results"
#datasetPath = "/home/colombelli/Documents/datasets/merged80Samples.rds"

seed = 42
bags = 30
folds = 10



chosenFS = {
            "relief": False,
            "gainRatio": True,
            "symmetricalUncertainty": True,
            "oneR": False,
            "svmRFE": False
        }         

print("Preparing enviroment...")
print("Running command: R CMD javareconf -e\n\n")
call(["R", "CMD", "javareconf", "-e"])
#popen('R CMD javareconf -e')
print("\n\n")

dm = DataManager(resultsPath, datasetPath, bags, folds, seed)

efs = EFS(dm, chosenFS)
efs.selectFeatures()
