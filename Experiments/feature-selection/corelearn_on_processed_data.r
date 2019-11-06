library(CORElearn)
#filePath <- "/home/colombelli/Documents/datasets/shuffledMerge_log2.txt"

print("Reading data...")
#df <- read.delim(filePath, header=TRUE, nrows=70)
#df$class <- as.factor(df$class)
filePath <- '/home/colombelli/Documents/datasets/merged.RData'
load(filePath)
df.merged$class <- as.factor(df.merged$class)

print("Selecting features with infoGain...")

startTime <- Sys.time()
attScores <- attrEval(class ~ ., df.merged, estimator="GainRatio") 
endTime <- Sys.time()

timeTaken <- endTime - startTime

print("Time taken to select features:")
print(timeTaken)
print("10 top features:")
print(sort(attScores, decreasing=TRUE)[1:10])