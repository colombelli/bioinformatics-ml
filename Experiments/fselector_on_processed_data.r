library(FSelector)
filePath <- "/home/colombelli/Documents/datasets/shuffledMerge.txt"

print("Reading data...")
df <- read.delim(filePath, header=TRUE, nrows=70)
df$class <- as.factor(df$class)


print("Selecting features with infoGain...")

startTime <- Sys.time()
attScores <- information.gain(class ~ ., df)
endTime <- Sys.time()

timeTaken <- endTime - startTime

print("Time taken to select features:")
print(timeTaken)
print("50 top features:")
print(cutoff.k(attScores, k = 4))