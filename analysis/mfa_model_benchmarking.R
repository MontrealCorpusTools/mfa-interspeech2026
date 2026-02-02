

#category_boundary_data <- subset(boundary_data, following_reference_category == following_test_category & previous_reference_category == previous_test_category)

#t <- subset(boundary_data, previous_reference_category != previous_test_category)
mfa3_data$evaluation <- factor(mfa3_data$evaluation)
mfa3_data$phoneset <- "mfa"
mfa3_data[str_detect(mfa3_data$evaluation, "arpa"),]$phoneset <- "arpa"

mfa3_data$adaptation <- "unadapted"
mfa3_data[str_detect(mfa3_data$evaluation, "adapted"),]$adaptation <- "Adapted"

mfa3_data$fine_tune <- "base"
mfa3_data[str_detect(mfa3_data$evaluation, "finetune"),]$fine_tune <- "Fine-tuned"


data <- subset(data, !is.na(data$alignment_score))

plotData <- summarySE(data=subset(mfa3_data, !is.na(mfa3_data$alignment_score)), measurevar = 'alignment_score', groupvars=c("phoneset", 'adaptation', 'fine_tune', "corpus"))

ggplot(aes(x=phoneset, y=mean * 1000, color=adaptation, shape=fine_tune), data=plotData) + geom_point(size = 5) +
  geom_errorbar(aes(ymin = (mean - ci) * 1000, ymax = (mean + ci)* 1000),size=2, width=0.5) +
  ylab('Phone boundary error (ms)') + xlab('Data subset') +ggtitle('Phone boundary errors') +
  theme_memcauliffe() +
  scale_x_discrete(guide = guide_axis(n.dodge = 2))+ facet_wrap(~corpus, scales='free_x') #+ scale_color_manual(values=cbbPalette)

plotData <- summarySE(data=mfa3_boundary_data, measurevar = 'abs_boundary_error', groupvars=c("evaluation", "corpus"))

plotData <- subset(plotData, !evaluation %in% c("mfa_3.1", "mfa_3.1_finetune", "mfa_3.1_adapted_finetune", "arpa_3.0", "arpa_3.0_finetune", "arpa_3.0_adapted_finetune"))

ggplot(aes(x=evaluation, y=mean * 1000), data=plotData) + geom_point(size = 5, color='#FB5607') +
  geom_errorbar(aes(ymin = (mean - ci) * 1000, ymax = (mean + ci)* 1000),size=2, width=0.5, color='#FB5607') +
  ylab('Phone boundary error (ms)') + xlab('Data subset') +ggtitle('Phone boundary errors') +
  theme_memcauliffe() +
  scale_x_discrete(guide = guide_axis(n.dodge = 2))+ facet_wrap(~corpus, scales='free_x') #+ scale_color_manual(values=cbbPalette) 

ggsave("output/utterance_boundary_agreement.png", width=1400, height=800, units="px", dpi=200)


plotData <- summarySE(data=boundary_data, measurevar = 'abs_boundary_error', groupvars=c("evaluation"))

ggplot(aes(x=following_reference_category, y=previous_reference_category, fill=mean * 1000), data=plotData) + geom_tile()+
  ylab('First segment') + xlab('Following segment') +
  theme_memcauliffe() + scale_fill_gradient(high='#FB5607', low="#003566", name="Abs error") +
  scale_x_discrete(guide = guide_axis(n.dodge = 2)) +ggtitle(paste("Mean boundary error for", ds, sep=" ")) +facet_wrap(~mfa_model)

ggsave(paste("output/", ds, "_phone_category_agreement.png", sep=""), width=2000, height=800, units="px", dpi=200)
