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


word_threshold_table = word_boundary_data %>% mutate(thresh_10ms=abs_boundary_error *1000 <= 10, thresh_20ms=abs_boundary_error *1000 <= 20, thresh_50ms=abs_boundary_error *1000 <= 50, thresh_100ms=abs_boundary_error *1000 <= 100) %>% group_by(corpus, evaluation) %>% summarise(mean_error=round(mean(abs_boundary_error *1000),2), thresh_10ms=round(mean(thresh_10ms) * 100,2), thresh_20ms=round(mean(thresh_20ms) * 100,2), thresh_50ms=round(mean(thresh_50ms) * 100,2), thresh_100ms=round(mean(thresh_100ms) * 100,2)) 

# For interspeech presentation

plotData <- summarySE(data=subset(word_boundary_data, evaluation %in% c("arpa_1.0", "arpa_3.0", "nemo", "w2v2", "whisperx")), measurevar = 'abs_boundary_error', groupvars=c("evaluation", "corpus"))

plotData$evaluation = factor(plotData$evaluation, levels = c("arpa_3.0", "arpa_1.0", "w2v2", "whisperx", "nemo"), labels= c("MFA 3.0", "MFA 1.0", "Wav2Vec2*", "WhisperX*", "NeMo*"))
plotData$corpus = factor(plotData$corpus, levels= c("timit", "buckeye"), labels=c("TIMIT", "Buckeye"))

ggplot(aes(x=evaluation, y=mean * 1000, color=corpus), data=plotData) + geom_point(size = 3) +
  geom_errorbar(aes(ymin = (mean - ci) * 1000, ymax = (mean + ci)* 1000),size=1, width=0.25) +
  ylab('Word boundary error (ms)') + xlab('Aligner') +ggtitle('Word boundary errors in English') +
  theme_minimal(base_size = 16) +
  theme(
    panel.grid.minor = element_blank(), 
    panel.border = element_rect(color = "grey40", fill = NA)
  ) +
  ggokabeito::scale_color_okabe_ito(name="Corpus")
#scale_color_manual(values=cbbPalette, name="Corpus")

ggsave("output/interspeech_word_boundaries.png", width=13.33, height=7.5, dpi=600)
