from EFS import EFS
from DataManager import DataManager


datasetPath = "/home/colombelli/Documents/datasets/merged226Samples.rds"
#datasetPath = "/home/colombelli/Documents/datasets/merged80Samples.rds"

seed = 42
bags = 30
folds = 10




chosenFS = {
            "relief": False,
            "gainRatio": False,
            "symmetricalUncertainty": False,
            "oneR": False,
            "svmRFE": True
        }         



dm = DataManager(datasetPath, bags, folds, seed)

#efs = EFS(datasetPath, chosenFS, bags, folds)
#efs.buildRanks()



