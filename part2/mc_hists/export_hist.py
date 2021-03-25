import numpy as np
import matplotlib.pyplot as plt
from hist import df

ncharged_ha = df.loc[df['ptype'] == 'h', 'Ncharged']
ncharged_el = df.loc[df['ptype'] == 'e', 'Ncharged']
ncharged_mu = df.loc[df['ptype'] == 'm', 'Ncharged']
ncharged_tau = df.loc[df['ptype'] == 't', 'Ncharged']

pcharged_ha = df.loc[df['ptype'] == 'h', 'Pcharged']
pcharged_el = df.loc[df['ptype'] == 'e', 'Pcharged']
pcharged_mu = df.loc[df['ptype'] == 'm', 'Pcharged']
pcharged_tau = df.loc[df['ptype'] == 't', 'Pcharged']

e_ecal_ha = df.loc[df['ptype'] == 'h', 'E_ecal']
e_ecal_el = df.loc[df['ptype'] == 'e', 'E_ecal']
e_ecal_mu = df.loc[df['ptype'] == 'm', 'E_ecal']
e_ecal_tau = df.loc[df['ptype'] == 't', 'E_ecal']

e_hcal_ha = df.loc[df['ptype'] == 'h', 'E_hcal']
e_hcal_el = df.loc[df['ptype'] == 'e', 'E_hcal']
e_hcal_mu = df.loc[df['ptype'] == 'm', 'E_hcal']
e_hcal_tau = df.loc[df['ptype'] == 't', 'E_hcal']

PATH = "../../plot_data/part2/mc_hists/"


def export_hist(h: np.array, file, header=''):
    """Saves a matplotlib hist object as tabular txt

    :h: The matplotlib histogram
    :file: The name of the output file
    :header: The header of the txt
    :returns: None

    """
    np.savetxt(file,
               np.array(list(zip(h[1][:-1], h[1][1:], h[0]))),
               header=header,
               comments='')


ncharged_hist_bin = np.linspace(0, 40, 40)
(ncharged_ha_hist, ncharged_el_hist, ncharged_mu_hist, ncharged_tau_hist) = \
    (plt.hist(ncharged_ha, alpha=.5, bins=ncharged_hist_bin, label='h'),
     plt.hist(ncharged_el, alpha=.5, bins=ncharged_hist_bin, label='e'),
     plt.hist(ncharged_mu, alpha=.5, bins=ncharged_hist_bin, label='m'),
     plt.hist(ncharged_tau, alpha=.5, bins=ncharged_hist_bin, label='t'))

export_hist(ncharged_ha_hist, PATH + 'ncharged_ha.txt')
export_hist(ncharged_el_hist, PATH + 'ncharged_el.txt')
export_hist(ncharged_mu_hist, PATH + 'ncharged_mu.txt')
export_hist(ncharged_tau_hist, PATH + 'ncharged_tau.txt')

if __name__ == "__main__":
    plt.legend()
    plt.show()
    plt.clf()

e_ecal_hist_bin = np.linspace(0, 120, 60)
(e_ecal_ha_hist, e_ecal_el_hist, e_ecal_mu_hist, e_ecal_tau_hist) = \
    (plt.hist(e_ecal_ha, alpha=.5, bins=e_ecal_hist_bin, label='h'),
     plt.hist(e_ecal_el, alpha=.5, bins=e_ecal_hist_bin, label='e'),
     plt.hist(e_ecal_mu, alpha=.5, bins=e_ecal_hist_bin, label='m'),
     plt.hist(e_ecal_tau, alpha=.5, bins=e_ecal_hist_bin, label='t'))

export_hist(e_ecal_ha_hist, PATH + 'e_ecal_ha.txt')
export_hist(e_ecal_el_hist, PATH + 'e_ecal_el.txt')
export_hist(e_ecal_mu_hist, PATH + 'e_ecal_mu.txt')
export_hist(e_ecal_tau_hist, PATH + 'e_ecal_tau.txt')

if __name__ == "__main__":
    plt.legend()
    plt.show()
    plt.clf()

e_hcal_hist_bin = np.linspace(0, 40, 20)
(e_hcal_ha_hist, e_hcal_el_hist, e_hcal_mu_hist, e_hcal_tau_hist) = \
    (plt.hist(e_hcal_ha, alpha=.5, bins=e_hcal_hist_bin, label='h'),
     plt.hist(e_hcal_el, alpha=.5, bins=e_hcal_hist_bin, label='e'),
     plt.hist(e_hcal_mu, alpha=.5, bins=e_hcal_hist_bin, label='m'),
     plt.hist(e_hcal_tau, alpha=.5, bins=e_hcal_hist_bin, label='t'))

export_hist(e_hcal_ha_hist, PATH + 'e_hcal_ha.txt')
export_hist(e_hcal_el_hist, PATH + 'e_hcal_el.txt')
export_hist(e_hcal_mu_hist, PATH + 'e_hcal_mu.txt')
export_hist(e_hcal_tau_hist, PATH + 'e_hcal_tau.txt')

if __name__ == "__main__":
    plt.legend()
    plt.show()
    plt.clf()

pcharged_hist_bin = np.linspace(0, 120, 20)
(pcharged_ha_hist, pcharged_el_hist, pcharged_mu_hist, pcharged_tau_hist) = \
    (plt.hist(pcharged_ha, alpha=.5, bins=pcharged_hist_bin, label='h'),
     plt.hist(pcharged_el, alpha=.5, bins=pcharged_hist_bin, label='e'),
     plt.hist(pcharged_mu, alpha=.5, bins=pcharged_hist_bin, label='m'),
     plt.hist(pcharged_tau, alpha=.5, bins=pcharged_hist_bin, label='t'))

export_hist(pcharged_ha_hist, PATH + 'pcharged_ha.txt')
export_hist(pcharged_el_hist, PATH + 'pcharged_el.txt')
export_hist(pcharged_mu_hist, PATH + 'pcharged_mu.txt')
export_hist(pcharged_tau_hist, PATH + 'pcharged_tau.txt')

if __name__ == "__main__":
    plt.legend()
    plt.show()
    plt.clf()
