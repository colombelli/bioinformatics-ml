# Parameters

interestedCancerType <- "BRCA"

# For the normal patients, parameters should be something like:
# classColumnValue <- 0
# samplesPath <- "/home/colombelli/Documents/datasets/GSM1697009_06_01_15_TCGA_24.normal_Rsubread_TPM.txt"
# processedDataPath <- "/home/colombelli/Documents/datasets/procNormalSamples2.txt"
# listOfPatientsByCancerTypePath <- "/home/colombelli/Documents/datasets/GSE62944_06_01_15_TCGA_24_Normal_CancerType_Samples.txt"

# For the sick patients, parameters should be something like:
classColumnValue <- 1
samplesPath <- "/home/colombelli/Documents/datasets/GSM1536837_06_01_15_TCGA_24.tumor_Rsubread_TPM.txt"
processedDataPath <- "/home/colombelli/Documents/datasets/procTumorSamples.txt"
listOfPatientsByCancerTypePath <- "/home/colombelli/Documents/datasets/GSE62944_06_01_15_TCGA_24_CancerType_Samples.txt"



print("Trying to access file:")
print(listOfPatientsByCancerTypePath)


print("Reading patients IDs with cancer type dataset...")
df <- read.delim(listOfPatientsByCancerTypePath, header=FALSE)


print("Colecting selected patients IDs...")
patientList <- c()
for(i in 1:nrow(df)) {
    
    ithPatient <- as.character(df[["V1"]][i])
    ithCancerType <- as.character(df[["V2"]][i])
    
    if (ithCancerType == interestedCancerType){
        patientList <- append(patientList, ithPatient)
    }
}


print("Formatting IDs...")
# Exchanges "-" characters to "." characters
patientList <- gsub("-", "\\.", patientList)    
patientList <- append(c("X"), patientList)


print("Trying to access file:")
print(samplesPath)


# Build the vector responsible to read only the selected patients
# The first column must be character (the name of the gene)
# The remaining columns must be double (the gene expression TPM value)
print("Building vector to select only the patients for given cancer type...")
df <- read.delim(samplesPath, header=TRUE, nrow=1)

colsToLoad <- c("character")
for (columnName in colnames(df)[2:length(colnames(df))]){
    
    if (columnName %in% patientList){
        colsToLoad <- append(colsToLoad, "double")
    }
    else{
        colsToLoad <- append(colsToLoad, "NULL")
    }
}


print("Reading gene expression dataset...")
df <- read.delim(samplesPath, header=TRUE, colClasses=colsToLoad)



print("Processing dataset...")

# Transpose df maintaining header
df <- setNames(as.data.frame(t(df[,-1])), df[,1])

# Adding class column
df$class <- classColumnValue

print("File will be saved in:")
print(processedDataPath)

print("Saving processed dataset...")
write.table(df, processedDataPath, sep="\t", row.names = TRUE, col.names = TRUE)

print("Done!")