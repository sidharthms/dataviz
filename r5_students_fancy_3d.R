args <- commandArgs(TRUE)
library("plotly")
library("htmlwidgets")
setwd(args[1])
data=read.csv(args[2], header=TRUE,sep=",")
data=as.matrix(data)

graph=plot_ly(z = data, type = "surface")
saveWidget(graph, file=args[3], selfcontained = TRUE)  
