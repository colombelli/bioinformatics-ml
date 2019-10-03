print("Trying to access file:")
fileName <- "/home/colombelli/Documents/datasets/GSM1536837_06_01_15_TCGA_24.tumor_Rsubread_TPM.txt"
print(fileName)

print("Reading dataset...")
#df <- read.delim(fileName, header=TRUE)

# Reading only 300 samples (which are in the columns)
samplesToBeLoaded <- 300
colsToLoad <- c("character", rep("double", samplesToBeLoaded), rep("NULL", 9265-samplesToBeLoaded))

df <- read.table(fileName, header = TRUE, sep = "\t", quote = "\"", 
    dec = ".", fill = TRUE, comment.char = "", colClasses = colsToLoad)

print("Processing dataset...")

# Transpose df maintaining header
df <- setNames(as.data.frame(t(df[,-1])), df[,1])

# Adding class column
df$class <- 1

print("File will be saved in:")
fileName = "/home/colombelli/Documents/datasets/procTumorSamples.txt"
print(fileName)

print("Saving processed dataset...")
write.table(df, fileName, sep="\t", row.names = TRUE, col.names = TRUE)

print("Done!")