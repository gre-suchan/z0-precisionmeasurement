import uproot
import awkward as ak
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Path to the MC submodule
path_data = '../../z0decayMC/'

# {{{ Data setup
# Here we just read in the MC root files and name all the branches. This can
# probably be done better in a pandas df.

# Set up electron data
file_el = uproot.open(path_data + 'ee.root')
ttree_name = 'myTTree'
file_el[ttree_name].keys()
branches_el = file_el[ttree_name].arrays()

ncharged_el = ak.to_numpy(branches_el[b'Ncharged'])
pcharged_el = ak.to_numpy(branches_el[b'Pcharged'])
e_ecal_el = ak.to_numpy(branches_el[b'E_ecal'])
e_hcal_el = ak.to_numpy(branches_el[b'E_hcal'])

# Set up tau data
file_tau = uproot.open(path_data + 'tt.root')
ttree_name2 = 'myTTree'
file_tau[ttree_name2].keys()
branches_tau = file_tau[ttree_name2].arrays()

ncharged_tau = ak.to_numpy(branches_tau[b'Ncharged'])
pcharged_tau = ak.to_numpy(branches_tau[b'Pcharged'])
e_ecal_tau = ak.to_numpy(branches_tau[b'E_ecal'])
e_hcal_tau = ak.to_numpy(branches_tau[b'E_hcal'])

# Set up muon data
file_mu = uproot.open(path_data + 'mm.root')
ttree_name3 = 'myTTree'
file_mu[ttree_name3].keys()
branches_mu = file_mu[ttree_name3].arrays()

ncharged_mu = ak.to_numpy(branches_mu[b'Ncharged'])
pcharged_mu = ak.to_numpy(branches_mu[b'Pcharged'])
e_ecal_mu = ak.to_numpy(branches_mu[b'E_ecal'])
e_hcal_mu = ak.to_numpy(branches_mu[b'E_hcal'])

# Set up hadron data
file_ha = uproot.open(path_data + 'qq.root')
ttree_name4 = 'myTTree'
file_ha[ttree_name4].keys()
branches_ha = file_ha[ttree_name4].arrays()

ncharged_ha = ak.to_numpy(branches_ha[b'Ncharged'])
pcharged_ha = ak.to_numpy(branches_ha[b'Pcharged'])
e_ecal_ha = ak.to_numpy(branches_ha[b'E_ecal'])
e_hcal_ha = ak.to_numpy(branches_ha[b'E_hcal'])
# }}}

# Hadron Cuts
# This is the first cut we make: All events with more than 7 charged tracks are
# selected to be hadrons.
hadron_ha = ncharged_ha[branches_ha[b'Ncharged'] >= 7]
hadron_el = ncharged_el[branches_el[b'Ncharged'] >= 7]
hadron_mu = ncharged_mu[branches_mu[b'Ncharged'] >= 7]
hadron_tau = ncharged_tau[branches_tau[b'Ncharged'] >= 7]
Nhadron_total = len(hadron_ha) + len(hadron_el) + \
    len(hadron_mu) + len(hadron_tau)

print("Hadron Background:",
      (len(hadron_el) + len(hadron_mu) + len(hadron_tau)) / Nhadron_total)

print("Hadron Acceptance loss:",
      (len(ncharged_ha) - len(hadron_ha)) / len(ncharged_ha))

# Muon Cuts
# Now we select the muons. For this we require that the energy in the
# electromagnetic calorimeter E_Ecal is less than 10 while the scalar momentum
# sum should exceed 70. Physically, these are events featuring charged
# particles with high momenta which don't deposit a lot of energy in the
# electromagnetic calorimeter. As some of the particles have a scalar momentum
# sum of zero, we select those to be muons, too, if all the other requirements
# were met. Currently, we don't know why the scalar momentum sum is 0 at all,
# however, we know that those are about 90% Muons
muon_el = e_ecal_el[(branches_el[b'Ncharged'] < 7)
                    & (branches_el[b'E_ecal'] < 10) &
                    ((branches_el[b'Pcharged'] >= 70) |
                     (branches_el[b'Pcharged'] == 0))]
muon_mu = e_ecal_mu[(branches_mu[b'Ncharged'] < 7)
                    & (branches_mu[b'E_ecal'] < 10) &
                    ((branches_mu[b'Pcharged'] >= 70) |
                     (branches_mu[b'Pcharged'] == 0))]
muon_tau = e_ecal_tau[(branches_tau[b'Ncharged'] < 7)
                      & (branches_tau[b'E_ecal'] < 10) &
                      ((branches_tau[b'Pcharged'] >= 70) |
                       (branches_tau[b'Pcharged'] == 0))]
muon_ha = e_ecal_ha[(branches_ha[b'Ncharged'] < 7)
                    & (branches_ha[b'E_ecal'] < 10) &
                    ((branches_ha[b'Pcharged'] >= 70) |
                     (branches_ha[b'Pcharged'] == 0))]

Nmuon_total = len(muon_ha) + len(muon_el) + len(muon_mu) + len(muon_tau)

print("Muon Background:",
      (len(muon_el) + len(muon_ha) + len(muon_tau)) / Nmuon_total)

print("Muon Acceptance loss:",
      (len(e_ecal_mu) - len(muon_mu)) / len(e_ecal_mu))

# Electron Cuts
# Events with a small number of charged particles but a high amount of energy
# deposited in the E_Ecal are selected to be electrons. The Ncharged condition
# rejects hadrons (cut 1) and the high E_Ecal value (which is our selection
# criteria for electrons) automatically rejects muons (cut 2)
electron_el = e_ecal_el[(branches_el[b'Ncharged'] < 7)
                        & (branches_el[b'E_ecal'] >= 70)]
electron_mu = e_ecal_mu[(branches_mu[b'Ncharged'] < 7)
                        & (branches_mu[b'E_ecal'] >= 70)]
electron_tau = e_ecal_tau[(branches_tau[b'Ncharged'] < 7)
                          & (branches_tau[b'E_ecal'] >= 70)]
electron_ha = e_ecal_ha[(branches_ha[b'Ncharged'] < 7)
                        & (branches_ha[b'E_ecal'] >= 70)]
Nelectron_total = len(electron_ha) + len(electron_el) + \
    len(electron_mu) + len(electron_tau)

print("Electron Background:",
      (len(electron_mu) + len(electron_ha) + len(electron_tau)) /
      Nelectron_total)

print("Electron Acceptance loss:",
      (len(e_ecal_el) - len(electron_el)) / len(e_ecal_el))

# Tau Cuts
# Events with low amount of charged particles and medium (i. e. E_Ecal is in
# (10 GeV, 66 GeV)) deposit the electromagnetic calorimeter are selected to be
# taus. Muons (cut 2) are excluded via the momentum requirement; Hadrons (cut
# 1) via Ncharged.
# Note that particles with Ncharged < 7 and E_ecal in (66, 70)  are discarded
# as we couldn't (yet?) think of a criterion that cleanly selects taus from
# electrons.
tau_el = e_ecal_el[(branches_el[b'Ncharged'] < 7)
                   & (branches_el[b'E_ecal'] < 65) &
                   ((branches_el[b'E_ecal'] > 20)
                   | ((branches_el[b'Pcharged'] <= 70) & 
                   (branches_el[b'Pcharged'] > 0)))]
tau_mu = e_ecal_mu[(branches_mu[b'Ncharged'] < 7)
                   & (branches_mu[b'E_ecal'] < 65) &
                   ((branches_mu[b'E_ecal'] > 20)
                   | ((branches_mu[b'Pcharged'] <= 70) &
                   (branches_mu[b'Pcharged'] > 0)))]
tau_tau = e_ecal_tau[(branches_tau[b'Ncharged'] < 7)
                     & (branches_tau[b'E_ecal'] < 65) &
                   ((branches_tau[b'E_ecal'] > 20)
                   | ((branches_tau[b'Pcharged'] <= 70) & 
                   (branches_tau[b'Pcharged'] > 0)))]
tau_ha = e_ecal_ha[(branches_ha[b'Ncharged'] < 7)
                   & (branches_ha[b'E_ecal'] < 65) &
                   ((branches_ha[b'E_ecal'] > 20)
                   | ((branches_ha[b'Pcharged'] <= 70) & 
                   (branches_ha[b'Pcharged'] > 0)))]

Ntau_total = len(tau_ha) + len(tau_el) + len(tau_mu) + len(tau_tau)

print("Tau Background:",
      (len(tau_mu) + len(tau_ha) + len(tau_el)) / Nelectron_total)

print("Tau Acceptance loss:",
      (len(e_ecal_tau) - len(tau_tau)) / len(e_ecal_tau))

angle_mu = ak.to_numpy(branches_mu[b'cos_thet'])
angle_el = ak.to_numpy(branches_el[b'cos_thet'])

#angle = angle_el[branches_el['cos_thet'] < 2]

plt.subplot(2,2,1)
plt.hist2d(e_ecal_el, pcharged_el, range=[[0,120],[0,120]])
plt.subplot(2,2,2)
plt.hist2d(e_ecal_mu, pcharged_mu, range=[[0,120],[0,120]])
plt.subplot(2,2,3)
plt.hist2d(e_ecal_tau, pcharged_tau, range=[[0,120],[0,120]])
plt.subplot(2,2,4)

plt.hist2d(e_ecal_ha, pcharged_ha, range=[[0,120],[0,120]])

plt.show()
