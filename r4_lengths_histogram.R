args <- commandArgs(TRUE)
library("plotly")
library("htmlwidgets")
setwd(args[1])
length=read.csv(args[2], header=TRUE,sep=",")

graph <- plot_ly(x=length[ ,2],  opacity = 0.6, type = "histogram")
col=ncol(length)
for (i in 3:(col-1)){
   graph <- graph %>% add_trace(x=length[ ,i],  opacity = 0.6, type = "histogram")
   # graph[i]=plot_ly(x=length[ ,i],  opacity = 0.6, type = "histogram") %>%
}
graph <- graph %>% layout(barmode="overlay")
saveWidget(graph, file=args[3], selfcontained = TRUE)  
