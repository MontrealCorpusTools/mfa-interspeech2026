
root_dir = "D:/Data/experiments/interspeech_benchmarking/evaluation_data"

data = data.frame()
boundary_data = data.frame()

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
    d$alignment_score <- as.numeric(d$alignment_score)
    d$utterance <- paste(d$file, str_replace_all(as.character(d$begin), '\\.', '-'), str_replace_all(as.character(d$end), '\\.', '-'), sep="-")
    d$evaluation = e
    d$corpus = c
    data = bind_rows(data,d)
    
    path = file.path(root_dir, c, e, "alignment_reference_evaluation_boundaries.csv")
    if (!file.exists(path)){
      next
    }
    print(path)
    d = read_csv(path, show_col_types = F, lazy=F)
    d$utterance <- paste(d$file, str_replace_all(as.character(d$utterance_begin), '\\.', '-'), str_replace_all(as.character(d$utterance_end), '\\.', '-'), sep="-")
    d$evaluation = e
    d$corpus = c
    boundary_data = bind_rows(boundary_data,d)
  }
}

data$evaluation = factor(data$evaluation)
data$corpus = factor(data$corpus)
boundary_data$evaluation = factor(boundary_data$evaluation)
boundary_data$corpus = factor(boundary_data$corpus)
boundary_data$abs_boundary_error = abs(boundary_data$boundary_error)

# MFA models for comparison across aligners are the adapted, but might still be worth quantifying/showing effect of adaptation
#mfa3_data <- subset(data, evaluation %in% c("mfa_3.1", "mfa_3.1_adapted", "arpa_3.0", "arpa_3.0_adapted"))
#data <- subset(data, !evaluation %in% c("mfa_3.1", "arpa_3.0"))
#data[data$evaluation=="mfa_3.1_adapted",]$evaluation <- "mfa_3.1"
#data[data$evaluation=="arpa_3.0_adapted",]$evaluation <- "arpa_3.0"
#data$evaluation = factor(data$evaluation)

#mfa3_boundary_data <- subset(boundary_data, evaluation %in% c("arpa_1.0", "mfa_3.1", "mfa_3.1_adapted", "arpa_3.0", "arpa_3.0_adapted"))
#boundary_data <- subset(boundary_data, !evaluation %in% c("mfa_3.1", "arpa_3.0"))
#boundary_data[boundary_data$evaluation=="mfa_3.1_adapted",]$evaluation <- "mfa_3.1"
#boundary_data[boundary_data$evaluation=="arpa_3.0_adapted",]$evaluation <- "arpa_3.0"
#boundary_data$evaluation = factor(boundary_data$evaluation)


test_phone_lists = list(
  maus=list(
    vowel=c("U@", "@U", "u:", "OI", "O:", "o~", "I@", "i:", "eI", "e@", "e~", "aU", "aI", "A:", "a~", "3:", "3`", "V", "U", "u", "Q", "I", "E", "e", "6", "@", "{", 'o', "o:", 'a', 'i', 'a:', 'e:'),
    stop=c("t", "k", "p", "g", "d", "b", "?", 'kk', 'k_j', 'k_jk_j', 'gg', 'g_j', 'b_j', 'p_j', 'p_jp_j', 'dd', 'tt', 'pp'),
    approximant=c("l=", "w", "R", "r", "l", "j", "4", '4_j', 'jj'),
    nasal=c("N=", "n=", "m=", "N", "n", "m", 'N\\', 'J', 'JJ', 'm_j'),
    fricative=c("h\\", "v", "T", "h", "f", "D", "p\\", 'p\\_j', 'pp\\', 'hh', 'C'),
    sibilant=c("Z", "z", "S", "s", 'ss', 'SS', "tS", "dZ", 'ts', 'tts', 'ttS', 'ddZ'),
    silence=c('sil', '<p:>', '<p>')
  ),
  arpa=list(
    vowel=c("AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER", 'EY', "IH", "IY", "OW", "OY", "UH", "UW", "AA1", "AE1", "AH1", "AO1", "AW1", "AY1", "EH1", "ER1", 'EY1', "IH1", "IY1", "OW1", "OY1", "UH1", "UW1", "AA2", "AE2", "AH2", "AO2", "AW2", "AY2", "EH2", "ER2", 'EY2', "IH2", "IY2", "OW2", "OY2", "UH2", "UW2","AA0", "AE0", "AH0", "AO0", "AW0", "AY0", "EH0", "ER0", 'EY0', "IH0", "IY0", "OW0", "OY0", "UH0", "UW0"),
    stop=c("B", "P", "D", "T", "G", "K"),
    approximant=c("R", "L", "Y", "W"),
    nasal=c("M", "N", "NG"),
    fricative=c("DH", "TH", "HH", "F", "V"),
    sibilant=c("S", "SH", "Z", "ZH", "CH", "JH"),
    silence=c('sil')
  ),
  mfa=list(
    vowel=c("a", "ɐ", "ɑ", "ɒ", "aː", "ɑː", "ɒː", "æ", "aj", "aw", "ɔj", "e", "ə", "ɚ", "eː", "ej", "ɛ", "ɝ", "ɛː", "ɥ i", "ɥ iː", "i", "ɪ", "ɨ", "i̥", "ɨ̥", "iː", "ɨː","j ɐ", "j e", "j eː", "j ɛː", "j o", "j oː", "j u", "j uː", "j ʌ", "j ʌː",  "ɯ", "ɯ̥","ɰ i", "ɰ iː", "ɯː", "o", "oː", "ow", "u", "ʉ", "ʊ", "uː", "ʉː", "ʌ", "ʌː",  "w ɐ", "w e", "w eː", "w ʌ", "w ʌː"),
    stop=c("pʰː","b", "bʲ", "c", "c͈","cː","cʰ","cʷ","d", "d̪","dː", "dʲ","ɡ", "ɡː", "ɡʷ", "ɟ", "ɟʷ", "k", "k̚", "k͈", "kː", "k͈ː", "kʰ", "kʷ", "k͈ʷ","p", "p̚", "p͈","pː","pʰ", "pʲ", "p͈ʲ","pʲː", "pʷ", "t", "t̚", "t̪", "t͈", "tː", "tʰ", "tʲ", "t��ʲ", "tʲː", "tʷ", "ʔ", "t͈ʲ"),
    approximant=c("ɥ", "j", "l", "ɫ", "ɭ", "ɫ̩", "ɭː","ɰ",  "ɹ", "ɾ","ɾʲ", "w", "ʎ", "ʎː"),
    nasal=c("m", "m̩","ɰ̃","mː", "mʲ", "mʲː", "n", "ɴ", "ɲ", "n̩", "nː", "ɴː", "ɲː", "ŋ","ɾ̃"),
    fricative=c("ç", "ð", "f", "fʲ", "ɣ", "h", "ɦ", "ʝ", "ɸ", "ɸː", "ɸʲ", "ɸʷ","v","vʲ", "x",  "β", "βʷ", "θ"),
    sibilant=c("s͈ː","t s", "d z", "tɕ͈ː", "ɕ", "ɕ͈","ɕː","s", "s͈", "ʃ", "sː", "sʰ", "sʷ","z", "ʑ", "ʒ", "ɕʰ", "dz", "dʑ", "dʑː", "dʒ", "tɕ", "tɕ͈", "tɕː", "tɕʰ", "tɕʷ", "tɕ͈ʷ","ts", "tʃ", "tsː"),
    silence=c('sil')
  ),
  gp=list(
    vowel=c("A", "AE", "E", "EO", "EU", "euI", "I", "iA", "iE", "iEO", "iO", "iU", "O", "oA", "OE", "U", "UE", "uEO"),
    stop=c("B", "BB", "D", "DD", "G", "GG", "k", "Kh", "p", "Ph", "t", "Th"),
    approximant=c("L", "R"),
    nasal=c("M", "N", "NG"),
    fricative=c("H"),
    sibilant=c("CHh", "J", "JJ", "S", "SS"),
    silence=c('sil')
  ),
  bournemouth=list(
    vowel=c("a", "a:", "æ", "aɪ", "aʊ", "ɔ", "ɔɪ", "e", "ə", "ɚ", "eɪ", "ɛ", "i", "ɪ", "i:", "j e", "j ɛ", "j o", "j u", "j ʌ", "ɯ", "o", "o:", "oʊ", "u", "ʊ", "u:", "ʌ", "w e", "w ɛ", "w i", "w ʌ"),
    stop=c("b", "d", "g", "k", "p", "q", "t"),
    approximant=c("j", "l", "ɹ", "ɾ", "w"),
    nasal=c("m", "n", "ŋ"),
    fricative=c("ç", "ð", "f", "h", "v", "θ"),
    sibilant=c("ɕ", "s", "ʃ", "z", "ʒ", "dʒ", "ts", "tʃ"),
    silence=c('sil')
  ),
  charsiu=list(
    vowel=c("AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER", 'EY', "IH", "IY", "OW", "OY", "UH", "UW", "AA1", "AE1", "AH1", "AO1", "AW1", "AY1", "EH1", "ER1", 'EY1', "IH1", "IY1", "OW1", "OY1", "UH1", "UW1", "AA2", "AE2", "AH2", "AO2", "AW2", "AY2", "EH2", "ER2", 'EY2', "IH2", "IY2", "OW2", "OY2", "UH2", "UW2","AA0", "AE0", "AH0", "AO0", "AW0", "AY0", "EH0", "ER0", 'EY0', "IH0", "IY0", "OW0", "OY0", "UH0", "UW0"),
    stop=c("B", "P", "D", "T", "G", "K"),
    approximant=c("R", "L", "Y", "W"),
    nasal=c("M", "N", "NG"),
    fricative=c("DH", "TH", "HH", "F", "V"),
    sibilant=c("S", "SH", "Z", "ZH", "CH", "JH"),
    silence=c('sil', "[SIL]", "sil [SIL]", '[SIL] sil')
  ),
  maps=list(
    vowel=c("AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER", 'EY', "IH", "IY", "OW", "OY", "UH", "UW", "AA1", "AE1", "AH1", "AO1", "AW1", "AY1", "EH1", "ER1", 'EY1', "IH1", "IY1", "OW1", "OY1", "UH1", "UW1", "AA2", "AE2", "AH2", "AO2", "AW2", "AY2", "EH2", "ER2", 'EY2', "IH2", "IY2", "OW2", "OY2", "UH2", "UW2","AA0", "AE0", "AH0", "AO0", "AW0", "AY0", "EH0", "ER0", 'EY0', "IH0", "IY0", "OW0", "OY0", "UH0", "UW0"),
    stop=c("B", "P", "D", "T", "G", "K"),
    approximant=c("R", "L", "Y", "W"),
    nasal=c("M", "N", "NG"),
    fricative=c("DH", "TH", "HH", "F", "V"),
    sibilant=c("S", "SH", "Z", "ZH", "CH", "JH"),
    silence=c('sil', 'H#')
  ),
  sppas=list(
    vowel=c('@', "@U", "{", "3:r", 'a', 'A', 'a:', 'aI', 'aU', 'e', 'E','e:', 'eI', 'i', 'I', 'i:', 'o', 'o:','O:', 'OI', 'u', 'U', 'u:', 'V'),
    stop=c("b", 'by', 'd', 'g', 'gy', 'k', 'ky', 'q', 'p', 'py', 't'),
    approximant=c("4", 'l', 'r', 'r\\', 'ry', 'w', 'y'),
    nasal=c('m', 'n', 'my', 'N', 'ny'),
    fricative=c('D', 'T', 'f', 'h', 'hy', 'v'),
    sibilant=c('j', 's', 'sh', 'S', 'z', 'Z', 'ch', 'dZ', 'ts','tS'),
    silence=c('sil', 'silE', 'silB', 'sp')
  ),
  julius=list(
    vowel=c("a", "a:", "e", "e:", "i", "i:", "o", "o:", "u", "u:"),
    stop=c("b", "by", "d", "dy", "g", "gy", "k", "ky", "p", "py", "q", "t"),
    approximant=c("r", "ry", "w", "y"),
    nasal=c("m", "my", "n", "N", "ny"),
    fricative=c("f", "h", "hy"),
    sibilant=c("s", "sh", "z", "ch", "ts", "j"),
    silence=c('sil', 'silB', 'silE', 'sp')
  ),
  koreanforcedaligner=list(
    vowel=c("a", "ae", "e", "eo", "eu", "i", "o", "oe", "u", "wa", "wae", "we", "weo", "wi", "ya", "yae", "ye", "yeo", "yi", "yo", "yu"),
    stop=c("b", "bb", "d", "dd", "g", "gg", "k", "p", "t"),
    approximant=c("l", "r"),
    nasal=c("m", "n", "ng"),
    fricative=c("h"),
    sibilant=c("s", "ss", "c", "j", "jj"),
    silence=c('sil')
  )
)


boundary_data$previous_test_category <- "unknown"
boundary_data$following_test_category <- "unknown"

for (n in names(test_phone_lists)) {
  for (category in names(test_phone_lists[[n]])){
    boundary_data[boundary_data$previous_test_phone %in% test_phone_lists[[n]][[category]] & str_detect(boundary_data$evaluation, n),]$previous_test_category = category
    boundary_data[boundary_data$following_test_phone %in% test_phone_lists[[n]][[category]] & str_detect(boundary_data$evaluation, n),]$following_test_category = category
  }
}
boundary_data[boundary_data$previous_test_phone %in% c( "ɾ","ɾʲ", "4") & boundary_data$corpus %in% c('timit', 'buckeye'),]$previous_test_category = 'stop'
boundary_data[boundary_data$following_test_phone %in% c( "ɾ","ɾʲ", "4") & boundary_data$corpus %in% c('timit', 'buckeye'),]$following_test_category = 'stop'

reference_phone_lists = list(
  timit=list(
    vowel=c('aa', 'aan', 'ao', 'aon', 'ae', 'aen', 'ah', 'ahn', 'aw', 'awn', 'ay', 'ayn', 'eh', 'ehn', 'er', 'ern', 'ey', 'eyn', 'ih', 'ihn', 'iy', 'iyn', 'ow', 'own', 'oy', 'oyn', 'uw', 'uwn', 'uh', 'uhn', 'ax', 'ax-h', 'ix', 'ux', 'axr', 'ih r', 'iy r'),
    stop=c('dx', 'b', 'p', 't', 'd', 'k', 'g', 'q', 'bcl', 'pcl', 'tcl', 'tcl q', 'dcl', 'kcl', 'gcl', 't w', 'g w', 'k w', 'd w', 'p w', 'b w'),
    approximant=c('el', 'l', 'r', 'y', 'w'),
    nasal=c("en", "n","nx","em", 'm', 'eng', 'ng'),
    fricative=c('th', 'dh', 'f', 'v', 'hh', 'hv'),
    sibilant=c('s', 'z', 'sh', 'zh', 'ch', 'jh'),
    silence=c('sil')
  ),
  buckeye=list(
    vowel=c('aa', 'aan', 'ao', 'aon', 'ae', 'aen', 'ah', 'ahn', 'aw', 'awn', 'ay', 'ayn', 'eh', 'ehn', 'er', 'ern', 'ey', 'eyn', 'ih', 'ihn', 'iy', 'iyn', 'ow', 'own', 'oy', 'oyn', 'uw', 'uwn', 'uh', 'uhn', 'ih r', 'iy r'),
    stop=c('b', 'p', 't', 'd', 'k', 'g', 'dx', 'tq'),
    approximant=c('el', 'l', 'r', 'y', 'w'),
    nasal=c("en", "n","nx","em", 'm', 'eng', 'ng'),
    fricative=c('th', 'dh', 'f', 'v', 'hh'),
    sibilant=c('s', 'z', 'sh', 'zh', 'ch', 'jh'),
    silence=c('sil')
  ),
  seoul_corpus=list(
    vowel=c('aa', 'ee', 'ii', 'oo', 'uu', 'vv', 'wa', 'we', 'wi', 'wv', 'xi', 'xx', 'ya', 'ye', 'yo', 'yu', 'yv'),
    stop=c('k0', 'kh', 'kk', 'p0', 'ph', 'pp', 't0', 'th', 'tt'),
    approximant=c('ll', 'll ll'),
    nasal=c('mm', 'mm mm', 'ng', 'nn', 'nn nn'),
    fricative=c('hh'),
    sibilant=c('s0', 'ss', 'c0', 'cc', 'ch'),
    silence=c('sil')
  ),
  csj=list(
    vowel=c('o', 'o H', 'a', 'a H', 'e', 'e H', 'i', 'i H', 'u', 'u H', 'H'),
    stop=c('b', 'by', 'bj', 'd', 'dy', 'dj', 'g', 'gy', 'gj', 'k', 'ky', 'kj', 'kw', 'p', 'py', 'Q', 'Q d', 'Q g', 'Q k','Q kj', 'Q ky', 'Q p', 'Q py', 'Q t', 't', 'ty', 'tj'),
    approximant=c('r', 'ry', 'w', 'y'),
    nasal=c('m', 'n','my', 'N', 'N m', 'N my', 'N N', 'N H', 'N n', 'N nj', 'N ny', 'nj', 'ny'),
    fricative=c('F', 'Fy', 'h', 'hy', 'Q F', 'v', 'hj'),
    sibilant=c('Q s', 'Q sj', 'Q sy', 'Q zj', 's', 'sj', 'sy', 'z', 'zj', 'zy', 'c', 'cj', 'cy', 'Q c', 'Q cj', 'Q cy'),
    silence=c('sil')
  )
)


boundary_data$previous_reference_category <- "unknown"
boundary_data$following_reference_category <- "unknown"

for (n in names(reference_phone_lists)) {
  for (category in names(reference_phone_lists[[n]])){
    boundary_data[boundary_data$previous_reference_phone %in% reference_phone_lists[[n]][[category]] & boundary_data$corpus == n,]$previous_reference_category = category
    boundary_data[boundary_data$following_reference_phone %in% reference_phone_lists[[n]][[category]] & boundary_data$corpus == n,]$following_reference_category = category
  }
}

boundary_data[boundary_data$previous_test_phone %in% c( "ER0", "ER1", 'ER2', 'R', "3:", "3`", "3:r","r\\") & boundary_data$previous_reference_phone %in% c( "axr","r", "er")& boundary_data$corpus %in% c('timit', 'buckeye'),]$previous_test_category = boundary_data[boundary_data$previous_test_phone %in% c( "ER0", "ER1", 'ER2', 'R', "3:", "3`", "3:r","r\\") & boundary_data$previous_reference_phone %in% c( "axr","r", "er")& boundary_data$corpus %in% c('timit', 'buckeye'),]$previous_reference_category

boundary_data[boundary_data$following_test_phone %in% c( "ER0", "ER1", 'ER2', 'R', "3:", "3`", "3:r","r\\") & boundary_data$following_reference_phone %in% c( "axr","r", "er")& boundary_data$corpus %in% c('timit', 'buckeye'),]$following_test_category = boundary_data[boundary_data$following_test_phone %in% c( "ER0", "ER1", 'ER2', 'R', "3:", "3`", "3:r","r\\") & boundary_data$following_reference_phone %in% c( "axr","r", "er")& boundary_data$corpus %in% c('timit', 'buckeye'),]$following_reference_category

boundary_data[boundary_data$following_test_phone %in% c( "v") & boundary_data$following_reference_phone %in% c( "b")& boundary_data$corpus %in% c('csj'),]$following_test_category = boundary_data[boundary_data$following_test_phone %in% c( "v") & boundary_data$following_reference_phone %in% c( "b")& boundary_data$corpus %in% c('csj'),]$following_reference_category

boundary_data[boundary_data$following_test_phone %in% c( "d", "dʲ") & boundary_data$following_reference_phone %in% c( "nn")& boundary_data$corpus %in% c('seoul_corpus'),]$following_test_category = boundary_data[boundary_data$following_test_phone %in% c( "d", "dʲ") & boundary_data$following_reference_phone %in% c( "nn")& boundary_data$corpus %in% c('seoul_corpus'),]$following_reference_category

boundary_data[boundary_data$previous_test_phone %in% c( "d", "dʲ") & boundary_data$previous_reference_phone %in% c( "nn")& boundary_data$corpus %in% c('seoul_corpus'),]$previous_test_category = boundary_data[boundary_data$previous_test_phone %in% c( "d", "dʲ") & boundary_data$previous_reference_phone %in% c( "nn")& boundary_data$corpus %in% c('seoul_corpus'),]$previous_reference_category


for (cor in levels(boundary_data$corpus)){
  print(cor)
  for (c in levels(boundary_data$previous_reference_category)){
    t <- subset(boundary_data, previous_reference_category == c)
    phones = sort(unique(t$previous_reference_phone))
    print(c)
    print(phones)
    t <- subset(boundary_data, following_reference_category == c)
    phones = sort(unique(t$following_reference_phone))
    print(phones)
  }
}

data %>% subset(is.na(alignment_score)) %>% group_by(corpus, evaluation) %>% summarise(unaligned_count=n())
View(data %>% group_by(corpus, evaluation) %>% summarise(unaligned_count=sum(is.na(alignment_score)),total=n()))
View(filtered_data %>% group_by(corpus, evaluation) %>% summarise(unaligned_count=sum(is.na(alignment_score)),total=n()))

unaligned_utterances = unique(subset(data, is.na(alignment_score) & evaluation != 'sppas')$utterance)

utterances_with_unknown = unique(subset(boundary_data, following_test_category == 'unknown' | previous_test_category == 'unknown')$utterance)
boundary_data %>% subset(following_test_category == 'unknown' | previous_test_category == 'unknown') %>%group_by(corpus, evaluation) %>% summarise(n_distinct(utterance))

filtered_data <- subset(data, !utterance %in% unaligned_utterances)
data %>% group_by(corpus, evaluation) %>% summarise(phone_count=sum(reference_phone_count), removed_utterances=sum(utterance %in% unaligned_utterances), unknown_utterances=sum(utterance %in% utterances_with_unknown),total=n())

threshold_table = boundary_data %>% mutate(thresh_20ms=abs_boundary_error *1000 <= 20, thresh_50ms=abs_boundary_error *1000 <= 50) %>% group_by(corpus, evaluation) %>% summarise(thresh_20ms=mean(thresh_20ms), thresh_50ms=mean(thresh_50ms)) 

filtered_boundary_data = boundary_data %>% subset(previous_reference_category == previous_test_category & following_reference_category == following_test_category & following_test_category != 'unknown' & following_reference_category != 'unknown' & previous_test_category != "unknown" & previous_reference_category != "unknown")
threshold_table_filtered = filtered_boundary_data %>% mutate(thresh_10ms=abs_boundary_error *1000 <= 10, thresh_20ms=abs_boundary_error *1000 <= 20, thresh_50ms=abs_boundary_error *1000 <= 50, thresh_100ms=abs_boundary_error *1000 <= 100) %>% group_by(corpus, evaluation) %>% summarise(mean_error=round(mean(abs_boundary_error *1000),2), thresh_10ms=round(mean(thresh_10ms) *100,2), thresh_20ms=round(mean(thresh_20ms) *100,2), thresh_50ms=round(mean(thresh_50ms) *100,2), thresh_100ms=round(mean(thresh_100ms) *100,2), n()) 

t = boundary_data %>% mutate(mismatch_categories=previous_reference_category != previous_test_category & following_reference_category != following_test_category & following_test_category != 'unknown' & following_reference_category != 'unknown' & previous_test_category != "unknown" & previous_reference_category != "unknown" & !utterance %in% unaligned_utterances, unknown_categories = following_test_category == 'unknown' | following_reference_category == 'unknown' | previous_test_category == "unknown" | previous_reference_category == "unknown") %>% group_by(corpus, evaluation) %>% summarise(mismatched=sum(mismatch_categories), unknown=sum(unknown_categories),total =n()) %>% mutate(mismatch_percent=mismatched/total * 100)

View(subset(boundary_data, evaluation == 'sppas'& corpus == 'buckeye' & previous_test_category == 'unknown'))
View(subset(boundary_data, evaluation == 'maus'& corpus == 'csj' & previous_test_category == 'unknown'))


View(subset(boundary_data, evaluation == 'mfa_trained_rules' & previous_reference_category != previous_test_category & corpus == 'seoul_corpus'))

View(filtered_data %>% subset(!is.na(alignment_score)) %>% group_by(corpus, evaluation) %>% summarise(mean_phone_error_rate= round(mean(phone_error_rate) *100,2), mean_alignment_score= round(mean(alignment_score) *1000,2)))


head(filtered_data %>% subset(!is.na(alignment_score) & evaluation == 'maps' & corpus == 'timit') %>% arrange(desc(phone_error_rate)))


# Interspeech plots


cbbPalette <- c("#c5050c", "#006992", "#adadad", "#432e4f", "#8dd3ce", "#fccb51")

## English

plotData <- summarySE(data=subset(boundary_data, evaluation %in% c("arpa_1.0", "arpa_3.0", "maus", "maps", "charsiu", "bournemouth", "sppas", "julius", "koreanforcedaligner") & corpus %in% c("buckeye", "timit")), measurevar = 'abs_boundary_error', groupvars=c("evaluation", "corpus"))

plotData$evaluation = factor(plotData$evaluation, levels = c("arpa_3.0", "arpa_1.0", "maus", "sppas", "julius", "koreanforcedaligner", "maps", "charsiu", "bournemouth"), labels= c("MFA 3.0", "MFA 1.0", "MAUS", "SPPAS", "Julius", "KFA", "MAPS*", "Charsiu*", "BFA*"))
plotData$corpus = factor(plotData$corpus, levels= c("timit", "buckeye"), labels=c("TIMIT", "Buckeye"))

ggplot(aes(x=evaluation, y=mean * 1000, color=corpus), data=plotData) + geom_point(size = 3) +
  geom_errorbar(aes(ymin = (mean - ci) * 1000, ymax = (mean + ci)* 1000),size=1, width=0.25) +
  ylab('Phone boundary error (ms)') + xlab('Aligner') +ggtitle('Phone boundary errors in English') +
  theme_minimal(base_size = 16) +
  scale_y_continuous(limits=c(10, 50), expand = c(0,0)) +
  theme(
    panel.grid.minor = element_blank(), 
    panel.border = element_rect(color = "grey40", fill = NA)
  ) + 
  ggokabeito::scale_color_okabe_ito(name="Corpus")
  #scale_color_manual(values=cbbPalette, name="Corpus")

ggsave("output/interspeech_english_boundaries.png", width=13.33, height=7.5, dpi=600)

## Japanese

plotData <- summarySE(data=subset(boundary_data, evaluation %in% c("mfa_1.0", "mfa_3.1", "maus", "maps", "charsiu", "bournemouth", "sppas", "julius", "koreanforcedaligner") & corpus %in% c("csj")), measurevar = 'abs_boundary_error', groupvars=c("evaluation", "corpus"))

plotData$evaluation = factor(plotData$evaluation, levels = c("mfa_3.1", "mfa_1.0", "maus", "sppas", "julius", "koreanforcedaligner", "maps", "charsiu", "bournemouth"), labels= c("MFA 3.0", "MFA 1.0", "MAUS", "SPPAS", "Julius", "KFA", "MAPS*", "Charsiu*", "BFA*"))
plotData$corpus = factor(plotData$corpus, levels= c("csj"), labels=c("CSJ"))

ggplot(aes(x=evaluation, y=mean * 1000, color=corpus), data=plotData) + geom_point(size = 3) +
  geom_errorbar(aes(ymin = (mean - ci) * 1000, ymax = (mean + ci)* 1000),size=1, width=0.25) +
  ylab('Phone boundary error (ms)') + xlab('Aligner') +ggtitle('Phone boundary errors in Japanese') +
  scale_y_continuous(limits=c(10, 80), expand = c(0,0), breaks=c(10,20,40,60,80)) +
  theme_minimal(base_size = 16) +
  theme(
    panel.grid.minor = element_blank(), 
    panel.border = element_rect(color = "grey40", fill = NA)
  ) +
  ggokabeito::scale_color_okabe_ito(name="Corpus")
#scale_color_manual(values=cbbPalette, name="Corpus")

ggsave("output/interspeech_japanese_boundaries.png", width=13.33, height=7.5, dpi=600)

## Korean

plotData <- summarySE(data=subset(boundary_data, evaluation %in% c("gp_1.0", "mfa_3.1", "maus", "maps", "charsiu", "bournemouth", "sppas", "julius", "koreanforcedaligner") & corpus %in% c("seoul_corpus")), measurevar = 'abs_boundary_error', groupvars=c("evaluation", "corpus"))

plotData$evaluation = factor(plotData$evaluation, levels = c("mfa_3.1", "gp_1.0", "maus", "sppas", "julius", "koreanforcedaligner", "maps", "charsiu", "bournemouth"), labels= c("MFA 3.0", "MFA 1.0", "MAUS", "SPPAS", "Julius", "KFA", "MAPS*", "Charsiu*", "BFA*"))
plotData$corpus = factor(plotData$corpus, levels= c("seoul_corpus"), labels=c("Seoul"))

ggplot(aes(x=evaluation, y=mean * 1000, color=corpus), data=plotData) + geom_point(size = 3) +
  geom_errorbar(aes(ymin = (mean - ci) * 1000, ymax = (mean + ci)* 1000),size=1, width=0.25) +
  ylab('Phone boundary error (ms)') + xlab('Aligner') +ggtitle('Phone boundary errors in Korean') +
  scale_y_continuous(limits=c(10, 90), expand = c(0,0), breaks=c(10,20,40,60,80)) +
  theme_minimal(base_size = 16) +
  theme(
    panel.grid.minor = element_blank(), 
    panel.border = element_rect(color = "grey40", fill = NA)
  ) +
  ggokabeito::scale_color_okabe_ito(name="Corpus")
#scale_color_manual(values=cbbPalette, name="Corpus")

ggsave("output/interspeech_korean_boundaries.png", width=13.33, height=7.5, dpi=600)


# MFA 3.0 evaluations

plotData <- summarySE(data=subset(boundary_data, evaluation %in% c("mfa_3.1", "mfa_3.1_adapted", "mfa_remapped", "mfa_remapped_adapted", "mfa_trained")), measurevar = 'abs_boundary_error', groupvars=c("evaluation", "corpus"))

plotData$evaluation = factor(plotData$evaluation, levels = c("mfa_3.1", "mfa_3.1_adapted", "mfa_trained", "mfa_remapped", "mfa_remapped_adapted"), labels= c("Pretrained", "Adapted", "Trained", "English", "+Adapted"))
plotData$corpus = factor(plotData$corpus, levels= c("timit", "buckeye", "csj", "seoul_corpus"), labels=c("TIMIT", "Buckeye", "CSJ", "Seoul"))

ggplot(aes(x=evaluation, y=mean * 1000, color=corpus), data=plotData) + geom_point(size = 3) +
  geom_errorbar(aes(ymin = (mean - ci) * 1000, ymax = (mean + ci)* 1000),size=1, width=0.25) +
  ylab('Phone boundary error (ms)') + xlab('MFA model') +ggtitle('Phone boundary errors in MFA 3.0') +
  theme_minimal(base_size = 16) +
  theme(
    panel.grid.minor = element_blank(), 
    panel.border = element_rect(color = "grey40", fill = NA)
  ) +
  ggokabeito::scale_color_okabe_ito(name="Corpus") +
  facet_wrap(~corpus, scales="free")+ guides(colour = "none")
#scale_color_manual(values=cbbPalette, name="Corpus")

ggsave("output/interspeech_mfa_boundaries.png", width=13.33, height=7.5, dpi=600)

t <- subset(data, evaluation=="mfa_3.1" & corpus=="buckeye") %>% summarise(seconds_per_word=sum(duration)/sum(word_count), seconds_per_phone=sum(duration)/sum(reference_phone_count))
