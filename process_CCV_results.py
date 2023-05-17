# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 11:14:05 2022

@author: af3bd
"""

import pandas as pd
import os



deer_samples = pd.read_csv('../0_original_deer_data/TableS1_deer_description.csv')
deer_samples['IRMA % coverage']=deer_samples['IRMA % coverage'].str.rstrip('%').astype('float') / 100.0
deer_samples=deer_samples[deer_samples['IRMA % coverage']>0.95]
deer_samples=deer_samples[~deer_samples['date'].isnull()]
deer_samples=deer_samples[deer_samples['states']!='MNY']
lineage_state_groups=dict(tuple(deer_samples.groupby(['lineage','states'])))


remove_deer=lambda s:True if ('hCoV-19' in s) else False
include_human=lambda s: True if ('human' in s) else False
def get_closest_20(this_lineage,this_state,lineage_state_groups,database='gisaid'):
    
    if os.path.exists('./CCV_closest_selected/'+this_state+'_'+this_lineage+'_'+database+'_CCV.txt'):
        return None
    
    result_list=[]
    this_lineage_state=lineage_state_groups[this_lineage, this_state]
    CCV_matrix = pd.read_csv('./CCV_output/'+this_state+'_'+this_lineage+'_'+database+'.txt.fasta_CCV.txt',sep='\t', index_col=0,header=None)
    CCV_matrix=CCV_matrix.iloc[:,:-1]
    names=pd.DataFrame(list(CCV_matrix.index))
    for _,row in this_lineage_state.iterrows():
        #print(row['taxon'])
        temp=CCV_matrix.loc[row['taxon']].argsort()
        names_get=names.loc[temp]
        if database=='gisaid':
            names_get=names_get[list(map(remove_deer,names_get[0]))]
        if database=='ncbi':
            names_get=names_get[list(map(include_human,names_get[0]))]
        names_get=names_get[0:20]
        result_list.extend(list(names_get[0]))
        
    result_list=list(set(result_list))
    with open('./CCV_closest_selected/'+this_state+'_'+this_lineage+'_'+database+'_CCV.txt', 'w') as f:
        for line in result_list:
            f.write(f"{line}\n")    
    return result_list


states=list(deer_samples.groupby('states').groups.keys())
lineages=list(deer_samples.groupby('lineage').groups.keys())

for state in states:
    for lineage in lineages:
        if (lineage, state) in list(lineage_state_groups.keys()):
            if os.path.exists('./CCV_output/'+state+'_'+lineage+'_'+'ncbi'+'.txt.fasta_CCV.txt'):
                get_closest_20(lineage,state,lineage_state_groups,'ncbi')
            if os.path.exists('./CCV_output/'+state+'_'+lineage+'_'+'gisaid'+'.txt.fasta_CCV.txt'):
                get_closest_20(lineage,state,lineage_state_groups)

