#!/usr/bin/Rscript
# https://github.com/HGmin1159/Seoul_Festival
library(readr)

bst <- readRDS("bst.rds")

target<-read_csv('target_tag.csv')

df1<-as.matrix(target[,-1])

pred1 <-predict(bst, df1)

output<-cbind(target,pred1)

write.csv(output,file="output.csv",
  row.names=TRUE 
  )
