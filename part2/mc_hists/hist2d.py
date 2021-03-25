import matplotlib.pyplot as plt
import awkward as ak
from hist import pcharged_ha, pcharged_el, pcharged_mu, pcharged_tau, \
    e_ecal_ha, e_ecal_el, e_ecal_mu, e_ecal_tau, branches_mu, branches_el

angle_mu = ak.to_numpy(branches_mu[b'cos_thet'])
angle_el = ak.to_numpy(branches_el[b'cos_thet'])

# angle = angle_el[branches_el['cos_thet'] < 2]

plt.subplot(2, 2, 1)
plt.hist2d(e_ecal_el, pcharged_el, range=[[0, 120], [0, 120]])
plt.subplot(2, 2, 2)
plt.hist2d(e_ecal_mu, pcharged_mu, range=[[0, 120], [0, 120]])
plt.subplot(2, 2, 3)
plt.hist2d(e_ecal_tau, pcharged_tau, range=[[0, 120], [0, 120]])
plt.subplot(2, 2, 4)

plt.hist2d(e_ecal_ha, pcharged_ha, range=[[0, 120], [0, 120]])

plt.show()
