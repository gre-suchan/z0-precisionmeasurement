import numpy as np
import matplotlib.pyplot as plt

def Re_chi(s, M_Z, Gamma_Z):
    return ((s**2 - M_Z**2 * s) / ((s - M_Z**2)**2 + (s * Gamma_Z / M_Z)**2))

M_Z = 91.188
Gamma_Z = 2.495

s = np.linspace(88, 93, 10)

plt.plot(s, Re_chi(s, M_Z, Gamma_Z))
plt.show()
