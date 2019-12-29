from Selector import RSelector
from Selector import PySelector
from DataManager import DataManager
import rpy2.robjects.packages as rpackages


datasetPath = "/home/colombelli/Documents/datasets/iqrSelectedGenes.rds"
resultsPath = "/home/colombelli/Documents/bioinformatics-ml/EnsembleSelector-v2.0/results/"
#datasetPath = "/home/colombelli/Documents/datasets/merged80Samples.rds"

rpackages.importr('CORElearn')
rpackages.importr('FSelectorRcpp')
rpackages.importr('FSelector')


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


dm = DataManager(resultsPath, datasetPath, bags, folds, seed)
bootstrap = dm.getBootStrap(1)
df = bootstrap[0]["training"]
#selector = PySelector("svm", "svm_rfe")
selector = RSelector("gr", "gain-ratio-cpp", "gainRatio")

print(selector.select(df, resultsPath))