from EFS import EFS
from DataManager import DataManager
import time 

datasetPath = "/home/colombelli/Documents/datasets/iqrSelectedGenes.rds"
resultsPath = "/home/colombelli/Documents/bioinformatics-ml/EnsembleSelector/results2"
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

startTime = time.time()
dm = DataManager(resultsPath, datasetPath, bags, folds, seed)

efs = EFS(dm, chosenFS)
efs.selectFeatures()

endTime = time.time()
print(endTime - startTime)

"""
from Evaluate import Evaluate
import pickle
rankings = open('rankings.pkl', 'rb')      
rk = pickle.load(rankings) 
rankings.close() 

import pandas as pd
df = pd.read_pickle("df.pkl")

ev = Evaluate(rk, 80, df, df)
print(ev.getAUC())  
"""