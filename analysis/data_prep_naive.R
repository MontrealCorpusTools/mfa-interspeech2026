
root_dir = "D:/Data/experiments/interspeech_benchmarking/naive_evaluation_data"

naive_data = data.frame()
precision_boundary_data = data.frame()
recall_boundary_data = data.frame()

corpora = list.dirs(root_dir, recursive = F, full.names = F)
for (c in corpora){
  evals = list.dirs(file.path(root_dir, c), recursive = F, full.names = F)
  
  for (e in evals){
    
    print(e)
    path = file.path(root_dir, c, e, "alignment_reference_evaluation.csv")
    if (!file.exists(path)){
      next
    }
    print(path)
    d = read_csv(path, show_col_types = F, lazy=F)
    d$utterance <- paste(d$file, str_replace_all(as.character(d$begin), '\\.', '-'), str_replace_all(as.character(d$end), '\\.', '-'), sep="-")
    d$evaluation = e
    d$corpus = c
    d$precision = as.numeric(d$precision)
    d$recall = as.numeric(d$recall)
    d$f1 = as.numeric(d$f1)
    naive_data = bind_rows(naive_data,d)
    
    path = file.path(root_dir, c, e, "alignment_reference_precision_evaluation_boundaries.csv")
    if (!file.exists(path)){
      next
    }
    print(path)
    d = read_csv(path, show_col_types = F, lazy=F)
    d$utterance <- paste(d$file, str_replace_all(as.character(d$utterance_begin), '\\.', '-'), str_replace_all(as.character(d$utterance_end), '\\.', '-'), sep="-")
    d$evaluation = e
    d$corpus = c
    precision_boundary_data = bind_rows(precision_boundary_data,d)
    
    path = file.path(root_dir, c, e, "alignment_reference_recall_evaluation_boundaries.csv")
    if (!file.exists(path)){
      next
    }
    print(path)
    d = read_csv(path, show_col_types = F, lazy=F)
    d$utterance <- paste(d$file, str_replace_all(as.character(d$utterance_begin), '\\.', '-'), str_replace_all(as.character(d$utterance_end), '\\.', '-'), sep="-")
    d$evaluation = e
    d$corpus = c
    recall_boundary_data = bind_rows(recall_boundary_data,d)
  }
}

naive_data$evaluation = factor(naive_data$evaluation)
naive_data$corpus = factor(naive_data$corpus)

precision_boundary_data$evaluation = factor(precision_boundary_data$evaluation)
precision_boundary_data$corpus = factor(precision_boundary_data$corpus)
precision_boundary_data$abs_boundary_error = abs(precision_boundary_data$boundary_error)

recall_boundary_data$evaluation = factor(recall_boundary_data$evaluation)
recall_boundary_data$corpus = factor(recall_boundary_data$corpus)
recall_boundary_data$abs_boundary_error = abs(recall_boundary_data$boundary_error)

naive_data <- subset(naive_data, !evaluation %in% c("mfa_3.1", "arpa_3.0"))
naive_data[naive_data$evaluation=="mfa_3.1_adapted",]$evaluation <- "mfa_3.1"
naive_data[naive_data$evaluation=="arpa_3.0_adapted",]$evaluation <- "arpa_3.0"
naive_data$evaluation = factor(naive_data$evaluation)

precision_boundary_data <- subset(precision_boundary_data, !evaluation %in% c("mfa_3.1", "arpa_3.0"))
precision_boundary_data[precision_boundary_data$evaluation=="mfa_3.1_adapted",]$evaluation <- "mfa_3.1"
precision_boundary_data[precision_boundary_data$evaluation=="arpa_3.0_adapted",]$evaluation <- "arpa_3.0"
precision_boundary_data$evaluation = factor(precision_boundary_data$evaluation)

recall_boundary_data <- subset(recall_boundary_data, !evaluation %in% c("mfa_3.1", "arpa_3.0"))
recall_boundary_data[recall_boundary_data$evaluation=="mfa_3.1_adapted",]$evaluation <- "mfa_3.1"
recall_boundary_data[recall_boundary_data$evaluation=="arpa_3.0_adapted",]$evaluation <- "arpa_3.0"
recall_boundary_data$evaluation = factor(recall_boundary_data$evaluation)

precision_table <- precision_boundary_data %>% mutate(thresh_10ms=abs_boundary_error *1000 <= 10, thresh_20ms=abs_boundary_error *1000 <= 20, thresh_50ms=abs_boundary_error *1000 <= 50, thresh_100ms=abs_boundary_error *1000 <= 100) %>% group_by(corpus, evaluation) %>% summarise(mean_error=round(mean(abs_boundary_error *1000),2), thresh_10ms=round(mean(thresh_10ms) *100,2), thresh_20ms=round(mean(thresh_20ms) *100,2), thresh_50ms=round(mean(thresh_50ms) *100,2), thresh_100ms=round(mean(thresh_100ms) *100,2), n()) 

recall_table <- recall_boundary_data %>% mutate(thresh_10ms=abs_boundary_error *1000 <= 10, thresh_20ms=abs_boundary_error *1000 <= 20, thresh_50ms=abs_boundary_error *1000 <= 50, thresh_100ms=abs_boundary_error *1000 <= 100) %>% group_by(corpus, evaluation) %>% summarise(mean_error=round(mean(abs_boundary_error *1000),2), thresh_10ms=round(mean(thresh_10ms) *100,2), thresh_20ms=round(mean(thresh_20ms) *100,2), thresh_50ms=round(mean(thresh_50ms) *100,2), thresh_100ms=round(mean(thresh_100ms) *100,2), n()) 

f1_table = recall_table %>% add_column(precision_thresh_20ms=precision_table$thresh_20ms) %>% mutate(f1_20ms=round(2* (thresh_20ms * precision_thresh_20ms)/ (thresh_20ms + precision_thresh_20ms), 2))


