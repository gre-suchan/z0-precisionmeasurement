import uproot
import awkward as ak
import numpy as np
import matplotlib.pyplot as plt

path_data = '../../z0decayMC/'

file_el = uproot.open(path_data + 'ee.root')
ttree_name = 'myTTree'
file_el[ttree_name].keys()
branches_el = file_el[ttree_name].arrays()

e_ecal_el = ak.to_numpy(branches_el[b'E_ecal'])
e_hcal_el = ak.to_numpy(branches_el[b'E_hcal'])


file_tau = uproot.open(path_data + 'tt.root')
ttree_name2 = 'myTTree'
file_tau[ttree_name2].keys()
branches_tau = file_tau[ttree_name2].arrays()

e_ecal_tau = ak.to_numpy(branches_tau[b'E_ecal'])
e_hcal_tau = ak.to_numpy(branches_tau[b'E_hcal'])

# plt.hist(e_hcal, bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
# plt.hist(e_hcal2, bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50],alpha=0.7)
# plt.show()

#plt.hist(e_ecal,
#         bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130])
#plt.hist(e_ecal2,
#         bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130],
#         alpha=0.7)
#plt.show()

angle = ak.to_numpy(branches_el['cos_thru'])
plt.hist(angle)
plt.show()
