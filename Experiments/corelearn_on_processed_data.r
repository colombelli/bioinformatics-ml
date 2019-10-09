library(CORElearn)
filePath <- "/home/colombelli/Documents/datasets/shuffledMerge.txt"

print("Reading data...")
df <- read.delim(filePath, header=TRUE, nrows=70)
df$class <- as.factor(df$class)


print("Selecting features with infoGain...")

startTime <- Sys.time()
attScores <- attrEval(class ~ ., df, estimator="InfGain") 
endTime <- Sys.time()

timeTaken <- endTime - startTime

print("Time taken to select features:")
print(timeTaken)
print("10 top features:")
print(sort(attScores, decreasing=TRUE)[1:10])