import numpy as np
import matplotlib.pyplot as plt
from efficiencies import mat, err_mat

ntoy = 5000000

# Create numpy matrix of list to append elements of inverted toy matrices
# inverse_toys = np.empty((4, 4))

# Create a list of the same matrix mat and err_mat
template_matrix = np.tile(mat, reps=[ntoy, 1, 1])
template_err_matrix = np.tile(err_mat, reps=[ntoy, 1, 1])

# Now, create one random number for each pair of mean and sd; invert the
# simulated efficiency matrix and "reshape" these inverted matrix to be
# matrices of lists with length ntoy
inverse_toys = np.dstack(
    np.linalg.inv(
        np.random.normal(template_matrix,
                         template_err_matrix,
                         size=(ntoy, 4, 4))))


# Define gaussian function to draw to the toy distributions:
def gauss(x, A, mu, sigma):
    return A * np.exp(-(x - mu)**2 / (2. * sigma**2))


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
ax00 = plt.subplot(4, 4, 1)
ax01 = plt.subplot(4, 4, 2)
ax02 = plt.subplot(4, 4, 3)
ax03 = plt.subplot(4, 4, 4)

ax10 = plt.subplot(4, 4, 5)
ax11 = plt.subplot(4, 4, 6)
ax12 = plt.subplot(4, 4, 7)
ax13 = plt.subplot(4, 4, 8)

ax20 = plt.subplot(4, 4, 9)
ax21 = plt.subplot(4, 4, 10)
ax22 = plt.subplot(4, 4, 11)
ax23 = plt.subplot(4, 4, 12)

ax30 = plt.subplot(4, 4, 13)
ax31 = plt.subplot(4, 4, 14)
ax32 = plt.subplot(4, 4, 15)
ax33 = plt.subplot(4, 4, 16)

axes = [[ax00, ax01, ax02, ax03], [ax10, ax11, ax12, ax13],
        [ax20, ax21, ax22, ax23], [ax30, ax31, ax32, ax33]]

p0 = np.dstack(
    np.array([
        500 * np.ones((4, 4)),
        np.eye(4), .2 * np.eye(4) + .01 * np.ones((4, 4))
    ]))

# Fill histograms for each inverted matrix coefficient:
for j in range(0, 4, 1):
    for k in range(0, 4, 1):
        mean = np.mean(inverse_toys[j, k, :])
        sd = np.std(inverse_toys[j, k, :])
        # Diagonal and off-diagonal terms have different histogram ranges
        hbins, hedges, _ = axes[j][k].hist(inverse_toys[j, k, :],
                                           bins=20,
                                           density=True,
                                           range=(mean - 4 * sd,
                                                  mean + 4 * sd),
                                           histtype='step',
                                           linewidth=2,
                                           label=f'toyhist{j}{k}')
        axes[j][k].legend()

        # Instead of a curve_fit, we just estimate the mean using the ML
        # estimator
        coeffs = (1 / np.sqrt(2 * np.pi * sd**2), mean, sd)

        xspace = np.linspace(hedges[0], hedges[-1], 150)
        h_fit = gauss(xspace, *coeffs)

        axes[j][k].plot(xspace, h_fit, label=f'Fit{j}{k}')

        # To avoid misfitting of the gaussian, take directly std of values
        # in the histogram as the uncertainty
        inverse_means[j, k] = np.mean(inverse_toys[j, k, :])
        inverse_errors[j, k] = np.std(inverse_toys[j, k, :])

if __name__ == "__main__":
    print(f"Erros for the inverse matrix:\n{inverse_errors}")
    print(f"Means for the inverse matrix:\n{inverse_means}")
    plt.show()
