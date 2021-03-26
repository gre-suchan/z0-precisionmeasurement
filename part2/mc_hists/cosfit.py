import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from hist import df

# Test fit for the cos_thet distribution of the electrons.

angle = df.loc[(df['ptype'] == 'e') & (df['cos_thet'] < 2), 'cos_thet']


# Function we want to fit to the data
def fit_function(x, A, B, C):
    return (A * (1 + x**2) + B / (1 - x)**2 + C)


# Separate function the s channel
def s_channel(x, A, C):
    return (A * (1 + x**2) + C)


# Separate function the s channel
def t_channel(x, B, C):
    return (B / (1 - x)**2 + C)


# Bined data.
angle_binned, bins = np.histogram(angle, bins=np.linspace(-0.9, 0.9, 30))

# Calculate bin centers
bincenters = (bins[1:] + bins[:-1]) / 2

# fit using curve_fit
popt, pcov = curve_fit(fit_function,
                       xdata=bincenters,
                       ydata=angle_binned,
                       p0=[1000, 100, 1])

# Print fit parameters
print(popt)

# Ploting the results

# xvalues for the plotting
xspace = np.linspace(-1, 1, 10000, endpoint=False)

# the plots
plt.bar(bincenters,
        angle_binned,
        width=bins[1] - bins[0],
        color='navy',
        label=r'Histogram entries')

plt.plot(xspace,
         fit_function(xspace, *popt),
         color='darkorange',
         linewidth=2.5,
         label=r'Fitted function')

plt.plot(xspace, s_channel(xspace, popt[0], popt[2]), color='b', label='s')
plt.plot(xspace, t_channel(xspace, popt[1], popt[2]), color='g', label='t')

plt.ylim(0, 1.1 * max(angle_binned))
plt.legend()
plt.show()
