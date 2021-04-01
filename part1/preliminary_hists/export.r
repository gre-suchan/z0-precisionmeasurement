#!/usr/bin/env Rscript

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
hist.df2 <- bin.and.hist(data, tex.brks, "tec.ratio")

write.csv(file="../../plot_data/part1/hists/tec.ratio.csv",
          row.names=F,
          hist.df2)

ecal.brks <- seq(0, 125, by=5)
hist.df3 <- bin.and.hist(data, ecal.brks, "e.ecal")

write.csv(file="../../plot_data/part1/hists/ecal.csv",
          row.names=F,
          hist.df3)

p.brks <- seq(0, 120, by=5)
hist.df4 <- bin.and.hist(data, p.brks, "p.charged")
write.csv(file="../../plot_data/part1/hists/p.charged.csv",
          row.names=F,
          hist.df4)

hcal.brks <- seq(0, 86, by=2)
hist.df5 <- bin.and.hist(data, hcal.brks, "e.hcal")
write.csv(file="../../plot_data/part1/hists/hcal.csv",
          row.names=F,
          hist.df5)

aaa <- seq(-1, 3, by=1)
hist.df6 <- bin.and.hist(data, aaa, "n.muon")
write.csv(file="../../plot_data/part1/hists/n.muon.csv",
          row.names=F,
          hist.df6)
