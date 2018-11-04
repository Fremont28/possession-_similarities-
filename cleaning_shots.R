#10/24/18 15-16 nba pbp
library(plyr)
library(dplyr)

nba_pbp=read.csv("(10-20-2015)-(06-20-2016)-combined-stats.csv")
head(nba_pbp)
table(nba_pbp['type']) 
#shot attempts only 
shot_att=subset(nba_pbp,shot_distance>=0)

#time posessions 
shot_att$poss_time=substr(shot_att$play_length,start=6,stop=8)
shot_att$poss_time=as.numeric(shot_att$poss_time)

shot_att$assists<-ifelse(grepl("AST", shot_att$description), 1, 0)
shot_att$block<-ifelse(grepl("BLK", shot_att$description), 1, 0)
shot_att$make<-ifelse(grepl("MISS", shot_att$description), 0, 1)
shot_att$stl<-ifelse(grepl("STL", shot_att$description), 1, 0)

shot_att$make=as.factor(shot_att$make)
shot_att$converted_x=as.numeric(shot_att$converted_x)
shot_att$converted_y=as.numeric(shot_att$converted_y)
shot_att$original_x=as.numeric(shot_att$original_x)
shot_att$original_y=as.numeric(shot_att$original_y)

#export to csv file 
write.csv(shot_att,file="shot_att_16.csv")


