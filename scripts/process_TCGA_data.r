# Author: Felipe Colombelli
# GitHub: @colombelli
# Title: GSE62944 Data Processing
#
# Description and how to use:
#
# This R script aims to automatically pre-process GSE62944 related data, from TCGA.
# In order to use it, you must have the following files (with their original names)
# placed in the same directory:
#
#   -   GSM1697009_06_01_15_TCGA_24.normal_Rsubread_TPM.txt
#   -   GSM1536837_06_01_15_TCGA_24.tumor_Rsubread_TPM.txt
#   -   GSE62944_06_01_15_TCGA_24_Normal_CancerType_Samples.txt
#   -   GSE62944_06_01_15_TCGA_24_CancerType_Samples.txt
#
#
# After asked for input the path for GSE/GSM files, you must provide an absolute path 
# like '/home/user/Documents/datasets/'.
#
# The same logic applies when inputting the directory where processed datasets and
# boxplots will be saved. Note that you must provide an existing path.
#
# The recommended fraction of genes to select by IQR (if chosen) is 0.6.


collectPatientIDs <- function(df) {
    
    patientList <- c()
    for(i in 1:nrow(df)) {

        ithPatient <- as.character(df[["V1"]][i])
        ithCancerType <- as.character(df[["V2"]][i])

        if (ithCancerType == interestedCancerType){
            patientList <- append(patientList, ithPatient)
        }
    }
    
    # Exchanges "-" characters to "." characters
    patientList <- gsub("-", "\\.", patientList)    
    patientList <- append(c("X"), patientList)
    return(patientList)
}


# Build the vector responsible to read only the selected patients
# The first column must be character (the name of the gene)
# The remaining columns must be double (the gene expression TPM value)

buildColumnsToLoadVector <- function(samplesPath, patientList) {
    
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
    return(colsToLoad) 
}



saveBoxplot <- function(normal, tumor, cancerType, outputPath, imageName) {
    
    randomSamples <- cbind(t(tumor[sample(1:nrow(tumor),size = 15),]),
                           t(normal[sample(1:nrow(normal),size = 15),]))
    

    png(filename=paste(outputPath, imageName, ".png", sep=""))
    
    boxplot(randomSamples, main = paste("Cancer type:", cancerType, 
                                        "(tumoral and non-tumoral samples)"),
            xlab = "Patients (random sampled)", ylab = "Gene expression value", xaxt="n")
    
    sink("NUL")
    dev.off()
    sink()
}


readline <- function(prompt){
    cat(prompt);
    return(readLines("stdin",n=1));
}




# Inputs

interestedCancerType <- readline(prompt="Enter interested cancer type (e.g. BRCA): ")
datasetsPath <- readline(prompt="Enter path for GSE and GSM files (file names must be the original ones): ")
processedDataPath <- readline(prompt="Enter path to save processed datasets and boxplots: ")


preselWithIQR <- readline(prompt="Do you wish to pre-select genes based on IQR? y/n ")
while (!(preselWithIQR %in% c("y", "n"))) {
    preselWithIQR <- readline(prompt="Please input 'y' if you want to do the IQR pre-selection or 'n' otherwise. ")
}
if(preselWithIQR == 'y') {
    fractionToKeep <- as.numeric(readline(prompt="Enter fraction of genes to keep (e.g. 0.6 for 60%): "))
    while (fractionToKeep %in% c(0, NA)) {
        fractionToKeep <- as.numeric(readline(prompt="Please, enter a convertable number also different from 0: "))
    }
}



normalSamplesFile <- paste(datasetsPath, 'GSM1697009_06_01_15_TCGA_24.normal_Rsubread_TPM.txt', sep="")
tumorSamplesFile <- paste(datasetsPath, 'GSM1536837_06_01_15_TCGA_24.tumor_Rsubread_TPM.txt', sep="")
listOfNormalSamples <- paste(datasetsPath, 'GSE62944_06_01_15_TCGA_24_Normal_CancerType_Samples.txt', sep="")
listOfTumorSamples <- paste(datasetsPath, 'GSE62944_06_01_15_TCGA_24_CancerType_Samples.txt', sep="")


print("Reading patients IDs...")
normalIDs <- read.delim(listOfNormalSamples, header=FALSE)
tumorIDs <- read.delim(listOfTumorSamples, header=FALSE)

print("Colecting selected patients IDs...")
normalPatientsList <- collectPatientIDs(normalIDs)
tumorPatientsList <- collectPatientIDs(tumorIDs)

print("Building vector to select only the patients for given cancer type...")
colsNormal <- buildColumnsToLoadVector(normalSamplesFile, normalPatientsList)
colsTumor <- buildColumnsToLoadVector(tumorSamplesFile, tumorPatientsList)


print("Reading gene expression datasets...")
normalDF <- read.delim(normalSamplesFile, header=TRUE, colClasses=colsNormal)
tumorDF <- read.delim(tumorSamplesFile, header=TRUE, colClasses=colsTumor)


# Transpose dataframe maintaining header
print("Transposing datasets...")
normalDF <- setNames(as.data.frame(t(normalDF[,-1])), normalDF[,1])
tumorDF <- setNames(as.data.frame(t(tumorDF[,-1])), tumorDF[,1])


print("Saving boxplot for non-normalized data...")
saveBoxplot(normalDF, tumorDF, interestedCancerType, processedDataPath, "non_normalized_boxplot")

print("Normalizing data...")
normalDF <- log2(normalDF + 1)
tumorDF <- log2(tumorDF + 1)

print("Saving boxplot for normalized data...")
saveBoxplot(normalDF, tumorDF, interestedCancerType, processedDataPath, "normalized_boxplot")

print("Adding class column...")
normalDF$class <- 0
tumorDF$class <- 1


print("Binding normal and tumor processed datasets...")
processedDF <- rbind(normalDF, tumorDF)


print("Processed dataset will be saved in:")
print(processedDataPath)
print(paste("Saving processed dataset as processed", interestedCancerType, ".rds...", sep=""))
saveRDS(processedDF, paste(processedDataPath, "processed", interestedCancerType, ".rds", sep=""))



if(preselWithIQR == 'y') {
    print("Calculating genes IQR...")
    # applies IQR function column-wise for given dataset
    genesIQR <- apply(processedDF[1:length(processedDF)-1], MARGIN=2, IQR)
    
    print("Sorting genes by IQR value...")
    # sort genes by IQR values
    sortedGenesIQR <- sort(genesIQR, decreasing=TRUE)
    
    amountToKeep <- round(fractionToKeep * length(sortedGenesIQR))
    
    # get the name of the genes to keep
    genesToKeep <- names(sortedGenesIQR)[1:amountToKeep]
    
    print("Selecting genes...")
    iqrSelectedGenes <- processedDF[append(genesToKeep, "class")]
    
    print("Saving new dataset as iqrSelectedGenes.rds...")
    saveRDS(iqrSelectedGenes, file=paste(processedDataPath, "iqrSelectedGenes.rds", sep=""))
}


print("All done! :)")