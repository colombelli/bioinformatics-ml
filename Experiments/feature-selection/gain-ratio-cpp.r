#!/usr/bin/env Rscript
library(optparse)
library(FSelectorRcpp)

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
dfx <- df[c(1:226), c(1:length(df)-1)]
dfy <- dfy <- df$class


print("Calculating Information Gain Ratio...")
gr <- information_gain(x=dfx, y=dfy, type = "gainratio")


print("Processing output...")
gr <- gr[order(-gr$importance),,drop=FALSE]
rownames(gr) <- gr$attributes
gr$attributes <- NULL
gr["rank"] <- c(1:length(gr$importance))
gr$importance <- NULL


print("Saving rank...")
saveRDS(gr, args$output)