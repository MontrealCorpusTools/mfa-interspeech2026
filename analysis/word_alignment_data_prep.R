library(tidyr)
library(dplyr)
library(readr)
library(stringr)
root_dir = "D:/Data/experiments/interspeech_benchmarking/word_alignments/alignments"

word_boundary_data = data.frame()

corpora = list.dirs(root_dir, recursive = F, full.names = F)
for (c in corpora){
  evals = list.dirs(file.path(root_dir, c), recursive = F, full.names = F)
  
  for (e in evals){
    
    print(e)
  
    path = file.path(root_dir, c, e, "word_alignment_boundaries.csv")
    if (!file.exists(path)){
      next
    }
    print(path)
    d = read_csv(path, show_col_types = F, lazy=F)
    d$evaluation = e
    d$corpus = c
    word_boundary_data = bind_rows(word_boundary_data,d)
  }
}

word_boundary_data$evaluation = factor(word_boundary_data$evaluation)
word_boundary_data$corpus = factor(word_boundary_data$corpus)
word_boundary_data$abs_boundary_error = abs(word_boundary_data$boundary_error)

word_boundary_data <- subset(word_boundary_data, !evaluation %in% c("mfa_3.1", "arpa_3.0"))
word_boundary_data[word_boundary_data$evaluation=="mfa_3.1_adapted",]$evaluation <- "mfa_3.1"
word_boundary_data[word_boundary_data$evaluation=="arpa_3.0_adapted",]$evaluation <- "arpa_3.0"
word_boundary_data$evaluation = factor(word_boundary_data$evaluation)


word_threshold_table = word_boundary_data %>% mutate(thresh_10ms=abs_boundary_error *1000 <= 10, thresh_20ms=abs_boundary_error *1000 <= 20, thresh_50ms=abs_boundary_error *1000 <= 50, thresh_100ms=abs_boundary_error *1000 <= 100) %>% group_by(corpus, evaluation) %>% summarise(mean_error=mean(abs_boundary_error *1000), median_error=median(abs_boundary_error *1000), thresh_10ms=mean(thresh_10ms) * 100, thresh_20ms=mean(thresh_20ms) * 100, thresh_50ms=mean(thresh_50ms) * 100, thresh_100ms=mean(thresh_100ms) * 100) 
