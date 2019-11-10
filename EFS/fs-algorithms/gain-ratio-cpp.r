gainRatio <- function(df, outputPath) {
  
  df$class <- as.factor(df$class)
  dfx <- df[c(1:226), c(1:length(df)-1)]
  dfy <- dfy <- df$class


  print("Calculating Information Gain Ratio...")
  rankDf <- information_gain(x=dfx, y=dfy, type = "gainratio")


  print("Processing output...")
  rankDf <- rankDf[order(-rankDf$importance),,drop=FALSE]
  rownames(rankDf) <- rankDf$attributes
  rankDf$attributes <- NULL
  rankDf["rank"] <- c(1:length(rankDf$importance))
  rankDf$importance <- NULL


  print("Saving rank...")
  saveRDS(rankDf, outputPath)

  return(rankDf)
}