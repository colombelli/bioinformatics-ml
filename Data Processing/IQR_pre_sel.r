#!/usr/bin/env Rscript
library("optparse")
 
option_list = list(
	make_option(c("-d", "--dataset"), type="character", default=NULL, 
              help=".rds dataset file path", metavar="character"),
    make_option(c("-f", "--fraction"), type="numeric", default=0.4, 
              help="fraction of genes to drop", metavar="numeric")
); 
 
opt_parser = OptionParser(option_list=option_list);
args = parse_args(opt_parser);



if (length(args) != 3){
  print_help(opt_parser)
  stop("Missing arguments found.", call.=FALSE)
}


print("Reading dataset...") 
df <- readRDS(args$dataset)


print("Calculating genes IQR...")
# applies IQR function column-wise for given dataset
genesIQR <- apply(df[1:length(df)-1], MARGIN=2, IQR)


print("Sorting genes by IQR value...")
# sort genes by IQR values
sortedGenesIQR <- sort(genesIQR, decreasing=TRUE)


fractionToKeep <- 1 - args$fraction
amountToKeep <- round(fractionToKeep * length(sortedGenesIQR))


# get the name of the genes to keep
genesToKeep <- names(sortedGenesIQR)[1:amountToKeep]


print("Selecting genes...")
iqrSelectedGenes <- df[append(genesToKeep, "class")]


print("Saving new dataset as iqrSelectedGenes.rds...")
saveRDS(iqrSelectedGenes, file="iqrSelectedGenes.rds")