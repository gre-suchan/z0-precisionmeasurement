library(dplyr)
library(magrittr)
library(units)
library(functional)
c.n <- c("sqrt.s","sqrt.s.err","sigma","sigma.err")
df.e <- read.csv("../../plot_data/part2/crosssections/e.csv", col.names=c.n)
df.m <- read.csv("../../plot_data/part2/crosssections/m.csv", col.names=c.n)
df.t <- read.csv("../../plot_data/part2/crosssections/t.csv", col.names=c.n)
df.h <- read.csv("../../plot_data/part2/crosssections/h.csv", col.names=c.n)

# Install units
install_unit("c", "299792458 m/s", "speed of light in vacuum")
install_unit("hbar", "1.05457148e-34 m2 kg / s", "planck constant")
c0 <- as_units("c")
hbar <- as_units("hbar")

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

# ...Alongside their errors
fit.df <- fit.df %>%
    mutate(Gamma.f.err = sqrt((fix_units(Gamma.e.Gamma.f.err) / Gamma.e)^2 +
                              (Gamma.e.err * fix_units(Gamma.e.Gamma.f) /
                               Gamma.e^2)^2))
# Fix the error on Gamma.e as the mutate above overwrote it
fit.df[1, "Gamma.f.err"] <- Gamma.e.err
# Print results
fit.df[c("Gamma.f", "Gamma.f.err")]

Gamma.Z <- set_units(weighted.mean(fit.df$Gamma.Z, 1 / fit.df$Gamma.Z.err^2),
                     GeV)
# More conservative error estimation: Standard error of mean as the values to
# be averaged over are extremely similar
# Gamma.Z.err <- 1 / sqrt(sum(1 / fit.df$Gamma.Z.err^2))
Gamma.Z.err <- set_units(fit.df$Gamma.Z %>% {sd(.) / sqrt(length(.))},
                         GeV)

####################################
#  Number of neutrino generations  #
####################################

# This is the theoretical value for the neutrino decay width
Gamma.nu <- set_units(165.88050, MeV)
# The invisible width is the difference between the total and the observed
# widths. By dividing the invisible width by the neutrino width, we should be
# able to obtain the total number of neutrino generations
N.Neutrinos <- (Gamma.Z - sum(fit.df$Gamma.f)) / Gamma.nu
N.Neutrinos.err <- sqrt(Gamma.Z.err^2 + sum(fit.df$Gamma.f.err^2)) / Gamma.nu


####################################
#  Cross section/Branching ratios  #
####################################

fit.df %<>%
    mutate(sigma.peak=set_units(12 * pi * Gamma.e.Gamma.f / (M.Z^2 * Gamma.Z^2),
                                nanobarn))
    
gradient <- . %>% {12 * pi * c(1 / (.[2]^2 * .[3]^2),
                               .[1] / (.[2]^2 * (-.[3])^3),
                               .[1] / (-.[2]^3 * .[3]^2))}

fit.df$sigma.peak.err <- lapply(list(df.e, df.m, df.t, df.h), . %>%    # For each of the data...
                                plot.and.fit %>%                       # Calculate the fits again
                                {list(gradient(coef(.)), vcov(.))} %>% # Compute coef gradient and cov matrix
                                {.[[1]] %*% .[[2]] %*% .[[1]]} %>%     # Multiply them out
                                as.numeric) %>%                        # Convert to a numeric again
                         unlist %>%                                    # Convert the whole thing to a num vector
                         set_units(nanobarn)                           # Set the units

# Compute the ratios of the cross sections at peak
fit.df %<>%
    mutate(sigma.peak.ratio=sigma.peak / sigma.peak[4])

# and their errors
fit.df %<>%
    mutate(sigma.peak.ratio.err=sqrt((sigma.peak.err / sigma.peak[4])^2 +
                                     (sigma.peak.err[4] * sigma.peak /
                                      sigma.peak[4]^2)^2))

# Compute the ratios of the decay widths
fit.df %<>%
    mutate(branching.ratio=Gamma.f / Gamma.f[4])

# and their errors
fit.df %<>%
    mutate(branching.ratio.err=sqrt((Gamma.f.err / Gamma.f[4])^2 +
                                     (Gamma.f.err[4] * Gamma.f /
                                      Gamma.f[4]^2)^2))
# Present the results
fit.df[-c(4), c('sigma.peak.ratio', 'sigma.peak.ratio.err',
                'branching.ratio', 'branching.ratio.err')]

# Test if the two ratio samples stem from the same distribution
fit.df[-c(4), ] %$% ks.test(drop_units(sigma.peak.ratio),
                            drop_units(branching.ratio))
fit.df[-c(4), ] %$% t.test(drop_units(sigma.peak.ratio),
                           drop_units(branching.ratio))
