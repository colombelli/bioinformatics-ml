from DataManager import DataManager
from Evaluator import Evaluator
from Constants import *
import csv
from numpy import array as np_array
from numpy import mean as np_mean
from numpy import std as np_std
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
                
                aucs = np_array(self.evaluator.aucs).transpose()[i]
                mean_auc = np_mean(aucs)
                std_auc = np_std(aucs)

                row = [frac_th, th, stability, mean_auc, std_auc]
                writer.writerow(row)
        return


    def create_level2_csv_tables(self, aucs, stabilities):
        self.__create_intermediate_csv_auc_table(aucs, LVL2_CSV_AUC_TABLE_FILE_NAME)
        self.__create_intermediate_csv_stabilities_table(stabilities, LVL2_CSV_STB_TABLE_FILE_NAME)
        self.__create_intermediate_csv_final_results(aucs, stabilities, LVL2_CSV_FINAL_RESULTS_TABLE_FILE_NAME)
        return

    
    def __create_intermediate_csv_auc_table(self, aucs, table_name):

        with open(self.dm.results_path+table_name, 'w', newline='') as file:
            writer = csv.writer(file)
            
            columns = deepcopy(CSV_AUC_TABLE_COLUMNS)
            for i in range(len(aucs)):
                columns.append("AUC_"+str(i+1))

            writer.writerow(columns)

            aucs = np_array(aucs).transpose()

            for i, th in enumerate(self.evaluator.thresholds):
                frac_th = self.evaluator.frac_thresholds[i]
                row = [frac_th, th] + list(aucs[i])

                writer.writerow(row)
        return

    
    def __create_intermediate_csv_stabilities_table(self, stabilities, table_name):

        with open(self.dm.results_path+table_name, 'w', newline='') as file:
            writer = csv.writer(file)
            
            columns = deepcopy(CSV_AUC_TABLE_COLUMNS)
            for i in range(len(stabilities)):
                columns.append("Stb_"+str(i+1))

            writer.writerow(columns)

            stabilities = np_array(stabilities).transpose()

            for i, th in enumerate(self.evaluator.thresholds):
                frac_th = self.evaluator.frac_thresholds[i]
                row = [frac_th, th] + list(stabilities[i])
                writer.writerow(row)
        return


    def __create_intermediate_csv_final_results(self, aucs, stabilities, table_name):

        aucs = np_array(aucs).transpose()
        stabilities = np_array(stabilities).transpose()
        with open(self.dm.results_path+table_name, 'w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow(LVL2_CSV_FINAL_RESULTS_TABLE_COLUMNS)

            
            for i, th in enumerate(self.evaluator.thresholds):
                frac_th = self.evaluator.frac_thresholds[i]
                
                mean_auc = np_mean(aucs[i])
                std_auc = np_std(aucs[i])

                mean_stb = np_mean(stabilities[i])
                std_stb = np_std(stabilities[i])

                row = [frac_th, th, mean_stb, std_stb, mean_auc, std_auc]
                writer.writerow(row)

        return