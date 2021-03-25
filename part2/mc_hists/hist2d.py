import matplotlib.pyplot as plt
from hist import df
# from hist import pcharged_ha, pcharged_el, pcharged_mu, pcharged_tau, \
#     e_ecal_ha, e_ecal_el, e_ecal_mu, e_ecal_tau, branches_mu, branches_el

# angle = angle_el[branches_el['cos_thet'] < 2]

plt.subplot(2, 2, 1)
plt.hist2d(df.loc[df['ptype'] == 'e', 'E_ecal'],
           df.loc[df['ptype'] == 'e', 'Pcharged'],
           range=[[0, 120], [0, 120]])
plt.subplot(2, 2, 2)
plt.hist2d(df.loc[df['ptype'] == 'm', 'E_ecal'],
           df.loc[df['ptype'] == 'm', 'Pcharged'],
           range=[[0, 120], [0, 120]])
plt.subplot(2, 2, 3)
plt.hist2d(df.loc[df['ptype'] == 't', 'E_ecal'],
           df.loc[df['ptype'] == 't', 'Pcharged'],
           range=[[0, 120], [0, 120]])
plt.subplot(2, 2, 4)

plt.hist2d(df.loc[df['ptype'] == 't', 'E_ecal'],
           df.loc[df['ptype'] == 't', 'Pcharged'],
           range=[[0, 120], [0, 120]])

plt.show()
