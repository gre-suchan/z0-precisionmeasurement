#!/usr/bin/env Rscript

library(ggplot2)

hadrons   <- read.csv("../grope-tables/hadrons.csv")
electrons <- read.csv("../grope-tables/electrons.csv")
muons     <- read.csv("../grope-tables/muons.csv")
taus      <- read.csv("../grope-tables/taus.csv")

# Combine the data.frames
data <- rbind(hadrons, electrons, muons, taus)
data$particle <- rep(c("h", "e", "m", "t"), each=50)
data$guess <- "u" # This is the guessed particle type. u="unknown"

# This is the binning of the n.charged observable
nchr.brks <- seq(0, 80, by=5)
ggplot(data=data,
       aes(x=n.charged, group=particle, fill=particle)) +
    geom_histogram(alpha=.5, breaks=nchr.brks, position='identity', color='black') +
    theme_minimal()

# {{{ Old histograms
# Set colors for the standard R hists
h.col <- rgb(1, 1, 0, 1/4)
e.col <- rgb(0,0,1,1/4)
m.col <- rgb(0,1,0,1/4)
t.col <- rgb(1,0,0,1/4)
hist(hadrons$n.charged,   breaks=nchr.brks, add=F, col=h.col)
hist(electrons$n.charged, breaks=nchr.brks, add=T, col=e.col)
hist(muons$n.charged,     breaks=nchr.brks, add=T, col=m.col)
hist(taus$n.charged,      breaks=nchr.brks, add=T, col=t.col)
# }}}

# Cut: hadrons have n.charged >= 15
sum(data$particle == "h" & data$n.charged >= 15) / sum(data$particle == "h")
data[data$n.charged >= 15, ]$guess <- "h"

# New Criterion: sump/e.ecal
hadrons$tec.ratio   <- hadrons$p.charged   / hadrons$e.ecal
electrons$tec.ratio <- electrons$p.charged / electrons$e.ecal
muons$tec.ratio     <- muons$p.charged     / muons$e.ecal
taus$tec.ratio      <- taus$p.charged      / taus$e.ecal
data$tec.ratio      <- data$p.charged      / data$e.ecal

# "Only" muons have a high tex.ratio, i.e. sump/e.ecal
sum(data$particle == "m" & data$tec.ratio >= 8) / sum(data$particle == "m")
data[data$guess == "u" & data$tec.ratio >= 8,]$guess <- "m"

tex.brks <- c(seq(0, 7.5, by=.5), seq(8, 75, by=5))
ggplot(data=data[data$particle != "h", ],
       aes(x=tec.ratio, group=particle, fill=particle)) +
    geom_histogram(alpha=.5, breaks=tex.brks, position='identity', color='black') +
    theme_minimal()

hist(electrons$tec.ratio, breaks=tex.brks,freq=T, ylim=c(0, 60), xlim=c(0, 8.5), add=F, col=e.col)
hist(muons$tec.ratio,     breaks=tex.brks,freq=T, ylim=c(0, 60), xlim=c(0, 8.5), add=T, col=m.col)
hist(taus$tec.ratio,      breaks=tex.brks,freq=T, ylim=c(0, 60), xlim=c(0, 8.5), add=T, col=t.col)

# Maybe attempt to cut e.ecal to separate electrons and taus?
ggplot(data=data[data$particle %in% c("e", "t"), ],
       aes(x=e.hcal, fill=particle)) +
    geom_histogram(breaks=seq(0, 125, by=5), position='identity', color='grey50', alpha=.5) +
    theme_classic()

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
