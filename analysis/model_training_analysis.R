
model_data_dir = "D:/Data/experiments/interspeech_benchmarking/model_training_analysis"

languages = list.files(model_data_dir, recursive = F, full.names = F)

model_data = data.frame()

for (l in languages){
  print(l)
  path = file.path(model_data_dir, l)
  print(path)
  if (!file.exists(path)){
    next
  }
  d = read_csv(path, show_col_types = F, lazy=F)
  d$language = l
  model_data = bind_rows(model_data,d)
}

summary(model_data)

model_data$corpus = factor(model_data$corpus)
model_data$file_format = factor(model_data$file_format)

median_dates = model_data %>% group_by(corpus) %>% summarise(minimum_date=min(modified_date), median_date=median(modified_date), max(modified_date)) 

model_data$modified = F

for (c in levels(model_data$corpus)){
  min_date = median_dates[median_dates$corpus==c,]$median_date
  if (nrow(model_data[model_data$corpus==c & model_data$modified_date > min_date,])>0){
    model_data[model_data$corpus==c & model_data$modified_date > min_date,]$modified = T
    
  }
}

modified_data <- model_data %>% group_by(language,corpus) %>% summarise(manual_count = sum(manual_alignments), modified_count=sum(modified), textgrid_count=sum(file_format=='TextGrid'), total=n())

use_textgrid_corpora = c("common_voice", "snemovna", "czech_parliament")

for (c in use_textgrid_corpora){
  modified_data[str_detect(modified_data$corpus, c),]$modified_count = modified_data[str_detect(modified_data$corpus, c),]$textgrid_count
}

modified_data %>% mutate(modified_percent = round((modified_count/total)*100, 2))
modified_data %>% group_by(language) %>% summarise(modified_count=sum(modified_count), total=sum(total)) %>% mutate(modified_percent = round((modified_count/total)*100, 2))

