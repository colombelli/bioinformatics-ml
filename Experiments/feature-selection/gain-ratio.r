#!/usr/bin/env Rscript
library(optparse)
library(CORElearn)

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
print("Calculating Information Gain Ratio...")
attScores <- attrEval(class ~ ., df, estimator="GainRatio") 


print("Processing output...")
rankDf <- as.data.frame(attScores)
rankDf <- rankDf[order(-rankDf$attScores),,drop=FALSE]
rankDf["rank"] <- c(1:length(rankDf$attScores))
rankDf["attScores"] <- NULL


print("Saving ranking output...")
saveRDS(rankDf, args$output)