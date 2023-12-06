library(scales)
library(ggplot2)
library(ggtree)
library(phytools)
library(treeio)
library(TreeTools)
library(ape)
library(tidytree)

setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

options(ignore.negative.edge=TRUE)


tree <- read.beast('US_BEAST.trees.output')
#TEST = read.csv('US_BEAST_host.txt',sep = "\t")

host_info = read.csv('US_BEAST_node_number_and_node_label.csv')
host_info =host_info[1:478,c(1,8)]
node_num = read.csv('US_BEAST_node_number_and_cluster_info.csv')
node_num =node_num[,c(1,7)]
#node_num[is.na(node_num)] <- 'black'
host_info$node <- as.character(host_info$node)
node_num$node <- as.character(node_num$node)

tree@data<-full_join(tree@data, host_info, by = 'node')
tree@data<-full_join(tree@data, node_num, by = 'node')


ggtree(tree,mrsd="2022-05-28", aes(color=color),size=0.7) +
  geom_tippoint(aes(color=host))+ theme_tree2()+
  scale_colour_manual(values=c('blue','orange','lime green','medium orchid',"red"),na.value = "black")

ggtree(tree,mrsd="2022-05-28", aes(color=color),size=1) +geom_treescale(x=2022.5,color='white',width=0.6)+
  geom_tiplab(aes(color=host))+ theme_tree2()+
  scale_colour_manual(values=c('blue','orange','lime green','medium orchid',"red"),na.value = "black")+
  theme(legend.position = "none")+
  #geom_text2(color = "orange",aes(subset=!isTip, label=node), hjust=-0.3,size=3)+
  geom_nodelab(color = "Magenta",aes(x=branch, label=round(as.double(posterior),2), subset=posterior>0.69999), vjust=0,hjust=0.5, size=3)

ggsave("C:/Users/af3bd/Downloads/clade__tree.pdf", width = 80, height = 200, units = "cm", limitsize = FALSE)


ggtree(tree,mrsd="2022-05-28",size=1) %<+% TEST+
  geom_tiplab(aes(color=host))+ theme_tree2()+theme(legend.position = "none")+
  geom_text2(color = "orange",aes(subset=isTip, label=node), hjust=-0.3,size=3)+
  geom_nodelab(color = "Magenta",aes(x=branch, label=round(as.double(posterior),2), subset=posterior>0), vjust=0,hjust=0.5, size=3)
