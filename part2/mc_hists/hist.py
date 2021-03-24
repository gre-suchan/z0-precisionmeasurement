import uproot
import awkward as ak
import numpy as np
import matplotlib.pyplot as plt

path_data = '../../z0decayMC/'

file = uproot.open(path_data + 'ee.root')
ttree_name = 'myTTree'

file[ttree_name].keys()

branches = file[ttree_name].arrays()

print(branches)
var = b'E_ecal'
e_ecal = ak.to_numpy(branches[var])
var4 = b'E_hcal'
e_hcal = ak.to_numpy(branches[var4])

file2 = uproot.open(path_data + 'tt.root')

ttree_name2 = 'myTTree'

file2[ttree_name2].keys()

branches = file2[ttree_name2].arrays()

var2 = b'E_ecal'
e_ecal2 = ak.to_numpy(branches[var2])
var3 = b'E_hcal'
e_hcal2 = ak.to_numpy(branches[var3])

# plt.hist(e_hcal, bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
# plt.hist(e_hcal2, bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50],alpha=0.7)
# plt.show()

plt.hist(e_ecal,
         bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130])
plt.hist(e_ecal2,
         bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130],
         alpha=0.7)
plt.show()
