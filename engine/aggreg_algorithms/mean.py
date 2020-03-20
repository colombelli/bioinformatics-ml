import pandas as pd

def aggregate(self, rankings):
        
        aggregated_ranking = {}  # it's a dictionary where the keys 
                                # represent the genes and its values 
                                # are, at first, the sum of the ranking
                                # positions and, by the end, the mean
                                # value of the rankings 


        for gene in rankings[0].index:
            aggregated_ranking[gene] = 0

        for ranking in rankings:
            for gene in ranking.index: 
                aggregated_ranking[gene] += ranking.loc[gene, 'rank']

        num_rankings = len(rankings)
        for gene, ranking in aggregated_ranking.items():
            aggregated_ranking[gene] /= num_rankings 


        final_ranking = pd.DataFrame.from_dict(aggregated_ranking, orient='index')
        final_ranking.columns = ['rank']
       
        return final_ranking.sort_values(by='rank')