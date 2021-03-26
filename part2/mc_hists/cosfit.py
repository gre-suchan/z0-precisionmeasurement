import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from hist import df

# Test fit for the cos_thet distribution of the electrons.

angle = df.loc[(df['ptype'] == 'e') & (df['cos_thet'] < 2), 'cos_thet']


# Function we want to fit to the data
def fit_function(x, A, B):
    return (A * (1 + x**2) + B / (1 - x)**2)


# Separate function the s channel
def s_channel(x, A):
    return (A * (1 + x**2))


# Separate function the s channel
def t_channel(x, B):
    return (B / (1 - x)**2)


# Bined data.
angle_binned, bins = np.histogram(angle, bins=np.linspace(-.9, .9, 30))

# Calculate bin centers
bincenters = (bins[1:] + bins[:-1]) / 2

# fit using curve_fit
popt, pcov = curve_fit(fit_function,
                       xdata=bincenters,
                       ydata=angle_binned,
                       sigma=np.sqrt(angle_binned),
                       p0=[100, 10])

# Print fit parameters
print(popt)

# Ploting the results

# xvalues for the plotting
xspace = np.linspace(-1, 1, 10000, endpoint=False)

# the plots
plt.hist(angle, bins=bins)
# plt.bar(bincenters,
#         angle_binned,
#         width=bins[1] - bins[0],
#         color='navy',
#         label=r'Histogram entries')

plt.plot(xspace,
         fit_function(xspace, *popt),
         color='darkorange',
         linewidth=2.5,
         label=r'Fitted function')

plt.plot(xspace, s_channel(xspace, popt[0]), color='b', label='s')
plt.plot(xspace, t_channel(xspace, popt[1]), color='g', label='t')

plt.ylim(0, 1.1 * max(angle_binned))
plt.legend()
plt.show()


#### Integrals to calculate cuts ####
# Rootfunction of the s channel.
def rootfunction_A (x, A):
    return (A * (x**3 / 3 + x))

# Rootfunction of the t channel.
def rootfunction_B(x, B):
    return (B / (1 - x))

# Cuts to get just the s channel electrons
upper_cut = 0.
lower_cut = -0.9

# Efficiency of the cut, calculated by dividing the integral of the s-channel
# function for the given interval with the integral of the over all function
# for the given interval.
efficiency = (rootfunction_A(upper_cut, popt[0]) - rootfunction_A(lower_cut,
    popt[0]))/(rootfunction_A(upper_cut, popt[0]) + rootfunction_B(upper_cut,
        popt[1]) - rootfunction_A(lower_cut, popt[0]) -
        rootfunction_B(lower_cut, popt[1]))
print(efficiency)
