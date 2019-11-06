library(FSelector)
#filePath <- "/home/colombelli/Documents/datasets/shuffledMerge.txt"
filePath <- '/home/colombelli/Documents/datasets/merged.RData'

print("Reading data...")
#df <- read.delim(filePath, header=TRUE, nrows=70)
#df$class <- as.factor(df$class)
load(filePath)
df.merged$class <- as.factor(df.merged$class)


print("Selecting features with Symmetrical Uncertainty...")

startTime <- Sys.time()
attScores <- symmetrical.uncertainty(class ~ ., df.merged)
endTime <- Sys.time()

timeTaken <- endTime - startTime

print("Time taken to select features:")
print(timeTaken)
print("10 top features:")
print(cutoff.k(attScores, k=10)