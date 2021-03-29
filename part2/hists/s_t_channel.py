import pandas as pd
from cuts import mc_df as df, opal_df
from cosfit import upper_cut
from cosfit import lower_cut


def apply_stcut(data: pd.DataFrame):
    """Apply the cuts for the s channel to the otherwise already cuted data."""

    # Adding a new column defining if it is a s channel electron or not.
    data['s_channel'] = 'u'

    # Doing the actual cut, by now cutting out the part in between -0.9 and 0,
    # which hopefully is a convenient tradeoff between efficiency and data
    # loss.
    data.loc[(data['guess'] == 'e') & (data['cos_thet'] >= lower_cut) &
             (data['cos_thet'] <= upper_cut), 's_channel'] = 's'


final_df = df
apply_stcut(final_df)
apply_stcut(opal_df)

if __name__ == "__main__":
    print(final_df)
