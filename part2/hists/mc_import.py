import pandas as pd
import uproot3 as uproot


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
