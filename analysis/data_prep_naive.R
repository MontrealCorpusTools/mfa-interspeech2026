
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



precision_boundary_data$previous_test_category <- "unknown"
precision_boundary_data$following_test_category <- "unknown"

for (n in names(test_phone_lists)) {
  for (category in names(test_phone_lists[[n]])){
    precision_boundary_data[precision_boundary_data$previous_test_phone %in% test_phone_lists[[n]][[category]] & str_detect(precision_boundary_data$evaluation, n),]$previous_test_category = category
    precision_boundary_data[precision_boundary_data$following_test_phone %in% test_phone_lists[[n]][[category]] & str_detect(precision_boundary_data$evaluation, n),]$following_test_category = category
  }
}
precision_boundary_data[precision_boundary_data$previous_test_phone %in% c( "ɾ","ɾʲ", "4") & precision_boundary_data$corpus %in% c('timit', 'buckeye'),]$previous_test_category = 'stop'
precision_boundary_data[precision_boundary_data$following_test_phone %in% c( "ɾ","ɾʲ", "4") & precision_boundary_data$corpus %in% c('timit', 'buckeye'),]$following_test_category = 'stop'


precision_boundary_data$previous_reference_category <- "unknown"
precision_boundary_data$following_reference_category <- "unknown"

for (n in names(reference_phone_lists)) {
  for (category in names(reference_phone_lists[[n]])){
    precision_boundary_data[precision_boundary_data$previous_reference_phone %in% reference_phone_lists[[n]][[category]] & precision_boundary_data$corpus == n,]$previous_reference_category = category
    precision_boundary_data[precision_boundary_data$following_reference_phone %in% reference_phone_lists[[n]][[category]] & precision_boundary_data$corpus == n,]$following_reference_category = category
  }
}

precision_boundary_data[precision_boundary_data$previous_test_phone %in% c( "ER0", "ER1", 'ER2', 'R', "3:", "3`", "3:r","r\\") & precision_boundary_data$previous_reference_phone %in% c( "axr","r", "er")& precision_boundary_data$corpus %in% c('timit', 'buckeye'),]$previous_test_category = precision_boundary_data[precision_boundary_data$previous_test_phone %in% c( "ER0", "ER1", 'ER2', 'R', "3:", "3`", "3:r","r\\") & precision_boundary_data$previous_reference_phone %in% c( "axr","r", "er")& precision_boundary_data$corpus %in% c('timit', 'buckeye'),]$previous_reference_category

precision_boundary_data[precision_boundary_data$following_test_phone %in% c( "ER0", "ER1", 'ER2', 'R', "3:", "3`", "3:r","r\\") & precision_boundary_data$following_reference_phone %in% c( "axr","r", "er")& precision_boundary_data$corpus %in% c('timit', 'buckeye'),]$following_test_category = precision_boundary_data[precision_boundary_data$following_test_phone %in% c( "ER0", "ER1", 'ER2', 'R', "3:", "3`", "3:r","r\\") & precision_boundary_data$following_reference_phone %in% c( "axr","r", "er")& precision_boundary_data$corpus %in% c('timit', 'buckeye'),]$following_reference_category


recall_boundary_data$previous_test_category <- "unknown"
recall_boundary_data$following_test_category <- "unknown"

for (n in names(test_phone_lists)) {
  for (category in names(test_phone_lists[[n]])){
    recall_boundary_data[recall_boundary_data$previous_test_phone %in% test_phone_lists[[n]][[category]] & str_detect(recall_boundary_data$evaluation, n),]$previous_test_category = category
    recall_boundary_data[recall_boundary_data$following_test_phone %in% test_phone_lists[[n]][[category]] & str_detect(recall_boundary_data$evaluation, n),]$following_test_category = category
  }
}
recall_boundary_data[recall_boundary_data$previous_test_phone %in% c( "ɾ","ɾʲ", "4") & recall_boundary_data$corpus %in% c('timit', 'buckeye'),]$previous_test_category = 'stop'
recall_boundary_data[recall_boundary_data$following_test_phone %in% c( "ɾ","ɾʲ", "4") & recall_boundary_data$corpus %in% c('timit', 'buckeye'),]$following_test_category = 'stop'


recall_boundary_data$previous_reference_category <- "unknown"
recall_boundary_data$following_reference_category <- "unknown"

for (n in names(reference_phone_lists)) {
  for (category in names(reference_phone_lists[[n]])){
    recall_boundary_data[recall_boundary_data$previous_reference_phone %in% reference_phone_lists[[n]][[category]] & recall_boundary_data$corpus == n,]$previous_reference_category = category
    recall_boundary_data[recall_boundary_data$following_reference_phone %in% reference_phone_lists[[n]][[category]] & recall_boundary_data$corpus == n,]$following_reference_category = category
  }
}

boundary_data[boundary_data$previous_test_phone %in% c( "ER0", "ER1", 'ER2', 'R', "3:", "3`", "3:r","r\\") & boundary_data$previous_reference_phone %in% c( "axr","r", "er")& boundary_data$corpus %in% c('timit', 'buckeye'),]$previous_test_category = boundary_data[boundary_data$previous_test_phone %in% c( "ER0", "ER1", 'ER2', 'R', "3:", "3`", "3:r","r\\") & boundary_data$previous_reference_phone %in% c( "axr","r", "er")& boundary_data$corpus %in% c('timit', 'buckeye'),]$previous_reference_category

boundary_data[boundary_data$following_test_phone %in% c( "ER0", "ER1", 'ER2', 'R', "3:", "3`", "3:r","r\\") & boundary_data$following_reference_phone %in% c( "axr","r", "er")& boundary_data$corpus %in% c('timit', 'buckeye'),]$following_test_category = boundary_data[boundary_data$following_test_phone %in% c( "ER0", "ER1", 'ER2', 'R', "3:", "3`", "3:r","r\\") & boundary_data$following_reference_phone %in% c( "axr","r", "er")& boundary_data$corpus %in% c('timit', 'buckeye'),]$following_reference_category



precision_table <- precision_boundary_data %>% mutate(thresh_10ms=abs_boundary_error *1000 <= 10, thresh_20ms=abs_boundary_error *1000 <= 20, thresh_50ms=abs_boundary_error *1000 <= 50, thresh_100ms=abs_boundary_error *1000 <= 100) %>% group_by(corpus, evaluation) %>% summarise(mean_error=round(mean(abs_boundary_error *1000),2), thresh_10ms=round(mean(thresh_10ms) *100,2), thresh_20ms=round(mean(thresh_20ms) *100,2), thresh_50ms=round(mean(thresh_50ms) *100,2), thresh_100ms=round(mean(thresh_100ms) *100,2), n()) 

recall_table <- recall_boundary_data %>% mutate(thresh_10ms=abs_boundary_error *1000 <= 10, thresh_20ms=abs_boundary_error *1000 <= 20, thresh_50ms=abs_boundary_error *1000 <= 50, thresh_100ms=abs_boundary_error *1000 <= 100) %>% group_by(corpus, evaluation) %>% summarise(mean_error=round(mean(abs_boundary_error *1000),2), thresh_10ms=round(mean(thresh_10ms) *100,2), thresh_20ms=round(mean(thresh_20ms) *100,2), thresh_50ms=round(mean(thresh_50ms) *100,2), thresh_100ms=round(mean(thresh_100ms) *100,2), n()) 

f1_table = recall_table %>% add_column(precision_thresh_20ms=precision_table$thresh_20ms) %>% mutate(f1_20ms=round(2* (thresh_20ms * precision_thresh_20ms)/ (thresh_20ms + precision_thresh_20ms), 2))


filtered_precision_boundary_data = precision_boundary_data %>% subset(previous_reference_category == previous_test_category & following_reference_category == following_test_category & following_test_category != 'unknown' & following_reference_category != 'unknown' & previous_test_category != "unknown" & previous_reference_category != "unknown")

filtered_recall_boundary_data = recall_boundary_data %>% subset(previous_reference_category == previous_test_category & following_reference_category == following_test_category & following_test_category != 'unknown' & following_reference_category != 'unknown' & previous_test_category != "unknown" & previous_reference_category != "unknown")



precision_table_filtered <- filtered_precision_boundary_data %>% mutate(thresh_10ms=abs_boundary_error *1000 <= 10, thresh_20ms=abs_boundary_error *1000 <= 20, thresh_50ms=abs_boundary_error *1000 <= 50, thresh_100ms=abs_boundary_error *1000 <= 100) %>% group_by(corpus, evaluation) %>% summarise(mean_error=round(mean(abs_boundary_error *1000),2), thresh_10ms=round(mean(thresh_10ms) *100,2), thresh_20ms=round(mean(thresh_20ms) *100,2), thresh_50ms=round(mean(thresh_50ms) *100,2), thresh_100ms=round(mean(thresh_100ms) *100,2), n()) 

recall_table_filtered <- filtered_recall_boundary_data %>% mutate(thresh_10ms=abs_boundary_error *1000 <= 10, thresh_20ms=abs_boundary_error *1000 <= 20, thresh_50ms=abs_boundary_error *1000 <= 50, thresh_100ms=abs_boundary_error *1000 <= 100) %>% group_by(corpus, evaluation) %>% summarise(mean_error=round(mean(abs_boundary_error *1000),2), thresh_10ms=round(mean(thresh_10ms) *100,2), thresh_20ms=round(mean(thresh_20ms) *100,2), thresh_50ms=round(mean(thresh_50ms) *100,2), thresh_100ms=round(mean(thresh_100ms) *100,2), n()) 

f1_table_filtered = recall_table_filtered %>% add_column(precision_thresh_20ms=precision_table_filtered$thresh_20ms) %>% mutate(f1_20ms=round(2* (thresh_20ms * precision_thresh_20ms)/ (thresh_20ms + precision_thresh_20ms), 2))

recall_boundary_data %>% subset(corpus=='timit' & evaluation != 'bournemouth') %>% mutate(filtered = previous_reference_category != previous_test_category | following_reference_category != following_test_category | following_test_category == 'unknown' | following_reference_category == 'unknown' | previous_test_category == "unknown" | previous_reference_category == "unknown") %>% group_by(evaluation,file) %>% summarise(n_filtered=sum(filtered)) %>% pivot_wider(names_from=evaluation, values_from=n_filtered, names_prefix="n_filtered_") %>% arrange(desc(n_filtered_maus))

View(subset(recall_boundary_data, file == 'DR6_MSDS0_SI1077' & evaluation == 'maus') %>% mutate(filtered = previous_reference_category != previous_test_category | following_reference_category != following_test_category | following_test_category == 'unknown' | following_reference_category == 'unknown' | previous_test_category == "unknown" | previous_reference_category == "unknown"))


View(boundary_data %>% subset(evaluation == 'maus' & corpus =='timit') %>% group_by(previous_reference_phone, following_reference_phone) %>% summarise(mean_error=mean(abs_boundary_error),count=n()) %>% arrange(desc(count)))
View(boundary_data %>% subset(evaluation == 'mfa_3.1' & corpus =='timit') %>% group_by(previous_reference_phone, following_reference_phone) %>% summarise(mean_error=mean(abs_boundary_error),count=n()) %>% arrange(desc(count)))

View(filtered_boundary_data %>% subset(evaluation == 'maus' & corpus =='timit') %>% group_by(previous_reference_phone) %>% summarise(mean_error=mean(abs_boundary_error),count=n()) %>% arrange(desc(count)))

View(filtered_boundary_data %>% subset(evaluation == 'arpa_3.0' & corpus =='timit') %>% group_by(previous_reference_phone) %>% summarise(mean_error=mean(abs_boundary_error),count=n()) %>% arrange(desc(count)))
