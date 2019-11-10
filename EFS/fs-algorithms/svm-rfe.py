#!/usr/bin/python
from pandas import DataFrame
from pandas import read_csv
from time import time
from sklearn.feature_selection import RFE
from sklearn.svm import SVR
import sys
from argparse import ArgumentParser


"""
    DEALING WITH INITIAL ARGUMENTS
"""

parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="input",
                    help="input csv file name to use", metavar="FILE"),
parser.add_argument("-o", "--output", dest="output",
                    help="output csv file name to save", metavar="FILE")

args = parser.parse_args()

if (len(sys.argv) != 5):
    parser.print_help()
    print("\nMissing arguments were found.")
    sys.exit()






print("Reading dataset...")
df = read_csv(args.input, index_col=0)


X = df.iloc[0:, 1:-1]
y = df.iloc[:, -1]

startTime = time()

estimator = SVR(kernel="linear")
selector = RFE(estimator, 1, step=1)
print("Ranking features...")
selector = selector.fit(X, y)

endTime = time()
elapsedTime = endTime - startTime


print("Rank finished. Time taken:", elapsedTime)



print("Building CSV...")
data = {"rank": selector.ranking_}
rank = DataFrame(data, index=list(X.columns))


print("Saving CSV:", args.output)
rank.to_csv(args.output, index_label=False)