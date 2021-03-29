import pandas as pd
import numpy as np
import uproot3 as uproot

# Import method for opal data


def get_opal_dataframe():
    """Import the *.root file from the z0DecayData folder
    :returns: A pandas data frame

    """

    # Path to the OPAL data submodule
    path = '../../z0DecayData/daten_3.root'
    file = uproot.open(path)
    df = pd.DataFrame(file['myTTree'].arrays(namedecode='utf-8'))
    df['sqrt_s'] = 2 * df['E_lep']
    df['guess'] = 'u'

    return df


def get_luminosity_dataframe():
    """Import the luminosity file from z0DecayData/lumi_files/daten_3.csv'
    :returns: A pandas df

    """
    path = '../../z0DecayData/lumi_files/daten_3.csv'
    return pd.read_csv(path, dtype=np.float32)


if __name__ == "__main__":
    print(get_luminosity_dataframe())
