print("Trying to access file:")
fileName <- "/home/colombelli/Documents/datasets/GSM1697009_06_01_15_TCGA_24.normal_Rsubread_TPM.txt"
print(fileName)

print("Reading dataset...")
df <- read.delim(fileName, header=TRUE)


print("Processing dataset...")

# Transpose df maintaining header
df <- setNames(as.data.frame(t(df[,-1])), df[,1])

# Adding class column
df$class <- 0

print("File will be saved in:")
fileName = "/home/colombelli/Documents/datasets/procNormalSamples.txt"
print(fileName)

print("Saving processed dataset...")
write.table(df, fileName, sep="\t", row.names = TRUE, col.names = TRUE)

print("Done!")