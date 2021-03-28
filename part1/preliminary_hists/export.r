#!/usr/bin/env Rscript

library(ggplot2)
library(magrittr)

hadrons   <- read.csv("../grope-tables/hadrons.csv")
electrons <- read.csv("../grope-tables/electrons.csv")
muons     <- read.csv("../grope-tables/muons.csv")
taus      <- read.csv("../grope-tables/taus.csv")
# Combine the data.frames
data <- rbind(hadrons, electrons, muons, taus)
data$particle <- factor(rep(c("h", "e", "m", "t"), each=50),
                        levels=c("h", "e", "m", "t", "u"))
data$tec.ratio <- data$p.charged / data$e.ecal

bin.and.hist <- function (df, bins, column) {
    ret <- as.data.frame(
                         do.call(cbind,
                                 tapply(df[[column]],
                                        data$particle,
                                        . %>% tapply(., cut(., breaks=bins), length))))

    ret$min <- bins[-length(bins)]
    ret$max <- bins[-1]
    ret$mid <- (ret$max - ret$min) / 2
    ret[is.na(ret)] <- 0
    return(ret)
}

# This is the binning of the n.charged observable
nchr.brks <- seq(0, 80, by=5)
hist.df <- bin.and.hist(data, nchr.brks, "n.charged")

write.csv(file="../../plot_data/part1/hists/n.charged.csv",
          row.names=F,
          hist.df)

tex.brks <- seq(0, 75, by=2)
ggplot(data=data[data$particle != "h", ],
       aes(x=tec.ratio, group=particle, fill=particle)) +
    geom_histogram(alpha=.5, breaks=tex.brks, position='identity', color='black') +
    theme_minimal()

hist.df2 <- bin.and.hist(data, tex.brks, "tec.ratio")

write.csv(file="../../plot_data/part1/hists/tec.ratio.csv",
          row.names=F,
          hist.df2)

ecal.brks <- seq(0, 125, by=5)
hist.df3 <- bin.and.hist(data, ecal.brks, "e.ecal")

write.csv(file="../../plot_data/part1/hists/ecal.csv",
          row.names=F,
          hist.df3)

