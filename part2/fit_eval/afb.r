library(dplyr)
library(magrittr)

df <- read.csv("../../plot_data/part2/forward_backward/A_FB.csv",
               col.names=c("sqrt.s", "N.f","N.b","N.f.err","N.b.err", "A.FB",
                           "A.FB.err","sin.W","sin.W_err", "sqrt.s.err"), 
               skip=2)

df %$%
    plot(sqrt.s, A.FB)
df %$%
    arrows(sqrt.s, A.FB-A.FB.err,
           sqrt.s, A.FB+A.FB.err,
           length=.05, angle=90, code=3)

fit <- lm(A.FB ~ sqrt.s, data=df, weights=1/A.FB.err^2)
abline(fit, col='red')

# Our measured Z mass
M.Z <- 91.19046
M.Z.err <- 0.05137956

# Forward backward asymmetry at resonance by linear model prediction
A.FB.res <- as.numeric(predict(fit, newdata=data.frame(sqrt.s=c(M.Z))))
# Propagate error
grad <- c(1, M.Z, coef(fit)[2])
# Construct a covariance matrix out of the fit covariance matrix and the error
# on M.Z
v <- vcov(fit) %>%
    rbind(0) %>%
    cbind(c(0, 0, M.Z.err^2))
A.FB.res.err <- as.numeric(sqrt(grad %*% v %*% grad))

points(M.Z, A.FB.res, col='blue')
arrows(M.Z, A.FB.res-A.FB.res.err,
       M.Z, A.FB.res+A.FB.res.err,
       length=.05, angle=90, code=3)

# From A.Fb.res calculate the sin^2 of the Weinberg angle
sin2.W <- 1/4 * (1 - sqrt(abs(A.FB.res/3)))
sin2.W.err <- 1/24 * A.FB.res.err / sqrt(abs(A.FB.res) / 3)

