args <- commandArgs(TRUE)

library(MASS)
setwd(args[1])
data=read.table(args[2], header=TRUE,sep=",")
my_colors=colors()[as.numeric(data$grade)*11]
png(filename=args[3])
parcoord(data[,c(2:4)] , col= my_colors ,var.label=TRUE)
dev.off()
