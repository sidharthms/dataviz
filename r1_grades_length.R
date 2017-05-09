args <- commandArgs(TRUE)

# Library
library(streamgraph)
library(htmlwidgets)

# Load data:
setwd(args[1])
length=read.table(args[2], header=TRUE,sep=",")

year=length[ ,2]
name=length[ ,3]
value=length[ ,4]
data=data.frame(year, name, value)

# png(filename=args[3])
sg <- streamgraph(data, key="name", value="value", date="year", scale="continuous")
# sg_fill_brewer("Blues")
# dev.off()

# sg <- streamgraph(data = hashtags_df, key = "hashtag", value = "value", date = "yearmonth",
#                  offset = "silhouette", interpolate = "cardinal",
#                  width = "700", height = "400") %>%
  # sg_legend(TRUE, "hashtag: ") %>%
  # sg_axis_x(tick_interval = 1, tick_units = "year", tick_format = "%Y")

# Save it for viewing in the blog post
# For some reason I can not save it to files/R/ direclty so need to use file.rename()
saveWidget(sg, file=args[3], selfcontained = TRUE)
# file.rename("twitter_streamgraph.html", "files/R/twitter_streamgraph.html")
