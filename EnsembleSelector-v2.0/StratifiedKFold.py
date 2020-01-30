import random
import pandas as pd
import numpy as np

class StratifiedKFold:
    
    def __init__(self, seed, dataframe, class_column_name, k, undersampling=True):
        random.seed(seed)
        
        self.df = dataframe
        self.class_coloumn_name = class_column_name
        self.k = k
        self.undersampling = undersampling

        
        self.classes = self.df[self.class_coloumn_name].unique()
        self.class_counts = self.df[self.class_coloumn_name].value_counts().to_dict()
        self.minority_count = self.class_counts[min(self.class_counts)]
        
        
        self.folds = self.__get_folds()   # a list with pandas Index objects, one per fold
        self.__shuffle_each_fold()
        
        
    def __get_folds(self):
        
        
        final_folds = [[] for _ in range(self.k)]
        for df_class in self.classes:
    
            class_indexes = self.df.loc[self.df[self.class_coloumn_name] == df_class].index.to_list()
            amount_per_fold = self.class_counts[df_class] // self.k
            
            random.shuffle(class_indexes)
            current_class_folds = [[] for _ in range(self.k)]

            for class_fold in current_class_folds:
                self.__get_random_samples(class_fold, class_indexes, amount_per_fold)

        
            self.__distribute_remaining_samples(amount_per_fold, current_class_folds, final_folds, class_indexes)
            if self.undersampling:
                self.__random_undersample(final_folds, current_class_folds)
            else:
                self.__append_in_final_folds(final_folds, current_class_folds)
        
        return final_folds
        
            
    def __get_random_samples(self, class_fold, samples, amount):
        
        for _ in range(amount):
            class_fold.append(samples.pop())
        return
    
    
    def __distribute_remaining_samples(self, current_amount, current_folds, final_folds, class_indexes):
        
        len_folds = np.array([len(x)+current_amount for x in final_folds])
        while class_indexes:
            fold_with_less_samples = len_folds.argmin()
            current_folds[fold_with_less_samples].append(class_indexes.pop())
            len_folds[fold_with_less_samples] += 1
            
        return
    
    
    def __random_undersample(self, final_folds, current_class_folds):
        
        base_per_fold = self.minority_count // self.k
        remaining_samples = self.minority_count - (self.k * base_per_fold)
        samples_per_fold = [base_per_fold for _ in range(self.k)]
        
        len_folds = np.array([len(x)+base_per_fold for x in final_folds])
        for _ in range(remaining_samples):
            fold_with_less_samples = len_folds.argmin()
            samples_per_fold[fold_with_less_samples] += 1
            len_folds[fold_with_less_samples] += 1

        
        for i, amount in enumerate(samples_per_fold):
            final_folds[i] = final_folds[i] + \
                            random.sample(current_class_folds[i], amount)
        return
    
    
    def __append_in_final_folds(self, final_folds, current_class_folds):
        
        for i, samples in enumerate(current_class_folds):
            final_folds[i] = final_folds[i] + samples
        return
    
    
    
    def __shuffle_each_fold(self):
        
        for fold in self.folds:
            random.shuffle(fold)
        return
    
    
    
    def split(self):
        
        for i, fold in enumerate(self.folds):
            
            test_set = fold
            train_set = [item for j,sublist in enumerate(self.folds) if j!=i for item in sublist]
            yield (train_set, test_set)