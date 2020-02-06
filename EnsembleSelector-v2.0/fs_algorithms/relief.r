select <- function(df) {

  df$class <- as.factor(df$class)
  print("Reliefing... :)")

  sink("NUL")
  attScores <- attrEval(class ~ ., df, estimator="Relief") 
  sink()


  print("Processing output...")
  rankDf <- as.data.frame(attScores)
  rankDf <- rankDf[order(-rankDf$attScores),,drop=FALSE]
  rankDf["rank"] <- c(1:length(rankDf$attScores))
  rankDf["attScores"] <- NULL

  return(rankDf)
}