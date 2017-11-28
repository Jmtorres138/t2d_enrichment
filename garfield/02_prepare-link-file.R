"%&%" <- function(a,b) paste0(a,b)

library("tidyverse")

work_dir <- "/well/got2d/jason/projects/t2d_enrichment/garfield/"
input_dir <- "/well/got2d/jason/projects/t2d_enrichment/fgwas/fgwas_input/"
input_file <- input_dir %&% "ukbb_diamante-euro.fgwas.gz"

annot_dir <- work_dir %&% "annotation/"

con <- file(input_file,"r")
first_line <- readLines(con,n=1)
close(con)

annot.vec <- strsplit(first_line,split="\t")[[1]]
annot.vec <- annot.vec[10:(length(annot.vec)-1)] # remove gwas columns and distance_tss (very last one)

Index <- 0:(length(annot.vec)-1)
Annotation <- annot.vec
Celltype <- map(Annotation,function(annot){
  if(grepl("varshney",annot)==TRUE){
    val <- strsplit(annot,split="_")[[1]][2]
  } else if(grepl("DOR",annot)==TRUE){
    val <- strsplit(annot,split="_")[[1]][1]
  } else if(grepl("islet_",annot)==TRUE){
    val <- "islet"
  } else if(grepl("ES_D",annot)==TRUE){
    val <- strsplit(annot,"_")[[1]][4]
  } else{
    val <- "genomic"
  }
}) %>% as.character(.)

Tissue <- Celltype

Type <- map(Annotation,function(annot){
  if(grepl("varshney",annot)==TRUE){
    val <- "chromatin_state"
  } else if(grepl("DOR",annot)==TRUE){
    val <- "islet_diff_open_region"
  } else if(grepl("_atac_chromstate",annot)==TRUE){
    val <- "chromatin_state"
  } else if(grepl("_atac",annot)==TRUE){
    val <- "ATAC"
  } else if(grepl("islet_",annot)==TRUE){
    val <- "chromatin_state"
  } else if(grepl("ES_D",annot)==TRUE){
    val <- strsplit(annot,"_")[[1]][3]
  } else{
    val <- "genomic"
  }
}) %>% as.character(.)

Category <- Type

out.df <- data.frame(Index,Annotation,Celltype,
                     Tissue,Type,Category,stringsAsFactors=FALSE)
name.vec <- c("Index","Annotation","Celltype","Tissue","Type","Category")

names(out.df) <- name.vec

write.table(out.df,file=annot_dir%&%"link_file.txt",sep=" ",quote=F,row.names=F)
