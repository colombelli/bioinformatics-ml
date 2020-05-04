import pandas as pd
import engine.kuncheva_index as ki
from engine import Hybrid

heavy = True

def aggregate(self, selector:Hybrid):
    
    bs_rankings = selector.dm.bs_rankings
    ths = selector.thresholds

    mean_th = sum(ths) // len(ths)
    fs_stabilities = get_fs_stabilities(mean_th, bs_rankings)
    
    aggregated_ranking = initialize_aggregated_ranking_dict(bs_rankings)
    
    for bs in bs_rankings:
        for fs, ranking in enumerate(bs_rankings[bs]):
            reversed_ranking = ranking.iloc[::-1]
            for gene in reversed_ranking.index: 
                aggregated_ranking[gene] += (reversed_ranking.index.get_loc(gene)+1) * fs_stabilities[fs]
    
    return build_df_and_correct_order(aggregated_ranking)



def initialize_aggregated_ranking_dict(bs_rankings):
    aggregated_ranking = {}
    for gene in list(bs_rankings[0][0].index):
        aggregated_ranking[gene] = 0
    return aggregated_ranking


def get_fs_stabilities(threshold, bs_rankings):
    
    num_fs = len(bs_rankings[0])
    
    stabilities = []
    for fs in range(num_fs):
        
        fs_rankings = []
        for bs in bs_rankings:
            df_ranking = bs_rankings[bs][fs]
            lst_genes = list(df_ranking.index.values)
            fs_rankings.append(lst_genes)
        
        stabilities.append(ki.get_kuncheva_index(fs_rankings, threshold=threshold))  
    return stabilities


def build_df_and_correct_order(aggregated_ranking):
    final_ranking = pd.DataFrame.from_dict(aggregated_ranking, orient='index')
    final_ranking.columns = ['rank']
    final_ranking = final_ranking.sort_values(by='rank', ascending=False)
    final_ranking.iloc[:] = final_ranking.iloc[::-1].values
    return final_ranking
