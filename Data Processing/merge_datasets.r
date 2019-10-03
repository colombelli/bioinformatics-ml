# Paths
fileName1 <- "/home/colombelli/Documents/datasets/procNormalSamples.txt"
fileName2 <- "/home/colombelli/Documents/datasets/procTumorSamples.txt"

print("Reading datasets...")
normal <- read.delim(fileName1, header = TRUE, nrows = 300)
tumor <- read.delim(fileName2, header = TRUE, nrows = 300)

print("Merging datasets...")
mergedDF <- rbind(normal, tumor)

print("Saving merged datasets as mergedNormalTumor.txt...")
fileName <- "/home/colombelli/Documents/datasets/mergedNormalTumor.txt"
write.table(mergedDF, fileName, sep="\t", row.names = TRUE, col.names = TRUE)

print("Shuffling merged datasets...")
shuffledMerge <- mergedDF[sample(nrow(mergedDF)),]

print("Saving shuffled version as shuffledMerge.txt...")
fileName <- "/home/colombelli/Documents/datasets/shuffledMerge.txt"
write.table(shuffledMerge, fileName, sep="\t", row.names = TRUE, col.names = TRUE)