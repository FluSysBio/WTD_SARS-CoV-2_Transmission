# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 11:39:02 2022

@author: af3bd
"""
import pandas as pd
from Bio import SeqIO


deer_samples = pd.read_csv('../0_original_deer_data/TableS1_deer_description.csv')
deer_samples['IRMA % coverage']=deer_samples['IRMA % coverage'].str.rstrip('%').astype('float') / 100.0
deer_samples=deer_samples[deer_samples['IRMA % coverage']>0.95]
deer_samples=deer_samples[~deer_samples['date'].isnull()]
deer_samples=deer_samples[deer_samples['states']!='MNY']
lineage_state_groups=dict(tuple(deer_samples.groupby(['lineage','states'])))

lineage_state_groups.keys()

def get_names(this_lineage,this_state, lineage_state_groups):
    this_lineage_state=lineage_state_groups[this_lineage, this_state]
    human_in_state=pd.read_csv('../0_original_deer_data/huamn_lineage_in_24_states/'+this_state+'_lineage_report.csv')
    human_in_state_lineage=human_in_state[human_in_state['lineage']==this_lineage]
    human_in_state_lineage=human_in_state_lineage[human_in_state_lineage['taxon'].str.startswith('hCoV-19')]
    
    combined_human_deer=pd.concat([this_lineage_state['taxon'],human_in_state_lineage['taxon']])
    combined_human_deer.to_csv('./gisaid_fasta_names/'+this_state+'_'+this_lineage+'_gisaid.txt', index=False,header=False)


states=list(deer_samples.groupby('states').groups.keys())
lineages=list(deer_samples.groupby('lineage').groups.keys())

for state in states:
    for lineage in lineages:
        if (lineage, state) in list(lineage_state_groups.keys()):
            get_names(lineage,state,lineage_state_groups)
            

deer_seq=SeqIO.to_dict(SeqIO.parse('../0_original_deer_data/all_deer_samples_aligned.fasta','fasta'))

taxon=set(deer_samples['taxon'])
deer_seq_keys=set(deer_seq.keys())
deer_seq_keys-taxon
taxon-deer_seq_keys

taxon=list(deer_samples['taxon'])
my_seq=[]
for deer_id in taxon:
    my_seq.append(deer_seq[deer_id])
    
SeqIO.write(my_seq, "../0_original_deer_data/283_deer_samples_aligned.fasta", "fasta")
    



















