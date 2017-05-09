args <- commandArgs(TRUE)

setwd(args[1])
data=read.table(args[2], header=TRUE,sep=",")

# To generate a density plot.
library(ggplot2)

png(filename=args[3])
p  <- ggplot(data, aes(Length, colour=NumReqPosts, fill=NumReqPosts))
p  <- p + geom_density(alpha=0.55)
print(p)
dev.off()
