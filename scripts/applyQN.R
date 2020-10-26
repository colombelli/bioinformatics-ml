setwd("~/Dropbox/Pesquisa/Projeto_Felipe_Normalizacao/")
load("lung.RData")

# https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0156594
# if (!requireNamespace("BiocManager", quietly = TRUE))
#     install.packages("BiocManager")
# BiocManager::install("preprocessCore")

library(preprocessCore) #for normalization functions
library(data.table)
library(sva) #for combat function

source("normalizationMethods.R")

preProcessDataset <- function(dataset){
    dataset.df <- subset(dataset, select=-c(class,samples))
    dataset.annot <- subset(dataset, select=c(class,samples))
    genes <- colnames(dataset.df)
    samples <- dataset.annot$samples
    
    dataset.t <- t(dataset.df)
    dataset.t <- data.frame(cbind(genes,dataset.t))
    colnames(dataset.t) <- c("Gene",samples)
    return(list(dataset.t,dataset.annot))
}


cumida1.preproc <- preProcessDataset(cumida1)
cumida1.preproc.qn <- cumida1.preproc[[1]]

cumida2.preproc <- preProcessDataset(cumida2)
cumida2.preproc.qn <- cumida2.preproc[[1]]

cumida3.preproc <- preProcessDataset(cumida3)
cumida3.preproc.qn <- cumida3.preproc[[1]]

tcga_rnaseq.preproc <- preProcessDataset(tcga_rnaseq)
tcga_rnaseq.preproc.qn <- tcga_rnaseq.preproc[[1]]


## APPLY COMBAT TO REMOVE BATCH EFFECTS
#define batch. 0 means microarray, 1 means RNA-Seq
numSamplesMicroarray <- dim(cumida1)[1]+dim(cumida2)[1]+dim(cumida3)[1]
numSamplesRNASeq <- dim(tcga_rnaseq)[1]
batches = c(rep(1,numSamplesRNASeq),rep(0,numSamplesMicroarray))
mod2<-model.matrix(~0+batches)
##merge datasets

dat.merged = rbind(subset(tcga_rnaseq, select=-c(class,samples)),
                   subset(cumida1, select=-c(class,samples)),
                   subset(cumida2, select=-c(class,samples)),
                   subset(cumida3, select=-c(class,samples)))

##Add C1, C2, C3 to allow data separation after normalization
row.names(dat.merged) <- c(tcga_rnaseq$samples,
                           paste("C1.",cumida1$samples,sep=""),
                           paste("C2.",cumida2$samples,sep=""),
                           paste("C3.",cumida3$samples,sep=""))

##remove batch effects
cleandat.merged <- ComBat(t(dat.merged),batches)

## APPLY QN TO MERGED DATA FOR QUANTILE NORMALIZATION
cleandat.merged.qn <- QNSingleDT(data.table(cleandat.merged))
cleandat.merged.qn2 <- as.data.frame(t(cleandat.merged.qn))
# boxplot(cleandat.merged.qn[c(560:570,580:590,670:680,785:795),],main="ComBat+QN",las=2)


##separate and export datasets following the original format

##TCGA
tcga_rnaseq.final <- data.frame(cbind(tcga_rnaseq$samples,cleandat.merged.qn2[tcga_rnaseq$samples,],tcga_rnaseq$class))
colnames(tcga_rnaseq.final) <- c("samples",colnames(dat.merged),"class")


##CUMIDA1
cumida1.final <- data.frame(cbind(cumida1$samples,cleandat.merged.qn2[grep("C1",row.names(cleandat.merged.qn2)),],cumida1$class))
colnames(cumida1.final) <- c("samples",colnames(dat.merged),"class")


##CUMIDA2
cumida2.final <- data.frame(cbind(cumida2$samples,cleandat.merged.qn2[grep("C2",row.names(cleandat.merged.qn2)),],cumida2$class))
colnames(cumida2.final) <- c("samples",colnames(dat.merged),"class")


##CUMIDA3
cumida3.final <- data.frame(cbind(cumida3$samples,cleandat.merged.qn2[grep("C3",row.names(cleandat.merged.qn2)),],cumida3$class))
colnames(cumida3.final) <- c("samples",colnames(dat.merged),"class")


save(list=c("tcga_rnaseq.final","cumida1.final","cumida2.final","cumida3.final"), file="lung_normalized.RData")






#### FROM THIS POINT ON:  ONLY TESTS!! IGNORE...
# cumida1.qn <- QNProcessing(data.table(cumida1.preproc.qn),data.table(tcga_rnaseq.preproc.qn),zero.to.one = TRUE)
# ## inverse use of datasets does not return good results
# # cumida1.qn.v2 <- QNProcessing(data.table(tcga_rnaseq.preproc.qn),data.table(cumida1.preproc.qn),zero.to.one = TRUE)
# 
# data1 <- QNSingleDT(data.table(tcga_rnaseq.preproc.qn)) 
# data2 <- QNSingleDT(data.table(cumida1.preproc.qn)) 
# data3 <- QNSingleDT(data.table(cumida2.preproc.qn)) 
# data4 <- QNSingleDT(data.table(cumida3.preproc.qn)) 
# 

##TEST COMBAT AND QN OVER DATA
# #define batch. 0 means microarray, 1 means RNA-Seq
# batch = c(rep(0,90),rep(1,576))
# mod<-model.matrix(~0+batch)
# #merge datasets
# dat = rbind(subset(cumida1, select=-c(class,samples)),
#             subset(tcga_rnaseq, select=-c(class,samples)))
# 
# 
# #remove batch effects
# cleandat1 <- ComBat(t(dat),batch)
# cleandat1.qn <- QNSingleDT(data.table(cleandat1)) 
# pdf("boxplots_preprocess_datasets.pdf")
# boxplot(cleandat1[,c(70:110)],main="ComBat",las=2) 
# boxplot(cleandat1.qn[,c(70:110)],main="ComBat+QN",las=2) 
# 
# 
# ##QN data
# dat2 = rbind(t(subset(data2, select=-c(Gene))),t(subset(data1, select=-c(Gene))))
# cleandat2 <- ComBat(t(dat2),batch,mean.only = TRUE)
# boxplot(cleandat2[,c(70:110)],main="QN+ComBat",las=2) ##QN followed bt combat
# 
# boxplot(cumida1.qn[,c(70:110)],main="QN",las=2) ##only QN
# dev.off()



