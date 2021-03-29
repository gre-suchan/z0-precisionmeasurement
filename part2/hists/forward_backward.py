import pandas as pd
import matplotlib.pyplot as plt
from mc_import import get_mc_dataframe
from cuts import opal_df

# Read in the luminosity data
lum = pd.read_csv("../../z0DecayData/lumi_files/daten_3.csv")
# print(lum)

# Function to calculate the forward-backward asymmetry for given forward and
# backward cross sections. sig_b refers to the backward and sig_f to the
# forward hemisperes.


def A_FB(sig_b, sig_f):
    return (sig_f - sig_b) / (sig_f + sig_b)


#### MC Data ####

# Initializing the mc dataframe.
mc_df = get_mc_dataframe()

# Cutting out the events of the forward and backward hemisphere respectly.
mc_muon_b = mc_df.loc[(mc_df['ptype'] == 'm') & (mc_df['cos_thet'] < 0) &
                      (mc_df['cos_thet'] > -1)]
mc_muon_f = mc_df.loc[(mc_df['ptype'] == 'm') & (mc_df['cos_thet'] < 1) &
                      (mc_df['cos_thet'] > 0)]

# print(mc_muon_b)

# Calculating the forward and backward cross section using the luminosity for
# the nearest beam energy to the one used in the mc simulations.
mc_sig_b = (1 / lum['lumi'][3]) * len(mc_muon_b)
mc_sig_f = (1 / lum['lumi'][3]) * len(mc_muon_f)

# Calculating the forward-backward asymmetry for the mc data.
mc_afb = A_FB(mc_sig_b, mc_sig_f)
print(mc_afb)

#### OPAL data ####

# Cutting out the events of the forward and backward hemisphere respectly for
# each beam energy.
op_muon_b0 = opal_df.loc[(opal_df['guess'] == 'm') & (opal_df['cos_thet'] < 0)
                         & (opal_df['cos_thet'] > -1) &
                         (opal_df['E_lep'] * 2 < (89.46658 + 88.47630) / 2)]
op_muon_f0 = opal_df.loc[(opal_df['guess'] == 'm') & (opal_df['cos_thet'] < 1)
                         & (opal_df['cos_thet'] > 0) &
                         (opal_df['E_lep'] * 2 < (89.46658 + 88.47630) / 2)]
op_muon_b1 = opal_df.loc[(opal_df['guess'] == 'm') & (opal_df['cos_thet'] < 0)
                         & (opal_df['cos_thet'] > -1) &
                         (opal_df['E_lep'] * 2 > (89.46658 + 88.47630) / 2) &
                         (opal_df['E_lep'] * 2 < (89.46658 + 90.21986) / 2)]
op_muon_f1 = opal_df.loc[(opal_df['guess'] == 'm') & (opal_df['cos_thet'] < 1)
                         & (opal_df['cos_thet'] > 0) &
                         (opal_df['E_lep'] * 2 > (89.46658 + 88.47630) / 2) &
                         (opal_df['E_lep'] * 2 < (89.46658 + 90.21986) / 2)]
op_muon_b2 = opal_df.loc[(opal_df['guess'] == 'm') & (opal_df['cos_thet'] < 0)
                         & (opal_df['cos_thet'] > -1) &
                         (opal_df['E_lep'] * 2 > (89.46658 + 90.21986) / 2) &
                         (opal_df['E_lep'] * 2 < (91.22910 + 90.21986) / 2)]
op_muon_f2 = opal_df.loc[(opal_df['guess'] == 'm') & (opal_df['cos_thet'] < 1)
                         & (opal_df['cos_thet'] > 0) &
                         (opal_df['E_lep'] * 2 > (89.46658 + 90.21986) / 2) &
                         (opal_df['E_lep'] * 2 < (91.22910 + 90.21986) / 2)]
op_muon_b3 = opal_df.loc[(opal_df['guess'] == 'm') & (opal_df['cos_thet'] < 0)
                         & (opal_df['cos_thet'] > -1) &
                         (opal_df['E_lep'] * 2 > (91.22910 + 90.21986) / 2) &
                         (opal_df['E_lep'] * 2 < (91.22910 + 91.96428) / 2)]
op_muon_f3 = opal_df.loc[(opal_df['guess'] == 'm') & (opal_df['cos_thet'] < 1)
                         & (opal_df['cos_thet'] > 0) &
                         (opal_df['E_lep'] * 2 > (91.22910 + 90.21986) / 2) &
                         (opal_df['E_lep'] * 2 < (91.22910 + 91.96428) / 2)]
op_muon_b4 = opal_df.loc[(opal_df['guess'] == 'm') & (opal_df['cos_thet'] < 0)
                         & (opal_df['cos_thet'] > -1) &
                         (opal_df['E_lep'] * 2 > (91.22910 + 91.96428) / 2) &
                         (opal_df['E_lep'] * 2 < (92.96229 + 91.96428) / 2)]
op_muon_f4 = opal_df.loc[(opal_df['guess'] == 'm') & (opal_df['cos_thet'] < 1)
                         & (opal_df['cos_thet'] > 0) &
                         (opal_df['E_lep'] * 2 > (91.22910 + 91.96428) / 2) &
                         (opal_df['E_lep'] * 2 < (92.96229 + 91.96428) / 2)]
op_muon_b5 = opal_df.loc[(opal_df['guess'] == 'm') & (opal_df['cos_thet'] < 0)
                         & (opal_df['cos_thet'] > -1) &
                         (opal_df['E_lep'] * 2 > (92.96229 + 91.96428) / 2) &
                         (opal_df['E_lep'] * 2 < (92.96229 + 93.71362) / 2)]
op_muon_f5 = opal_df.loc[(opal_df['guess'] == 'm') & (opal_df['cos_thet'] < 1)
                         & (opal_df['cos_thet'] > 0) &
                         (opal_df['E_lep'] * 2 > (92.96229 + 91.96428) / 2) &
                         (opal_df['E_lep'] * 2 < (92.96229 + 93.71362) / 2)]
op_muon_b6 = opal_df.loc[(opal_df['guess'] == 'm') & (opal_df['cos_thet'] < 0)
                         & (opal_df['cos_thet'] > -1) &
                         (opal_df['E_lep'] * 2 > (92.96229 + 93.71362) / 2)]
op_muon_f6 = opal_df.loc[(opal_df['guess'] == 'm') & (opal_df['cos_thet'] < 1)
                         & (opal_df['cos_thet'] > 0) &
                         (opal_df['E_lep'] * 2 > (92.96229 + 93.71362) / 2)]

# Calculating the forward and backward cross section.
op_sig_b = []
op_sig_f = []
op_sig_b.append((1 / lum['lumi'][0]) * len(op_muon_b0))
op_sig_f.append((1 / lum['lumi'][0]) * len(op_muon_f0))
op_sig_b.append((1 / lum['lumi'][1]) * len(op_muon_b1))
op_sig_f.append((1 / lum['lumi'][1]) * len(op_muon_f1))
op_sig_b.append((1 / lum['lumi'][2]) * len(op_muon_b2))
op_sig_f.append((1 / lum['lumi'][2]) * len(op_muon_f2))
op_sig_b.append((1 / lum['lumi'][3]) * len(op_muon_b3))
op_sig_f.append((1 / lum['lumi'][3]) * len(op_muon_f3))
op_sig_b.append((1 / lum['lumi'][4]) * len(op_muon_b4))
op_sig_f.append((1 / lum['lumi'][4]) * len(op_muon_f4))
op_sig_b.append((1 / lum['lumi'][5]) * len(op_muon_b5))
op_sig_f.append((1 / lum['lumi'][5]) * len(op_muon_f5))
op_sig_b.append((1 / lum['lumi'][6]) * len(op_muon_b6))
op_sig_f.append((1 / lum['lumi'][6]) * len(op_muon_f6))

# Calculating the forward-backward asymmetry for the mc data.
op_afb = []
for i in range(0, 7):
    op_afb.append(A_FB(op_sig_b[i], op_sig_f[i]))
print(op_afb)

plt.plot(lum['meanenergy'], op_afb)
plt.show()
