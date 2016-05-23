library(dplyr)

df=read.csv("../data/clozeTestReviewed.csv",header=T,strip.white=TRUE)
nComp=df %>% group_by(sentID) %>% summarise(nComp=length(unique(subj_id))) #merge & derive accurate percentages. On last step
clozeCounts=df %>% group_by(sentID,CompLcase) %>% summarise(popularity = length(unique(subj_id)),percent = (length(unique(subj_id))/52*100)) %>% arrange(desc(popularity)) -> test
mostPop=clozeCounts %>% group_by(sentID) %>% filter(popularity == max(popularity))

