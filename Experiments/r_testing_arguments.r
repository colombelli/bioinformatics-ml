#!/usr/bin/env Rscript
library("optparse")
 
option_list = list(
  make_option(c("-d", "--dataset"), type="character", default=NULL, 
              help="dataset file name", metavar="character"),
	make_option(c("-r", "--random"), type="character", default="random", 
              help="random parameter [default= %default]", metavar="character")
); 
 
opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);

print("Those are the given arguments:")
print(opt)