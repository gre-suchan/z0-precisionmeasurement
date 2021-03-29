import numpy as np
import matplotlib.pyplot as plt
from efficiencies import mat, err_mat

ntoy = 500000

# Create numpy matrix of list to append elements of inverted toy matrices
# inverse_toys = np.empty((4, 4))

# Create a list consisting only of the same matrix mat and err_mat, repeated
# ntoy times
template_matrix = np.tile(mat, reps=[ntoy, 1, 1])
template_err_matrix = np.tile(err_mat, reps=[ntoy, 1, 1])

# Now, create one random number for each pair of mean and sd; invert the
# simulated efficiency matrix and "reshape" these inverted matrix to be
# matrices of lists with length ntoy.
# This works mainly as np.linalg.inv automatically iterates over lists of
# matrices (thank you numpy)
inverse_toys = np.dstack(
    np.linalg.inv(
        np.random.normal(template_matrix,
                         template_err_matrix,
                         size=(ntoy, 4, 4))))


# Define gaussian function to draw to the toy distributions:
def gauss(x, A, mu, sigma):
    return A * np.exp(-(x - mu)**2 / (2. * sigma**2))


# These matrices will hold the estimated errors and means (i think the latter
# are not that useful?)
inverse_errors = np.zeros((4, 4))
inverse_means = np.zeros((4, 4))

# Plotting setup
fig = plt.figure(figsize=(20, 10), dpi=80)
fig.subplots_adjust(left=None,
                    bottom=None,
                    right=None,
                    top=None,
                    wspace=0.2,
                    hspace=0.2)

# This is a 4 x 4 "matrix"  of plt.subplots indexed 1 through 16
axes = [[plt.subplot(4, 4, 1 + j * 4 + k) for k in range(0, 4)]
        for j in range(0, 4)]

hists = list()
# Fill histograms for each inverted matrix coefficient:
for j in range(0, 4, 1):
    hists.append(list())
    for k in range(0, 4, 1):
        # These are the ML estimators for a gaussian distribution
        mean = np.mean(inverse_toys[j, k, :])
        sd = np.std(inverse_toys[j, k, :])

        # Based on those, create normalized hists with a certain range within
        # the 4 x 4 matrix
        hbins, hedges, _ = axes[j][k].hist(inverse_toys[j, k, :],
                                           bins=20,
                                           range=(mean - 4 * sd,
                                                  mean + 4 * sd),
                                           histtype='step',
                                           linewidth=2,
                                           label=f'toyhist{j}{k}')
        axes[j][k].legend()
        hists[j].append(np.array([hbins, hedges, _], dtype=object))

        # Instead of a curve_fit, we just use the mean estimator from above
        scale = 0.997 * ntoy * 8 * sd / 20 * 1 / np.sqrt(2 * np.pi * sd**2)
        coeffs = (scale, mean, sd)

        # Now plot the gaussian using our estimators
        xspace = np.linspace(hedges[0], hedges[-1], 150)
        h_fit = gauss(xspace, *coeffs)
        axes[j][k].plot(xspace, h_fit, label=f'Fit{j}{k}')

        # To avoid misfitting of the gaussian, take directly std of values
        # in the histogram as the uncertainty
        inverse_means[j, k] = np.mean(inverse_toys[j, k, :])
        inverse_errors[j, k] = np.std(inverse_toys[j, k, :])

inv = np.linalg.inv(mat)
exact_inverse_errors = np.zeros((4, 4))
for alpha in range(4):
    for beta in range(4):
        exact_inverse_errors[alpha, beta] = np.sqrt(
            sum(inv[alpha, i]**2 * err_mat[i, j]**2 * inv[j, beta]**2
                for i in range(4) for j in range(4)))

if __name__ == "__main__":
    print(f"Means for the inverse matrix:\n{inverse_means}")
    print(f"Erros for the inverse matrix:\n{inverse_errors}")
    plt.show()
    print("Inverse")
    print(np.linalg.inv(mat))
    print("Exact solution")
    print(exact_inverse_errors)
