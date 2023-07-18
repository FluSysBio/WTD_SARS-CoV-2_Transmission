[![DOI](https://zenodo.org/badge/642095603.svg)](https://zenodo.org/badge/latestdoi/642095603)
# WTD_SARS-CoV-2_Transmission

This is the code related to our paper 'Transmission of SARS-CoV-2 in free-ranging white-tailed deer in the United States' authored by Aijing Feng, Sarah Bevins, Jeff Chandler, Thomas J. DeLiberto, Ria Ghai, Kristina Lantz, Julianna Lenoch, Adam Retchless, Susan Shriner, Cynthia Y. Tang, Suxiang Sue Tong, Mia Torchetti, Anna Uehara, Xiu-Feng Wan.

Cite this article

Feng, A., Bevins, S., Chandler, J. et al. Transmission of SARS-CoV-2 in free-ranging white-tailed deer in the United States. Nat Commun 14, 4078 (2023). https://doi.org/10.1038/s41467-023-39782-x

## Abstract
SARS-CoV-2 is a zoonotic virus with documented bi-directional transmission between people and animals. Transmission of SARS-CoV-2 from humans to free-ranging white-tailed deer (Odocoileus virginianus) poses a unique public health risk due to the potential for reservoir establishment where variants may persist and evolve. We collected 8,830 respiratory samples from free-ranging white-tailed deer across Washington, D.C. and 26 states in the United States between November 2021 and April 2022. We obtained 391 sequences and identified 34 Pango lineages including the Alpha, Gamma, Delta, and Omicron variants. Evolutionary analyses showed these white-tailed deer viruses originated from at least 109 independent spillovers from humans, which resulted in 39 cases of subsequent local deer-to-deer transmission and three cases of potential spillover from white-tailed deer back to humans. Viruses repeatedly adapted to white-tailed deer with recurring amino acid substitutions across spike and other proteins. Overall, our findings suggest that multiple SARS-CoV-2 lineages were introduced, became enzootic, and co-circulated in white-tailed deer.

## Dataset
### WTD data collected in this study
From November 4, 2021 to April 4, 2022, a total of 8,830 WTD nasal swab samples were collected from Washington, D.C. and 26 participating states either by hunter- or agency-harvest. None of the animals sampled exhibited clinical signs of SARS-CoV-2 infection. Over 95% of the WTD population resides in the Northeast, Midwest, and Southeastern United States, represented by Washington, D.C. and 26 states from which the samples were collected. These regions are also where much of the 6 million WTD are harvested annually by hunters. In the vast majority of cases, a paired blood sample was collected onto a Nobuto filter strip for serological analysis.

### Public dataset
All available SARS-CoV-2 genomic sequences (n = 11,778,398 by 2022/07/09) from humans were downloaded from GISAID, and additional genomes (n = 1,020,486 by 2022/04/07) were curated from GenBank. From these sequences, human SARS-CoV sequences were selected from the 23 states where we sampled the WTD sequences. After removing redundant entries and selecting the complete and high coverage sequences, a total of 717,717 SARS-CoV-2 genomic sequences were obtained for this study.  In addition, on December 5, 2022, we downloaded a total of 332 WTD SARS-CoV-2 genomes from GISAID. 

## Dependencies
### Python Dependencies
Data processing code is developed and tested under Python 3.8.x. The main dependent packages and their versions are as follows.

    pandas==1.2.4
    biopython==1.79
    ete3==3.1.2
    
### R Dependencies
    outbreakinfo==0.2.0
    
