# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 16:34:36 2022

@author: longy
"""

import pandas as pd
from collections import OrderedDict

combined=pd.DataFrame([])
for gene in ['S','ORF1a','ORF1b','ORF3a','ORF6','ORF7a','ORF7b','ORF8','N','ORF9b','E','M']:
    temp=pd.read_csv('./mutation_tables_lineage_staste/aaSubstitutions_'+gene+'_outbreak.csv',index_col=0)
    for mutation in list(temp.columns):
        new_name=gene+':'+mutation
        print(new_name)
        temp=temp.rename(columns={mutation: new_name})

    combined=pd.concat([combined,temp],axis=1)
combined.to_csv('./mutation_tables_lineage_staste/aaSubstitutions_combined_outbreak.csv')


combined=pd.DataFrame([])
for gene in ['S','ORF1a','ORF1b','ORF3a','ORF6','ORF7a','ORF7b','ORF8','N','ORF9b','E','M']:
    temp=pd.read_csv('./mutation_tables/aaSubstitutions_'+gene+'_outbreak.csv',index_col=0)
    for mutation in list(temp.columns):
        new_name=gene+':'+mutation
        print(new_name)
        temp=temp.rename(columns={mutation: new_name})

    combined=pd.concat([combined,temp],axis=1)
combined.to_csv('./mutation_tables/aaSubstitutions_combined_outbreak.csv')


# merge cluster info with mutations
get_id=lambda s:float(s.split('_')[0])

mutation_table=pd.read_csv('./mutation_tables/aaSubstitutions_combined_outbreak.csv')
mutation_table['id']=list(map(get_id,mutation_table['X']))
mutation_table=mutation_table.drop('X',axis=1)

cluster_table=pd.read_csv('../../fig2/find_close_human_seq/2_clusters_counts/cluster_info_based_on_lineage_state_tree_manully_revised_01242023.csv')
cluster_table=cluster_table[['id','state', 'lineage','deer_counts', 'type']]


results=cluster_table.merge(mutation_table,left_on='id', right_on='id',how='outer')
results.to_csv('./mutation_tables/aaSubstitutions_combined_outbreak_with_cluster_info.csv')


# remove not follow the cluster definition
results=results[results['type'].notnull()]
results=results.set_index('id')

# selected those only 0 percentage in human
mutation_list=list(results.columns[4:])
selected_mutation=[]
for mutation in mutation_list:
    percentage=mutation.split('_')[1]
    if float(percentage)<=0:
        selected_mutation.append(mutation)
        print(mutation)
results=results[list(results.columns[0:4])+selected_mutation]
results.to_csv('./mutation_tables/aaSubstitutions_combined_outbreak_with_cluster_info_only0percent.csv')

# remove those mutations that not in the lineage-state table
lineage_state_table=list(pd.read_csv('./mutation_tables_lineage_staste/aaSubstitutions_combined_outbreak.csv',index_col=0).columns)
for mutation in list(results.columns[4:]):
    if mutation not in lineage_state_table:
        results=results.drop(mutation,axis=1)
        
results.to_csv('./mutation_tables/aaSubstitutions_combined_outbreak_with_cluster_info_only0percent_RemoveNotInLineageState.csv')
            

# only zeor-one values in the matrix and put the gene in the names
for mutation in list(results.columns[4:]):
    new_name=mutation.split('_')[0]+'_'+mutation.split('_')[2]
    print(new_name)
    results=results.rename(columns={mutation: new_name})
    
temp=results.iloc[:,4:]
temp[~pd.isna(temp)] = 1 
temp[pd.isna(temp)] = 0 
results.iloc[:,4:]=temp
results.to_csv('./mutation_tables/aaSubstitutions_combined_outbreak_with_cluster_info_only0percent_RemoveNotInLineageState_01Values.csv')

# select two repeated mutations
temp=results.iloc[:,4:]
temp_columns=temp.columns[temp.sum()>=2]
temp=temp[temp_columns]
results=pd.concat([results.iloc[:,0:4],temp],axis=1)
results.to_csv('./mutation_tables/aaSubstitutions_combined_outbreak_with_cluster_info_only0percent_RemoveNotInLineageState_01Values_2repeat.csv')

# sort
results_groups=dict(tuple(results.groupby('lineage')))
temp=results_groups.copy()
temp2={}
del temp['B.1.1.7']
del temp['P.1']
del temp['BA.1.1']
key_list=list(temp.keys())
for key in key_list:
    if len(temp[key])<2:
        temp2[key]=temp[key]
        del temp[key]
        
temp=OrderedDict(sorted(temp.items()))
results=pd.DataFrame()
for key in temp.keys():
    results=pd.concat([results,temp[key]])

for key in temp2.keys():
    results=pd.concat([results,temp2[key]])
    
for key in ['B.1.1.7','P.1','BA.1.1']:
    results=pd.concat([results,results_groups[key]])

results.to_csv('./mutation_tables/aaSubstitutions_combined_outbreak_with_cluster_info_only0percent_RemoveNotInLineageState_01Values_2repeat_sorted.csv')

    