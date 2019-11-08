import time
import pandas as pd
from sklearn.feature_selection import RFE
from sklearn.svm import SVR

print("Reading dataset...")
df = pd.read_csv('mergedIQR.csv')


X = df.iloc[0:, 1:-1]
y = df.iloc[:, -1]

startTime = time.time()

estimator = SVR(kernel="linear")
selector = RFE(estimator, 100, step=1)
print("Selecting the top 100 most relevant features...")
selector = selector.fit(X, y)

endTime = time.time()
elapsedTime = endTime - startTime


print("Time passed:", elapsedTime)

try:
    with open("support.txt","w+") as file:
        file.write(selector.support_)

    with open("ranking.txt","w+") as file:
        file.write(selector.ranking_)

except:
    print("\n\n\n")
    print("suppor", selector.support_)
    print("\n\n\n")
    print("ranking", selector.ranking_)