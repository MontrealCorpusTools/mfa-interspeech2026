

#category_boundary_data <- subset(boundary_data, following_reference_category == following_test_category & previous_reference_category == previous_test_category)

#t <- subset(boundary_data, previous_reference_category != previous_test_category)

data <- subset(data, !is.na(data$alignment_score))

plotData <- summarySE(data=data, measurevar = 'edit_distance', groupvars=c("evaluation"))

ggplot(aes(x=evaluation, y=mean * 1000, color=evaluation), data=plotData) + geom_point(size = 5) +
  geom_errorbar(aes(ymin = (mean - ci) * 1000, ymax = (mean + ci)* 1000),size=2, width=0.5) +
  ylab('Phone boundary error (ms)') + xlab('Data subset') +ggtitle('Phone boundary errors') +
  theme_memcauliffe() +
  scale_x_discrete(guide = guide_axis(n.dodge = 2)) #+ scale_color_manual(values=cbbPalette)

plotData <- summarySE(data=filtered_data, measurevar = 'alignment_score', groupvars=c("evaluation", "corpus"))

ggplot(aes(x=evaluation, y=mean * 1000, color=evaluation), data=plotData) + geom_point(size = 5) +
  geom_errorbar(aes(ymin = (mean - ci) * 1000, ymax = (mean + ci)* 1000),size=2, width=0.5) +
  ylab('Phone boundary error (ms)') + xlab('Data subset') +ggtitle('Phone boundary errors') +
  theme_memcauliffe() +
  scale_x_discrete(guide = guide_axis(n.dodge = 2))+ facet_wrap(~corpus, scales='free_x') #+ scale_color_manual(values=cbbPalette)

plotData <- summarySE(data=filtered_boundary_data, measurevar = 'abs_boundary_error', groupvars=c("evaluation", "corpus"))

ggplot(aes(x=evaluation, y=mean * 1000), data=plotData) + geom_point(size = 5, color='#FB5607') +
  geom_errorbar(aes(ymin = (mean - ci) * 1000, ymax = (mean + ci)* 1000),size=2, width=0.5, color='#FB5607') +
  ylab('Phone boundary error (ms)') + xlab('Aligner') +ggtitle('Phone boundary errors') +
  theme_memcauliffe() +
  scale_x_discrete(guide = guide_axis(n.dodge = 2))+ facet_wrap(~corpus, scales='free_x') #+ scale_color_manual(values=cbbPalette) 

ggsave("output/utterance_boundary_agreement.png", width=1400, height=800, units="px", dpi=200)


plotData <- summarySE(data=boundary_data, measurevar = 'abs_boundary_error', groupvars=c("evaluation"))

ggplot(aes(x=following_reference_category, y=previous_reference_category, fill=mean * 1000), data=plotData) + geom_tile()+
  ylab('First segment') + xlab('Following segment') +
  theme_memcauliffe() + scale_fill_gradient(high='#FB5607', low="#003566", name="Abs error") +
  scale_x_discrete(guide = guide_axis(n.dodge = 2)) +ggtitle(paste("Mean boundary error for", ds, sep=" ")) +facet_wrap(~mfa_model)

ggsave(paste("output/", ds, "_phone_category_agreement.png", sep=""), width=2000, height=800, units="px", dpi=200)


# Benchmark other aligners

for (ds in levels(filtered_boundary_data$corpus)) {
  d = subset(filtered_boundary_data, corpus == ds & evaluation %in% c("bournemouth", "gp_1.0", "koreanforcedaligner", "mfa_3.1", "arpa_1.0", "arpa_3.0", "maps", "maus", "sppas", "charsiu", "julius"))
  plotData <- summarySE(data=d, measurevar = 'abs_boundary_error', groupvars=c("evaluation"))
  plotData$evaluation = factor(plotData$evaluation, levels = c("gp_1.0", "arpa_1.0", "maus", "sppas", "maps", "charsiu", "julius", "koreanforcedaligner", "bournemouth", "mfa_3.1", "arpa_3.0"), labels=c("MFA 1.0", "MFA 1.0", "MAUS", "SPPAS", "MAPS*", "Charsiu*", "Julius", "KFA", "BFA*", "MFA 3.0", "ARPA 3.0"))
  
  ggplot(aes(x=evaluation, y=mean * 1000), data=plotData) + geom_point(size = 4, color='#FB5607') +
    ylab('Phone boundary error (ms)') + xlab('Aligner') +ggtitle('Phone boundary errors') +
    theme_memcauliffe()
  
  ggsave(paste("output/", ds, "_phone_boundary_errors.png", sep=""), width=1500, height=800, units="px", dpi=200)
}

# Benchmark MFA adaptation


plotData <- summarySE(data=subset(filtered_boundary_data, evaluation %in% c("arpa_3.0", "arpa_3.0_adapted", "mfa_3.1", "mfa_3.1_adapted", "mfa_remapped", "mfa_remapped_adapted")), measurevar = 'abs_boundary_error', groupvars=c("evaluation", "corpus"))
plotData$corpus = factor(plotData$corpus, levels = c('timit', 'buckeye', 'csj', 'seoul_corpus'), labels=c('TIMIT', "Buckeye", "CSJ", "Seoul"))
plotData$adapted = "No"
plotData[str_detect(plotData$evaluation, "_adapted"),]$adapted = "Yes"
plotData$evaluation = factor(plotData$evaluation, levels = c("arpa_3.0", "arpa_3.0_adapted", "mfa_3.1", "mfa_3.1_adapted", "mfa_remapped", "mfa_remapped_adapted"), labels=c("ARPA", "ARPA", "MFA", "MFA", "Remapped", "Remapped"))

ggplot(aes(x=corpus, y=mean * 1000, color=evaluation, shape=adapted), data=plotData) + geom_point(size = 4) +
  ylab('Phone boundary error (ms)') + xlab('Corpus') +ggtitle('Phone boundary errors')  + scale_color_manual(values=cbbPalette,name="Phone set") + scale_shape_discrete(name="Adapted") +
  theme_memcauliffe()
ggsave("output/adaptation_phone_boundary_errors.png", width=1500, height=800, units="px", dpi=200)

# Benchmark MFA training


plotData <- summarySE(data=subset(filtered_boundary_data, evaluation %in% c("mfa_3.1", "mfa_trained", "mfa_trained_no_pronunciation_probability", "mfa_trained_rules")), measurevar = 'abs_boundary_error', groupvars=c("evaluation", "corpus"))
plotData$corpus = factor(plotData$corpus, levels = c('timit', 'buckeye', 'csj', 'seoul_corpus'), labels=c('TIMIT', "Buckeye", "CSJ", "Seoul"))
plotData$training = "Base"
plotData[str_detect(plotData$evaluation, "_no_pronunciation_probability"),]$training = "-PP"
plotData[str_detect(plotData$evaluation, "_rules"),]$training = "+Rules"
plotData$training = factor(plotData$training, levels=c("Base", "-PP", "+Rules"))
plotData$evaluation_type = "Pretrained"
plotData[str_detect(plotData$evaluation, "_trained"),]$evaluation_type = "Trained"

ggplot(aes(x=corpus, y=mean * 1000, color=evaluation_type, shape=training), data=plotData) + geom_point(size = 4) +
  ylab('Phone boundary error (ms)') + xlab('Corpus') +ggtitle('Phone boundary errors')  + scale_color_manual(values=cbbPalette,name="Evaluation") +scale_shape_discrete(name='Training') +
  theme_memcauliffe()
ggsave("output/training_phone_boundary_errors.png", width=1500, height=800, units="px", dpi=200)



# Word plots

plotData <- summarySE(data=subset(word_boundary_data, evaluation %in% c("arpa_1.0", "arpa_3.0", "whisperx", "w2v2", "nemo")), measurevar = 'abs_boundary_error', groupvars=c("evaluation", "corpus"))
plotData$corpus = factor(plotData$corpus, levels = c('timit', 'buckeye'), labels=c('TIMIT', "Buckeye"))
plotData$evaluation = factor(plotData$evaluation, levels = c( "arpa_1.0", "arpa_3.0", "w2v2", "whisperx", "nemo"), labels=c("MFA 1.0", "MFA 3.0", "Wav2Vec2.0", "WhisperX", "NFA"))

ggplot(aes(x=evaluation, y=mean * 1000, color=corpus), data=plotData) + geom_point(size = 4) +
  ylab('Word boundary error (ms)') + xlab('Aligner') +ggtitle('Word boundary errors') +
  theme_memcauliffe()  + scale_color_manual(values=cbbPalette,name="Corpus")
ggsave("output/word_boundary_errors.png", width=1500, height=800, units="px", dpi=200)
