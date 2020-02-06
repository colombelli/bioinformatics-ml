select <- function(df, outputPath) {


  df$class <- as.factor(df$class)
  print("Classifying with One Rule algorithm...")
  rankDf <- oneR(class ~ ., df) 


  print("Processing output...")
  rankDf <- rankDf[order(-rankDf$attr_importance),,drop=FALSE]
  rankDf["rank"] <- c(1:length(rankDf$attr_importance))
  rankDf["attr_importance"] <- NULL


  print("Saving ranking...")
  saveRDS(rankDf, outputPath)

  return(rankDf)
}

