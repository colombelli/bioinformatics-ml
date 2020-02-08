MAX_SEED = 9999999
AGGREGATED_RANKING_FILE_NAME = "agg_ranking.rds"

# Used in InformationManager
SINGLE_FS_DESIGN = "Single FS Method"
HYBRID_FS_DESIGN = "Hybrid Ensemble"
HETEROGENEOUS_FS_DESIGN = "Heterogeneous Ensemble"
HOMOGENEOUS_FS_DESIGN = "Homogeneous Ensemble"

# info file
INFO_FILE_NAME = "experiment_info.txt"
TITLE_INFO_FILE = "Experiment Informations\n"
DESIGN_INFO_FILE = "Design: "
NUM_FOLDS_INFO_FILE = "Chosen k for stratified k-fold cv: "
NUM_BOOTSTRAPS_INFO_FILE = "Number of bootstraps: "
HYB_FST_AGG_INFO_FILE = "First aggregation method: "
HYB_SND_AGG_INFO_FILE = "Second aggregation method: "
HET_HOM_AGG_INFO_FILE = "Aggregation method: "
DATASET_USED = "Dataset: "
SINGLE_FS_INFO_FILE = "Feature Selection method: "
MULTIPLE_FS_INFO_FILE = "Feature Selection methods:"
SEED_INFO_FILE = "Seed: "

# csv files
CSV_AUC_TABLE_FILE_NAME = "aucs_results.csv"
CSV_FINAL_RESULTS_TABLE_FILE_NAME = "final_results.csv"
CSV_AUC_TABLE_COLUMNS = ["th_frac", "th_int"] #auc1, auc2, ..., aucn
CSV_FINAL_RESULTS_TABLE_COLUMNS = ["th_frac", "th_int", "stabilities", "mean_AUC"]