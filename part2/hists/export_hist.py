import numpy as np
import matplotlib.pyplot as plt
from cuts import mc_df, opal_df

mc_df_zero_momentum = mc_df.loc[mc_df['Pcharged'] == 0]

MC_PATH = "../../plot_data/part2/mc_hists/"
MC_ZERO_MOMENTUM_PATH = "../../plot_data/part2/mc_hists_zero_momentum/"
OPAL_PATH = "../../plot_data/part2/opal_hists/"


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


# Plot tec.ratio for MC data to show that its not a good selection criterion
mc_df['ratio'] = mc_df['Pcharged'] / mc_df['E_ecal']
ratio_ha = mc_df.loc[mc_df['guess'] == 'h', 'ratio']
ratio_el = mc_df.loc[mc_df['guess'] == 'e', 'ratio']
ratio_mu = mc_df.loc[mc_df['guess'] == 'm', 'ratio']
ratio_tau = mc_df.loc[mc_df['guess'] == 't', 'ratio']

ratio_hist_bin = np.linspace(0, 8, 81)
ratio_ha_hist, ratio_el_hist, ratio_mu_hist, ratio_tau_hist = \
    (plt.hist(ratio_ha, alpha=.5, bins=ratio_hist_bin, label='h'),
     plt.hist(ratio_el, alpha=.5, bins=ratio_hist_bin, label='e'),
     plt.hist(ratio_mu, alpha=.5, bins=ratio_hist_bin, label='m'),
     plt.hist(ratio_tau, alpha=.5, bins=ratio_hist_bin, label='t'))

export_hist(ratio_ha_hist, MC_PATH + 'ratio_ha.txt')
export_hist(ratio_el_hist, MC_PATH + 'ratio_el.txt')
export_hist(ratio_mu_hist, MC_PATH + 'ratio_mu.txt')
export_hist(ratio_tau_hist, MC_PATH + 'ratio_tau.txt')

for df, var, PATH in [(mc_df, 'ptype', MC_PATH),
                      (mc_df_zero_momentum, 'ptype', MC_ZERO_MOMENTUM_PATH),
                      (opal_df, 'guess', OPAL_PATH)][:-3]:
    # Don't actually show the plots
    PLOTTING = False

    ncharged_ha = df.loc[df[var] == 'h', 'Ncharged']
    ncharged_el = df.loc[df[var] == 'e', 'Ncharged']
    ncharged_mu = df.loc[df[var] == 'm', 'Ncharged']
    ncharged_tau = df.loc[df[var] == 't', 'Ncharged']

    pcharged_ha = df.loc[df[var] == 'h', 'Pcharged']
    pcharged_el = df.loc[df[var] == 'e', 'Pcharged']
    pcharged_mu = df.loc[df[var] == 'm', 'Pcharged']
    pcharged_tau = df.loc[df[var] == 't', 'Pcharged']

    e_ecal_ha = df.loc[df[var] == 'h', 'E_ecal']
    e_ecal_el = df.loc[df[var] == 'e', 'E_ecal']
    e_ecal_mu = df.loc[df[var] == 'm', 'E_ecal']
    e_ecal_tau = df.loc[df[var] == 't', 'E_ecal']

    e_hcal_ha = df.loc[df[var] == 'h', 'E_hcal']
    e_hcal_el = df.loc[df[var] == 'e', 'E_hcal']
    e_hcal_mu = df.loc[df[var] == 'm', 'E_hcal']
    e_hcal_tau = df.loc[df[var] == 't', 'E_hcal']

    cos_ha = df.loc[df[var] == 'h', 'cos_thru']
    cos_el = df.loc[df[var] == 'e', 'cos_thet']
    cos_mu = df.loc[df[var] == 'm', 'cos_thet']
    cos_tau = df.loc[df[var] == 't', 'cos_thet']

    ncharged_hist_bin = np.linspace(0, 40, 41)
    (ncharged_ha_hist, ncharged_el_hist, ncharged_mu_hist, ncharged_tau_hist) = \
        (plt.hist(ncharged_ha, alpha=.5, bins=ncharged_hist_bin, label='h'),
         plt.hist(ncharged_el, alpha=.5, bins=ncharged_hist_bin, label='e'),
         plt.hist(ncharged_mu, alpha=.5, bins=ncharged_hist_bin, label='m'),
         plt.hist(ncharged_tau, alpha=.5, bins=ncharged_hist_bin, label='t'))

    export_hist(ncharged_ha_hist, PATH + 'ncharged_ha.txt')
    export_hist(ncharged_el_hist, PATH + 'ncharged_el.txt')
    export_hist(ncharged_mu_hist, PATH + 'ncharged_mu.txt')
    export_hist(ncharged_tau_hist, PATH + 'ncharged_tau.txt')

    if __name__ == "__main__" and PLOTTING:
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

    if __name__ == "__main__" and PLOTTING:
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

    if __name__ == "__main__" and PLOTTING:
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

    if __name__ == "__main__" and PLOTTING:
        plt.legend()
        plt.show()
        plt.clf()

    cos_hist_bin = np.linspace(-1, 1, 21)
    (cos_el_hist, cos_mu_hist, cos_tau_hist, cos_ha_hist) =\
        (plt.hist(cos_el, alpha=.5, bins=cos_hist_bin, label='e'),
         plt.hist(cos_mu, alpha=.5, bins=cos_hist_bin, label='e'),
         plt.hist(cos_tau, alpha=.5, bins=cos_hist_bin, label='e'),
         plt.hist(cos_ha, alpha=.5, bins=cos_hist_bin, label='e'))
    cos_el_hist_fine = plt.hist(cos_el, bins=np.linspace(-1, 1, 360))
    export_hist(cos_el_hist, PATH + 'cos_el.txt')
    export_hist(cos_el_hist_fine, PATH + 'cos_el_fine.txt')
    export_hist(cos_mu_hist, PATH + 'cos_mu.txt')
    export_hist(cos_tau_hist, PATH + 'cos_tau.txt')
    export_hist(cos_ha_hist, PATH + 'cos_ha.txt')

    if __name__ == "__main__" and PLOTTING:
        plt.legend()
        plt.show()
        plt.clf()

    hist2d_mu, xh_mu, yh_mu, _ = plt.hist2d(pcharged_mu,
                                            e_ecal_mu,
                                            bins=20,
                                            range=[[0, 120], [0, 100]])
    x_mu_ = (xh_mu[1:] + xh_mu[:-1]) / 2
    y_mu_ = (yh_mu[1:] + yh_mu[:-1]) / 2

    x_mu = np.tile(x_mu_, len(y_mu_))
    y_mu = np.repeat(y_mu_, len(x_mu_))
    np.savetxt(PATH + 'hist2d_mu.txt',
               np.array([x_mu, y_mu, hist2d_mu.flatten()]).T)

    hist2d_tau, xh_tau, yh_tau, ___ = plt.hist2d(pcharged_tau,
                                                 e_ecal_tau,
                                                 bins=20,
                                                 range=[[0, 120], [0, 100]])
    x_tau_ = (xh_tau[1:] + xh_tau[:-1]) / 2
    y_tau_ = (yh_tau[1:] + yh_tau[:-1]) / 2

    x_tau = np.tile(x_tau_, len(y_tau_))
    y_tau = np.repeat(y_tau_, len(x_tau_))
    np.savetxt(PATH + 'hist2d_tau.txt',
               np.array([x_tau, y_tau, hist2d_tau.flatten()]).T)
    # np.savetxt(PATH + 'hist2d_mu.txt', hist2d_mu)
    # np.savetxt(PATH + 'hist2d_tau.txt', hist2d_tau)
    if __name__ == "__main__" and PLOTTING:
        plt.show()
        plt.clf()
