from DataManager import DataManager
from Evaluator import Evaluator
from Constants import *
import csv
from copy import deepcopy

class InformationManager:

    # aggregators: if there are, then it must be a python list cointaining either one string 
    # or two (in case the hybrid design was chosen); if there aren't (single FS), keep it None
    # methods: a list containing one or more strings representing the fs methods used
    def __init__(self, data_manager:DataManager, evaluator:Evaluator,
                 methods:list, aggregators=None):

        self.dm = data_manager
        self.evaluator = evaluator
        self.aggregators = aggregators
        self.methods = methods
        
        self.info_txt_lines = None
        self.design = self.__find_design()

        self.thresholds = None
        self.stabilities = None
        self.aucs = None

        self.__create_initial_file_info()


    def __find_design(self):

        if not(self.aggregators):
            self.__get_single_fs_info()
            return SINGLE_FS_DESIGN

        elif len(self.aggregators) == 2:
            self.__get_hybrid_info()
            return HYBRID_FS_DESIGN

        elif self.dm.num_bootstraps == 0:
            self.__get_heterogeneous_info()
            return HETEROGENEOUS_FS_DESIGN

        else:
            self.__get_homogeneous_info()
            return HOMOGENEOUS_FS_DESIGN



    def __create_initial_file_info(self):
        
        title = TITLE_INFO_FILE
        dataset = DATASET_USED + self.dm.file_path
        seed = SEED_INFO_FILE + str(self.dm.seed)
        design = DESIGN_INFO_FILE + self.design
        num_folds = NUM_FOLDS_INFO_FILE + str(self.dm.num_folds)

        lines = [title, dataset, seed, design, num_folds]
        self.info_txt_lines = lines + self.info_txt_lines

        self.__save_info_file()
        return        


    def __get_single_fs_info(self):

        fs_method = SINGLE_FS_INFO_FILE + self.methods[0]
        self.info_txt_lines = [fs_method]
        return
    
    def __get_homogeneous_info(self):

        num_bootstraps = NUM_BOOTSTRAPS_INFO_FILE + str(self.dm.num_bootstraps)
        fs_method = SINGLE_FS_INFO_FILE + self.methods[0]
        aggregator = HET_HOM_AGG_INFO_FILE + self.aggregators[0]

        self.info_txt_lines = [num_bootstraps, fs_method, aggregator]
        return
    
    def __get_heterogeneous_info(self):
        methods_title = MULTIPLE_FS_INFO_FILE
        fs_methods = ["- " + method for method in self.methods]
        aggregator = HET_HOM_AGG_INFO_FILE + self.aggregators[0]

        self.info_txt_lines = [methods_title] + fs_methods + [aggregator]
        return
    
    def __get_hybrid_info(self):
        num_bootstraps = NUM_BOOTSTRAPS_INFO_FILE + str(self.dm.num_bootstraps)
        methods_title = MULTIPLE_FS_INFO_FILE
        fs_methods = ["- " + method for method in self.methods]
        fst_aggregator = HYB_FST_AGG_INFO_FILE + self.aggregators[0]
        snd_aggregator = HYB_SND_AGG_INFO_FILE + self.aggregators[1]

        self.info_txt_lines = [num_bootstraps, methods_title] + fs_methods + \
                                [fst_aggregator, snd_aggregator]
        return


    def __save_info_file(self):

        with open(self.dm.results_path+INFO_FILE_NAME, "w") as file:
            for line in self.info_txt_lines:
                file.write(line)
                file.write("\n")
        return


    
    def create_csv_tables(self):
        self.__create_csv_auc_table()
        self.__create_csv_final_results()
        return
    

    def __create_csv_auc_table(self):
        
        with open(self.dm.results_path+CSV_AUC_TABLE_FILE_NAME, 'w', newline='') as file:
            writer = csv.writer(file)
            
            columns = deepcopy(CSV_AUC_TABLE_COLUMNS)
            for i in range(self.dm.num_folds):
                columns.append("AUC_"+str(i+1))

            writer.writerow(columns)

            for i, th in enumerate(self.evaluator.thresholds):
                frac_th = self.evaluator.frac_thresholds[i]
                
                aucs = []
                for auc in self.evaluator.aucs:
                    aucs.append(auc[i])

                row = [frac_th, th] + aucs
                writer.writerow(row)
        return
        

    def __create_csv_final_results(self):
        
        with open(self.dm.results_path+CSV_FINAL_RESULTS_TABLE_FILE_NAME, 'w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow(CSV_FINAL_RESULTS_TABLE_COLUMNS)

            for i, th in enumerate(self.evaluator.thresholds):
                frac_th = self.evaluator.frac_thresholds[i]
                stability = self.evaluator.stabilities[i]
                
                sum_aucs = 0
                for auc in self.evaluator.aucs:
                    sum_aucs += auc[i]
                mean_auc = sum_aucs / len(self.evaluator.aucs)

                row = [frac_th, th, stability, mean_auc]
                writer.writerow(row)
        return