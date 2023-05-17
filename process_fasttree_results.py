# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 11:50:59 2022

@author: af3bd
"""

import ete3
from Bio import SeqIO
#import ipdb
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio import AlignIO
import os
from Bio.Align import MultipleSeqAlignment
import numpy as np
import pandas as pd
import re
import random

number_wanted=20

deer_samples = pd.read_csv('../0_original_deer_data/TableS1_deer_description.csv')
deer_samples['IRMA % coverage']=deer_samples['IRMA % coverage'].str.rstrip('%').astype('float') / 100.0
deer_samples=deer_samples[deer_samples['IRMA % coverage']>0.95]
deer_samples=deer_samples[~deer_samples['date'].isnull()]
deer_samples=deer_samples[deer_samples['states']!='MNY']
lineage_state_groups=dict(tuple(deer_samples.groupby(['lineage','states'])))
deer_aligned=SeqIO.to_dict(SeqIO.parse('../0_original_deer_data/all_deer_samples_aligned.fasta','fasta'))
calculator = DistanceCalculator('identity')

def get_closest_sequences(this_lineage,this_state,lineage_state_groups,database='gisaid'):
    this_lineage_state=lineage_state_groups[this_lineage, this_state]
    this_state_aligned=SeqIO.to_dict(SeqIO.parse('./fasta_output/'+this_state+'_'+this_lineage+'_'+database+'.txt.fasta', "fasta"))
    tree=ete3.Tree('./fasttree/'+this_state+'_'+this_lineage+'_'+database+'.txt.fasta.tree')
    
    result_list=[]
    for _,row in this_lineage_state.iterrows():
        if len(tree.search_nodes(name=row['taxon']))<1:
            print(row['taxon'])
            continue
        
        node = (tree.search_nodes(name=row['taxon']))[0]
        #print('This node:'+node.name)
        
        
        sequence_list_name={}
        this_branch={}
        find_flag=0
        for ancestors_group in node.get_ancestors():
            for leaf in ancestors_group.get_leaves():
                if ((database=='gisaid') and ('hCoV-19' in leaf.name)) or ((database=='ncbi') and ('human' in leaf.name)):
                    if leaf.name not in list(sequence_list_name.keys()):
                        sequence_list_name[leaf.name]=0
                        find_flag=find_flag+1
                    
            if find_flag>number_wanted:
                break
            else:
                this_branch=sequence_list_name.copy()
                
        result_list.extend(this_branch.keys())
        temp=pd.DataFrame([],columns=['id','distance'])
        outside_branch=list(set(sequence_list_name.keys())-set(this_branch.keys()))
        for seq in outside_branch:
            aln = MultipleSeqAlignment([deer_aligned[row['taxon']],this_state_aligned[seq]])
            dm = calculator.get_distance(aln)
            temp=pd.concat([temp,pd.DataFrame([[seq, dm.matrix[1][0]]], columns=['id','distance'])], axis=0)
        
        temp=temp.sort_values('distance')
        result_list.extend(list(temp.iloc[0:(number_wanted-len(this_branch)),0]))
        
    result_list=list(set(result_list))
    
    
    with open('./fasttree_closest_selected/'+this_state+'_'+this_lineage+'_'+database+'_fasttree.txt', 'w') as f:
        for line in result_list:
            f.write(f"{line}\n") 
    return result_list
    
states=list(deer_samples.groupby('states').groups.keys())
lineages=list(deer_samples.groupby('lineage').groups.keys())

for state in states:
    for lineage in lineages:
        if (lineage, state) in list(lineage_state_groups.keys()):
            get_closest_sequences(lineage,state,lineage_state_groups,'gisaid')
            get_closest_sequences(lineage,state,lineage_state_groups,'ncbi')
