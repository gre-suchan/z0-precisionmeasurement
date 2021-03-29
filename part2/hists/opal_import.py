import pandas as pd
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
    df['guess'] = 'u'

    return df


if __name__ == "__main__":
    print(get_opal_dataframe())
