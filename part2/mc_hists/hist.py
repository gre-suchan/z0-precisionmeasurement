import uproot3 as uproot
import pandas as pd


# Data setup, now in a pandas df
def get_mc_dataframe():
    """Import the *.root files from the z0decayMC folder
    :returns: A pandas data frame

    """

    # Path to the MC submodule
    path_data = '../../z0decayMC/'

    ttree_name = 'myTTree'
    # Set up electron data
    file_el = uproot.open(path_data + 'ee.root')
    file_tau = uproot.open(path_data + 'tt.root')
    file_mu = uproot.open(path_data + 'mm.root')
    file_ha = uproot.open(path_data + 'qq.root')

    branches_el = file_el[ttree_name].arrays(namedecode='utf-8')
    branches_tau = file_tau[ttree_name].arrays(namedecode='utf-8')
    branches_mu = file_mu[ttree_name].arrays(namedecode='utf-8')
    branches_ha = file_ha[ttree_name].arrays(namedecode='utf-8')

    df_el = pd.DataFrame(branches_el)
    df_tau = pd.DataFrame(branches_tau)
    df_mu = pd.DataFrame(branches_mu)
    df_ha = pd.DataFrame(branches_ha)

    df_el['ptype'] = 'e'
    df_tau['ptype'] = 't'
    df_mu['ptype'] = 'm'
    df_ha['ptype'] = 'h'

    df = pd.concat([df_el, df_tau, df_mu, df_ha])
    df['guess'] = 'u'

    return df


def apply_cuts(data: pd.DataFrame):
    """Apply our cuts to the data frame data.

    :data: A pandas df containing Ncharged, Pcharged, guess, E_ecal
    :returns: Absolutely nothing

    """
    # Hadron Cuts This is the first cut we make: All events with more than 7
    # charged tracks are selected to be hadrons.
    data.loc[data['Ncharged'] >= 7, 'guess'] = 'h'

    # Muon Cuts
    # Now we select the muons. For this we require that the energy in the
    # electromagnetic calorimeter E_Ecal is less than 10 while the scalar
    # momentum sum should exceed 70. Physically, these are events featuring
    # charged particles with high momenta which don't deposit a lot of energy
    # in the electromagnetic calorimeter. As some of the particles have a
    # scalar momentum sum of zero, we select those to be muons, too, if all the
    # other requirements were met. Currently, we don't know why the scalar
    # momentum sum is 0 at all, however, we know that those are about 90% Muons

    data.loc[(data['guess'] == 'u') & (data['E_ecal'] < 25) &
             ((data['Pcharged'] >= 70) | (data['Pcharged'] == 0)),
             'guess'] = 'm'

    # Electron Cuts
    # Events with a small number of charged particles but a high amount of
    # energy deposited in the E_Ecal are selected to be electrons.

    data.loc[(data['guess'] == 'u') & (data['E_ecal'] >= 70), 'guess'] = 'e'

    # Tau Cuts
    # Events with low amount of charged particles and medium (i. e.  E_Ecal is
    # in (10 GeV, 66 GeV)) deposit the electromagnetic calorimeter are selected
    # to be taus. Muons (cut 2) are excluded via the momentum requirement;
    # Hadrons (cut 1) via Ncharged.  Note that particles with Ncharged < 7 and
    # E_ecal in (66, 70)  are discarded as we couldn't (yet?) think of a
    # criterion that cleanly selects taus from electrons.

    data.loc[(data['guess'] == 'u') & (data['E_ecal'] < 70) &
             (data['Pcharged'] > 0) & (data['Pcharged'] < 70), 'guess'] = 't'


mc_df = get_mc_dataframe()
apply_cuts(mc_df)

if __name__ == "__main__":
    for key, name in [('h', 'Hadron'), ('m', 'Muon'), ('e', 'Electron'),
                      ('t', 'Tau')]:

        print(
            name + " Cleanliness:",
            sum((mc_df['ptype'] == key) & (mc_df['guess'] == key)) /
            sum(mc_df['guess'] == key))
        print(
            name + " Background:",
            sum((mc_df['guess'] == key) & (mc_df['ptype'] != key)) /
            sum(mc_df['guess'] == key))
        print(
            name + " Acceptance loss:",
            sum((mc_df['ptype'] == key) & (mc_df['guess'] != key)) /
            sum(mc_df['ptype'] == key))
        print(
            name + " Efficiency:",
            sum((mc_df['ptype'] == key) & (mc_df['guess'] == key)) /
            sum(mc_df['ptype'] == key))
