import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import metrics
import numpy as np

class Evaluate:

    def __init__(self, rankings, threshold, trainingDF, testingDF):

        self.rankings = self.__getGeneLists(rankings)
        self.threshold = threshold
        self.training_x = self.__getX(trainingDF)
        self.training_y = self.__getY(trainingDF)
        self.testing_x = self.__getX(testingDF)
        self.testing_y = self.__getY(testingDF)


    def __getGeneLists(self, pdRankings):
        geneLists = []

        for ranking in pdRankings:
            indexNamesArr = ranking.index.values
            geneLists.append(list(indexNamesArr))
        
        return geneLists


    def __getX(self, df):
        return df.loc[:, df.columns != 'class']
    
    def __getY(self, df):
        return df.loc[:, ['class']].T.values[0]



    def getAUC(self):
        
        clf = SVC(gamma='auto')
        clf.fit(self.training_x, self.training_y)
        
        pred = clf.predict(self.testing_x)
        y = self.testing_y
        

        fpr, tpr, thresholds = metrics.roc_curve(y, pred, pos_label=2)
        return metrics.auc(fpr, tpr)



