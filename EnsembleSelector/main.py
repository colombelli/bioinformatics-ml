from EFS import EFS
from DataManager import DataManager


datasetPath = "/home/colombelli/Documents/datasets/iqrSelectedGenes.rds"
#datasetPath = "/home/colombelli/Documents/datasets/merged80Samples.rds"

seed = 42
bags = 30
folds = 10



chosenFS = {
            "relief": False,
            "gainRatio": False,
            "symmetricalUncertainty": True,
            "oneR": False,
            "svmRFE": False
        }         



dm = DataManager(datasetPath, bags, folds, seed)

efs = EFS(dm, chosenFS)
efs.selectFeatures()



