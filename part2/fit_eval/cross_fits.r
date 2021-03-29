library(magrittr)
c.n <- c("sqrt.s","sqrt.s.err","sigma","sigma.err")
df.e <- read.csv("../../plot_data/part2/crosssections/e.csv", col.names=c.n)
df.m <- read.csv("../../plot_data/part2/crosssections/m.csv", col.names=c.n)
df.t <- read.csv("../../plot_data/part2/crosssections/t.csv", col.names=c.n)
df.h <- read.csv("../../plot_data/part2/crosssections/h.csv", col.names=c.n)

# Fit function
bw.dist <- function(E, Gamma.e.Gamma.f, M.Z, Gamma.Z) {
    return(12 * pi * Gamma.e.Gamma.f * E^2 / 
           ((E^2 - M.Z^2)^2 + (E^4 * Gamma.Z^2 / M.Z^2)))
}

plot.and.fit <- function (df, plot=F) {
    fit <- nls(sigma ~ sapply(sqrt.s, bw.dist, Gamma.e.Gamma.f, M.Z, Gamma.Z),
               data=df,
               start=list(Gamma.e.Gamma.f=1, M.Z=91, Gamma.Z=3),
               weights=1/(df$sigma.err^2),
               ); 
    if (plot) {
        # Ugly plot
        plot(df$sqrt.s, df$sigma)
        arrows(df$sqrt.s-df$sqrt.s.err, df$sigma,
               df$sqrt.s+df$sqrt.s.err, df$sigma,
               length=.05, angle=90, code=3)
        arrows(df$sqrt.s, df$sigma-df$sigma.err,
               df$sqrt.s, df$sigma+df$sigma.err,
               length=.05, angle=90, code=3)

        xrange <- seq(88, 94, length.out = 250)
        xrange %>%
            lines(predict(fit, newdata=data.frame(sqrt.s=.)), col='blue')
    }
    return(fit)
}

library(dplyr)
# Summarize the fits real quick
fit.df <- data.frame(t(sapply(list(df.e, df.m, df.t, df.h),
                            . %>% 
                                plot.and.fit %>%
                                summary %>% 
                                .$coefficients %>%
                                as.data.frame %>%
                                select(c(1, 2)) %>%
                                as.matrix %>% 
                                as.vector
                            )))
colnames(fit.df) <- c("Gamma.e.Gamma.f", "M.Z", "Gamma.Z", 
                      "Gamma.e.Gamma.f.err", "M.Z.err", "Gamma.Z.err")
rownames(fit.df) <- c("e", "m", "t", "h")
fit.df$Gamma.f <- 0
fit.df$Gamma.f.err <- 0
fit.df["e", "Gamma.f"] <- sqrt(fit.df["e", "Gamma.e.Gamma.f"])
# TODO: continue here  <29-03-21, gregor> #
