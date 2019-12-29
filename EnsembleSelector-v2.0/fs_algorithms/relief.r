relief <- function(df, outputPath) {

  df$class <- as.factor(df$class)
  print("Reliefing... :)")
  attScores <- attrEval(class ~ ., df, estimator="Relief") 


  print("Processing output...")
  rankDf <- as.data.frame(attScores)
  rankDf <- rankDf[order(-rankDf$attScores),,drop=FALSE]
  rankDf["rank"] <- c(1:length(rankDf$attScores))
  rankDf["attScores"] <- NULL


  print("Saving ranking...")
  saveRDS(rankDf, outputPath)

  return(rankDf)
}