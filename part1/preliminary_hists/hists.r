#!/usr/bin/env Rscript

library(ggplot2)

hadrons   <- read.csv("../grope-tables/hadrons.csv")
electrons <- read.csv("../grope-tables/electrons.csv")
muons     <- read.csv("../grope-tables/muons.csv")
taus      <- read.csv("../grope-tables/taus.csv")

# Combine the data.frames
data <- rbind(hadrons, electrons, muons, taus)
data$particle <- factor(rep(c("h", "e", "m", "t"), each=50),
                        levels=c("h", "e", "m", "t", "u"))
# data$guess <- "u" # This is the guessed particle type. u="unknown"
data$guess <- factor(c("u"), levels=c("h", "e", "m", "t", "u"))

# Cut: hadrons have n.charged >= 15
# sum(data$particle == "h" & data$n.charged >= 15) / sum(data$particle == "h")
data[data$n.charged >= 7, ]$guess <- "h"

# New Criterion: sump/e.ecal
data$tec.ratio <- data$p.charged / data$e.ecal

# "Only" muons have a high tex.ratio, i.e. sump/e.ecal
# sum(data$particle == "m" & data$tec.ratio >= 8) / sum(data$particle == "m")
data[data$guess == "u" & data$tec.ratio >= 8,]$guess <- "m"

# Maybe attempt to cut e.ecal to separate electrons and taus?
data[data$guess == "u" & data$e.ecal >= 70 & data$e.hcal <= 20,]$guess <- "e"
data[data$guess == "u" & data$e.ecal <= 60,]$guess <- "t"


# Now we calculate the background and acceptance of each particle
for (particle in c("h", "m", "e", "t")) {
    print(paste("Acceptance loss for", particle))
    print(1 - sum(data$particle == particle & data$guess == particle) /
          sum(data$particle == particle))
    print(paste("Background for", particle))
    print(sum(data$particle != particle & data$guess == particle) /
          sum(data$guess == particle))
}

# vim:foldmethod=marker
