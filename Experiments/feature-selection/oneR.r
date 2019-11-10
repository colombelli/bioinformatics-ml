#!/usr/bin/env Rscript
library(optparse)
library(FSelector)

option_list = list(
	make_option(c("-i", "--input"), type="character", default=NULL, 
              help=".rds input file path", metavar="FILE"),
  make_option(c("-o", "--output"), type="character", default=NULL, 
              help="name/file path for .rds output rank", metavar="FILE")
); 
 
opt_parser = OptionParser(option_list=option_list);
args = parse_args(opt_parser);



if (length(args) != 3){
  print_help(opt_parser)
  stop("Missing arguments found.", call.=FALSE)
}



print("Reading dataset...")
df <- readRDS(args$input)


df$class <- as.factor(df$class)
print("Classifying with One Rule algorithm...")
rankDf <- oneR(class ~ ., df)


print("Processing output...")
rankDf <- rankDf[order(-rankDf$attr_importance),,drop=FALSE]
rankDf["rank"] <- c(1:length(rankDf$attr_importance))
rankDf["attr_importance"] <- NULL


print("Saving rank...")
saveRDS(rankDf, args$output)