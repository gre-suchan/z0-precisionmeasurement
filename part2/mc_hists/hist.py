import uproot
import awkward as ak
import numpy as np
import matplotlib.pyplot as plt

path_data = '../../z0decayMC/'

#Set up electron data
file_el = uproot.open(path_data + 'ee.root')
ttree_name = 'myTTree'
file_el[ttree_name].keys()
branches_el = file_el[ttree_name].arrays()

ncharged_el = ak.to_numpy(branches_el[b'Ncharged'])
pcharged_el = ak.to_numpy(branches_el[b'Pcharged'])
e_ecal_el = ak.to_numpy(branches_el[b'E_ecal'])
e_hcal_el = ak.to_numpy(branches_el[b'E_hcal'])

#Set up tau data
file_tau = uproot.open(path_data + 'tt.root')
ttree_name2 = 'myTTree'
file_tau[ttree_name2].keys()
branches_tau = file_tau[ttree_name2].arrays()

ncharged_tau = ak.to_numpy(branches_tau[b'Ncharged'])
pcharged_tau = ak.to_numpy(branches_tau[b'Pcharged'])
e_ecal_tau = ak.to_numpy(branches_tau[b'E_ecal'])
e_hcal_tau = ak.to_numpy(branches_tau[b'E_hcal'])


#Set up muon data
file_mu = uproot.open(path_data + 'mm.root')
ttree_name3 = 'myTTree'
file_mu[ttree_name3].keys()
branches_mu = file_mu[ttree_name3].arrays()

ncharged_mu = ak.to_numpy(branches_mu[b'Ncharged'])
pcharged_mu = ak.to_numpy(branches_mu[b'Pcharged'])
e_ecal_mu = ak.to_numpy(branches_mu[b'E_ecal'])
e_hcal_mu = ak.to_numpy(branches_mu[b'E_hcal'])

#Set up hardron data
file_ha = uproot.open(path_data + 'qq.root')
ttree_name4 = 'myTTree'
file_ha[ttree_name4].keys()
branches_ha = file_ha[ttree_name4].arrays()

ncharged_ha = ak.to_numpy(branches_ha[b'Ncharged'])
pcharged_ha = ak.to_numpy(branches_ha[b'Pcharged'])
e_ecal_ha = ak.to_numpy(branches_ha[b'E_ecal'])
e_hcal_ha = ak.to_numpy(branches_ha[b'E_hcal'])


# Hardronen Cuts
hardron_ha = ncharged_ha[branches_ha[b'Ncharged'] >= 7]
hardron_el = ncharged_el[branches_el[b'Ncharged'] >= 7]
hardron_mu = ncharged_mu[branches_mu[b'Ncharged'] >= 7]
hardron_tau = ncharged_tau[branches_tau[b'Ncharged'] >= 7]
Nhardron_gesamt = len(hardron_ha) + len(hardron_el) + len(hardron_mu) + len(hardron_tau)

print("Hardronen Untergrund:", (len(hardron_el) + len(hardron_mu) + len(hardron_tau)
) / Nhardron_gesamt)

print("Hardronen Akzeptanzverlust:", (len(ncharged_ha) - len(hardron_ha)) / len(ncharged_ha))

# Muon Cuts
muon_mu = e_ecal_mu[(branches_mu[b'Ncharged'] < 7) & ((branches_mu[b'Pcharged']
    / branches_mu[b'E_ecal']) >= 8)]
muon_tau = e_ecal_tau[branches_tau[b'Ncharged'] < 7 &
        ((branches_tau[b'Pcharged'] / branches_tau[b'E_ecal']) >= 8)]
muon_ha = e_ecal_ha[(branches_ha[b'Ncharged'] < 7) &
        ((branches_ha[b'Pcharged'] / branches_ha[b'E_ecal']) >= 8)]
muon_el = e_ecal_el[(branches_el[b'Ncharged'] < 7) &
        ((branches_el[b'Pcharged'] / branches_el[b'E_ecal']) >= 8)]

Nmuon_gesamt = len(muon_ha) + len(muon_el) + len(muon_mu) + len(muon_tau)

print("Muon Untergrund:", (len(muon_el) + len(muon_ha) + len(muon_tau)
) / Nmuon_gesamt)

print("Muon Akzeptanzverlust:", (len(e_ecal_mu[branches_mu[b'Pcharged'] > 0]) - len(muon_mu)) / len(e_ecal_mu[branches_mu[b'Pcharged'] > 0]))

# Electron Cuts
electron_el = e_ecal_el[(branches_el[b'Ncharged'] < 7) & ((branches_el[b'Pcharged']
    / branches_el[b'E_ecal']) < 8) & (branches_el[b'E_ecal'] >= 70)]
electron_mu = e_ecal_mu[(branches_mu[b'Ncharged'] < 7) & ((branches_mu[b'Pcharged']
    / branches_mu[b'E_ecal']) < 8) & (branches_mu[b'E_ecal'] >= 70)]
electron_tau = e_ecal_tau[(branches_tau[b'Ncharged'] < 7) & ((branches_tau[b'Pcharged']
    / branches_tau[b'E_ecal']) < 8) & (branches_tau[b'E_ecal'] >= 70)]
electron_ha = e_ecal_ha[(branches_ha[b'Ncharged'] < 7) & ((branches_ha[b'Pcharged']
    / branches_ha[b'E_ecal']) < 8) & (branches_ha[b'E_ecal'] >= 70)]
Nelectron_gesamt = len(electron_ha) + len(electron_el) + len(electron_mu) + len(electron_tau)

print("Electron Untergrund:", (len(electron_mu) + len(electron_ha) +
    len(electron_tau)
) / Nelectron_gesamt)

print("Electron Akzeptanzverlust:", (len(e_ecal_el) - len(electron_el)) /
        len(e_ecal_el))

# Tau Cuts
tau_el = e_ecal_el[(branches_el[b'Ncharged'] < 7) & ((branches_el[b'Pcharged']
    / branches_el[b'E_ecal']) < 8) & (branches_el[b'E_ecal'] < 60)]
tau_mu = e_ecal_mu[(branches_mu[b'Ncharged'] < 7) & ((branches_mu[b'Pcharged']
    / branches_mu[b'E_ecal']) < 8) & (branches_mu[b'E_ecal'] < 60)]
tau_tau = e_ecal_tau[(branches_tau[b'Ncharged'] < 7) & ((branches_tau[b'Pcharged']
    / branches_tau[b'E_ecal']) < 8) & (branches_tau[b'E_ecal'] < 60)]
tau_ha = e_ecal_ha[(branches_ha[b'Ncharged'] < 7) & ((branches_ha[b'Pcharged']
    / branches_ha[b'E_ecal']) < 8) & (branches_ha[b'E_ecal'] < 60)]
Ntau_gesamt = len(tau_ha) + len(tau_el) + len(tau_mu) + len(tau_tau)

print("Tau Untergrund:", (len(tau_mu) + len(tau_ha) +
    len(tau_el)
) / Nelectron_gesamt)

print("Tau Akzeptanzverlust:", (len(e_ecal_tau) - len(tau_tau)) /
        len(e_ecal_tau))






#plt.hist(e_hcal, bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
#plt.hist(e_hcal2, bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50],alpha=0.7)
#plt.show()

#plt.hist(e_ecal,
#         bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130])
#plt.hist(e_ecal2,
#         bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130],
#         alpha=0.7)
#plt.show()


