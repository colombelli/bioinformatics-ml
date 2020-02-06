select <- function(df) {


  df$class <- as.factor(df$class)
  print("Classifying with One Rule algorithm...")
  rankDf <- oneR(class ~ ., df) 


  print("Processing output...")
  rankDf <- rankDf[order(-rankDf$attr_importance),,drop=FALSE]
  rankDf["rank"] <- c(1:length(rankDf$attr_importance))
  rankDf["attr_importance"] <- NULL

  return(rankDf)
}

