library(ggtree)
library(ggplot2)
library(readxl)
library(phytools)
library(treeio)
library(ape)
library(tibble)
library(pheatmap)
library(dplyr)
library(tidyverse)

library(outbreakinfo)
outbreakinfo::authenticateUser()

setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

for (this_gene in c('S','ORF1a','ORF1b','ORF3a','ORF6','ORF7a','ORF7b','ORF8','N','ORF9b','E','M')){
  if (length(readLines(paste0('./mutation_tables/',"aaSubstitutions_",this_gene,".csv")))<2) {next}
  df<-read.csv(paste0('./mutation_tables/',"aaSubstitutions_",this_gene,".csv"))

df2 <- df

for (i in 2:ncol(df2)){
  output = getPrevalence(mutations = paste0(this_gene,':',colnames(df2)[i]), cumulative = T,location='United States')
  colnames(df2)[i] <- paste0(colnames(df2)[i],'_',round(output$value.global_prevalence,2),'_',output$value.lineage_count)
}


#rownames(df2)<-df$X

write.csv(df2,paste0('./mutation_tables/',"aaSubstitutions_",this_gene,"_outbreak.csv"), row.names = FALSE)

}


