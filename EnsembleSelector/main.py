from EFS import EFS
from DataManager import DataManager


#datasetPath = "/home/colombelli/Documents/datasets/tt.rds"
datasetPath = "/home/colombelli/Documents/datasets/merged80Samples.rds"
seed = 42
chosenFS = {
            "relief": False,
            "gainRatio": False,
            "symmetricalUncertainty": False,
            "oneR": False,
            "svmRFE": True
        }         

bags = 30
folds = 10

#efs = EFS(datasetPath, chosenFS, bags, folds)
#efs.buildRanks()

dm = DataManager(datasetPath, bags, folds, seed)






