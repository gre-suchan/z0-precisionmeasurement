library(dplyr)
library(magrittr)
library(units)
c.n <- c("sqrt.s","sqrt.s.err","sigma","sigma.err")
df.e <- read.csv("../../plot_data/part2/crosssections/e.csv", col.names=c.n)
df.m <- read.csv("../../plot_data/part2/crosssections/m.csv", col.names=c.n)
df.t <- read.csv("../../plot_data/part2/crosssections/t.csv", col.names=c.n)
df.h <- read.csv("../../plot_data/part2/crosssections/h.csv", col.names=c.n)

# Fit function
bw.dist <- function(E, Gamma.e.Gamma.f, M.Z, Gamma.Z) {
    return(12 * pi / M.Z^2 * Gamma.e.Gamma.f * E^2 /
           ((E^2 - M.Z^2)^2 + (E^4 * Gamma.Z^2 / M.Z^2)))
}

plot.and.fit <- function (df, plot=F) {
    fit <- nls(sigma ~ sapply(sqrt.s, bw.dist, Gamma.e.Gamma.f, M.Z, Gamma.Z),
               data=df,
               start=list(Gamma.e.Gamma.f=5000, M.Z=91, Gamma.Z=3),
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

# Summarize the fits real quick
fit.df <- data.frame(t(sapply(list(df.e, df.m, df.t, df.h),
                              . %>%
                                  plot.and.fit %>%
                                  summary %>%
                                  .$coefficients %>%
                                  as.data.frame %>%
                                  select(c(1, 2)) %>%
                                  as.matrix %>%
                                  as.vector %>%
                                  abs
                              )))
colnames(fit.df) <- c("Gamma.e.Gamma.f", "M.Z", "Gamma.Z",
                      "Gamma.e.Gamma.f.err", "M.Z.err", "Gamma.Z.err")
rownames(fit.df) <- c("e", "m", "t", "h")

# Helper function to convert from the unit of the fit coefficient 
# to MeV^2
fix_units = . %>% 
    set_units("nanobarn*GeV^4/c^2/hbar^2") %>%
    set_units("MeV^2")

# This is the electron decay width
Gamma.e <- fit.df$Gamma.e.Gamma.f[1]  %>% 
    fix_units %>%
    sqrt

# This is the electron decay width's error
Gamma.e.err <- fit.df$Gamma.e.Gamma.f.err[1] %>%
    fix_units %>%
    "*"(1/2 * 1/Gamma.e)

# Write all decay widths to fit.df
fit.df$Gamma.f <- fit.df$Gamma.e.Gamma.f[2:4] %>%
    fix_units %>%
    "/"(Gamma.e) %>%
    c(Gamma.e, .)

# Alongside their errors
fit.df <- fit.df %>% 
    mutate(Gamma.f.err = sqrt((fix_units(Gamma.e.Gamma.f.err) / Gamma.e)^2 +
                              (Gamma.e.err * fix_units(Gamma.e.Gamma.f) / Gamma.e^2)^2))
fit.df[1, "Gamma.f.err"] <- Gamma.e.err
fit.df

# (c^4/MeV^2) -> 1/MeV^2 -> fb

