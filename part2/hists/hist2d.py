import matplotlib.pyplot as plt
from cuts import mc_df as df
# from hist import pcharged_ha, pcharged_el, pcharged_mu, pcharged_tau, \
#     e_ecal_ha, e_ecal_el, e_ecal_mu, e_ecal_tau, branches_mu, branches_el

plt.subplot(4, 2, 1)
plt.hist(df.loc[(df['ptype'] == 'e') & (df['cos_thet'] < 2), 'Pcharged'],
         range=[0, 120])
plt.subplot(4, 2, 3)
plt.hist(df.loc[(df['ptype'] == 'e') & (df['cos_thet'] < 2), 'E_ecal'],
         range=[0, 120])
plt.subplot(4, 2, 5)
plt.hist(df.loc[(df['ptype'] == 'e') & (df['cos_thet'] < 2), 'E_hcal'],
         range=[0, 10])
plt.subplot(4, 2, 7)
plt.hist(df.loc[(df['ptype'] == 'e') & (df['cos_thet'] < 2), 'Ncharged'],
         range=[0, 10])

plt.subplot(4, 2, 2)
plt.hist(df.loc[(df['ptype'] == 'e') & (df['cos_thet'] > 2), 'Pcharged'],
         range=[0, 120])
plt.subplot(4, 2, 4)
plt.hist(df.loc[(df['ptype'] == 'e') & (df['cos_thet'] > 2), 'E_ecal'],
         range=[0, 120])
plt.subplot(4, 2, 6)
plt.hist(df.loc[(df['ptype'] == 'e') & (df['cos_thet'] > 2), 'E_hcal'],
         range=[0, 10])
plt.subplot(4, 2, 8)
plt.hist(df.loc[(df['ptype'] == 'e') & (df['cos_thet'] > 2), 'Ncharged'],
         range=[0, 10])

plt.show()
