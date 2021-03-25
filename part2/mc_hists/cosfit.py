import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from hist import df

# Test fit for the cos_thet distribution of the electrons.

angle = df.loc[(df['ptype'] == 'e') & (df['cos_thet'] < 2), 'cos_thet']


# Function we want to fit to the data
def fit_function(x, A, B, C):
    return (A * (1 + x**2) + B / (1 - x)**2 + C)

def s_channel(x, A, C):
    return (A * (1 + x**2) + C) 

def t_channel(x, B, C):
    return (B / (1 - x)**2 + C)

# Bined data.
angle_bined, bins = np.histogram(angle, bins=np.linspace(-1, 0.8, 1000))

# Calculate bin centers
bincenters = np.array([0.5 * (bins[i] + bins[i+1]) for i in
    range(len(bins)-1)])

# fit using curve_fit
popt, pcov = curve_fit(fit_function, xdata = bincenters, ydata = angle_bined,
        p0 = [1000, 100, 1])

# Print fit parameters
print(popt)

### Ploting the results

# xvalues for the plotting
xspace = np.linspace(-1, 1, 10000, endpoint=False)

# the plots
plt.bar(bincenters, angle_bined, width = bins[1] - bins[0], color = 'navy',
        label = r'Histogram entries')
plt.plot(xspace, fit_function(xspace, *popt), color = 'darkorange', linewidth
        = 2.5, label = r'Fitted function')
plt.plot(xspace, s_channel(xspace, popt[0], popt[2]), color = 'b') 
plt.plot(xspace, t_channel(xspace, popt[1], popt[2]), color = 'g') 

plt.ylim(0, 1.1 * max(angle_bined))
plt.show()

