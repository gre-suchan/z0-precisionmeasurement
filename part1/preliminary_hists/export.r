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

# This is the binning of the n.charged observable
nchr.brks <- seq(0, 80, by=5)
as.data.frame(
              do.call(cbind,
                      tapply(data$n.charged,
                             data$particle,
                             . %>% tapply(., cut(., breaks=nchr.brks), length)))) -> hist.df

hist.df$min <- nchr.brks[-length(nchr.brks)]
hist.df$max <- nchr.brks[-1]
hist.df[is.na(hist.df)] <- 0

write.csv(file="../../plot_data/part1/hists/n.charged.csv",
          hist.df)

tex.brks <- seq(0, 75, by=2)
ggplot(data=data[data$particle != "h", ],
       aes(x=tec.ratio, group=particle, fill=particle)) +
    geom_histogram(alpha=.5, breaks=tex.brks, position='identity', color='black') +
    theme_minimal()

as.data.frame(
              do.call(cbind,
                      tapply(data$tec.ratio,
                             data$particle,
                             . %>% tapply(., cut(., breaks=tex.brks), length)))) -> hist.df2

hist.df2$min <- tex.brks[-length(tex.brks)]
hist.df2$max <- tex.brks[-1]
hist.df2[is.na(hist.df2)] <- 0

write.csv(file="../../plot_data/part1/hists/tec.ratio.csv",
          hist.df2)

ecal.brks <- seq(0, 125, by=5)
as.data.frame(
              do.call(cbind,
                      tapply(data$e.ecal,
                             data$particle,
                             . %>% tapply(., cut(., breaks=ecal.brks), length)))) -> hist.df3

hist.df3$min <- ecal.brks[-length(ecal.brks)]
hist.df3$max <- ecal.brks[-1]
hist.df3[is.na(hist.df3)] <- 0

write.csv(file="../../plot_data/part1/hists/ecal.csv",
          hist.df3)

