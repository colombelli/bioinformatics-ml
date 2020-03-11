from DataManager import DataManager
from Hybrid import Hybrid
from Heterogeneous import Heterogeneous
from Homogeneous import Homogeneous
from SingleFS import SingleFS
from Evaluator import Evaluator
from InformationManager import InformationManager
import rpy2.robjects.packages as rpackages
from time import time


num_bootstraps = 50
num_folds = 5

fs_methods = [
    ("reliefF", "python", "rf"),
    ("geoDE", "python", "gd"),
    ("gain-ratio", "r", "gr"),
    ("symmetrical-uncertainty", "r", "su"),
    ("oneR", "r", "or")
]

aggregator = "mean"

ths = [0.01, 0.02, 0.03, 0.04, 0.06, 0.08, 0.1, 0.2, 0.4]
seed = 42

str_methods = ["ReliefF", "GeoDE", "Gain Ratio", "Symmetrical Uncertainty", "OneR"]
str_aggregators = ["Mean Aggregation", "Mean Aggregation"]