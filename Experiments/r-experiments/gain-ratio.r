#!/usr/bin/env Rscript
library(optparse)
library(CORElearn)

option_list = list(
	make_option(c("-i", "--input"), type="character", default=NULL, 
              help="input csv dataset file path", metavar="FILE"),
  make_option(c("-o", "--output"), type="character", default=NULL, 
              help="output csv dataset file path", metavar="FILE")
); 
 
opt_parser = OptionParser(option_list=option_list);
args = parse_args(opt_parser);



if (length(args) != 3){
  print_help(opt_parser)
  stop("Missing arguments found.", call.=FALSE)
}



print("Reading dataset...")
df <- read.csv(args$input, header=TRUE)

# This is highly changeable depending on the dataset format
rownames(df) <- df[,1]
df[,1] <- NULL


df$class <- as.factor(df$class)
print("Calculating Information Gain Ratio...")
attScores <- attrEval(class ~ ., df, estimator="GainRatio") 

print("Processing output...")
rankDf <- as.data.frame(attScores)
rankDf <- rankDf[order(-rankDf$attScores),,drop=FALSE]
rankDf["rank"] <- c(1:length(rankDf$attScores))
rankDf["attScores"] <- NULL

print("Saving output CSV file...")
write.table(rankDf, args$output, sep=",")