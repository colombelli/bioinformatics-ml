from EFS import EFS


datasetPath = "/home/colombelli/Documents/datasets/tt.rds"

chosenFS = {
            "relief": False,
            "gainRatio": False,
            "symmetricalUncertainty": False,
            "oneR": False,
            "svmRFE": True
        }         

bags = 30
folds = 10

efs = EFS(datasetPath, chosenFS, bags, folds)
efs.buildRanks()






