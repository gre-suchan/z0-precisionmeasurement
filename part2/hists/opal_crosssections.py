from opal_import import get_luminosity_dataframe
from cuts import opal_df
from matrix_inversion import get_cached_inverse
import pandas as pd
import numpy as np

path_data = '../../plot_data/part2/crosssections/'

E_inv, E_inv_err = get_cached_inverse()
lumi_df = get_luminosity_dataframe()

# First, sort opal_df by sqrt(s) for merging
opal_df.sort_values(by='sqrt_s', inplace=True)
# Now, merge the lumi_df from the right so that we can group by meanenergy.
# Note that most of the columns are unnnecessary by now. One can probably
# remove them earlier in order to conserve memory
big_df = pd.merge_asof(opal_df,
                       lumi_df,
                       left_on='sqrt_s',
                       right_on='meanenergy',
                       direction='nearest')
# Remove unknowns
big_df = big_df.loc[big_df['guess'] != 'u']
# Calculate an 'error' on the mean energy by the nearest merging
meanenergy_err = big_df.groupby('meanenergy').agg('std')['sqrt_s']
# Now, group by the rows meanenergy and guess
df = big_df.groupby(['meanenergy', 'guess', 'lumi', 'stat', 'sys',
                     'all']).size().reset_index(name='NTilde')
# 'Merge' the meanenergy_err from the right
df['meanenergy_err'] = meanenergy_err.values.repeat(4)

# Now we carry out the matrix multiplication with E_inv by creating a giant
# block diagonal matrix and multiply that with the NTilde column.
# For that, we turn the guess variable into a categorical variable (why
# wasn't this the case before?) so that there exists an order.
df['guess'] = pd.Categorical(df['guess'], ['e', 'm', 't', 'h'])

# Sort the data frame by the meanenergy and the guess variable.
df.sort_values(by=['meanenergy', 'guess'], inplace=True)

# (Create and) Multiply the block diagonal inverse efficiency matrix...
big_E_inv = np.kron(np.eye(7, dtype=int), E_inv)
big_E_inv_err = np.kron(np.eye(7, dtype=int), E_inv_err)
df['N'] = big_E_inv.dot(df.NTilde)

# ...and divide by the luminosity to obtain the total cross section
df['crosssection'] = df['N'] / df['lumi']

# Now onto the errors. Luckily, as there are no covariances, the error can be
# propagated easily via matrix multiplication
df['N_err'] = np.sqrt(((big_E_inv_err)**2).dot(df['N']**2) +
                      ((big_E_inv)**2).dot(np.sqrt(df['N'])**2))
df['crosssection_err'] = np.sqrt((df['N_err'] / df['lumi'])**2 +
                                 (df['all'] * df['N'] / df['lumi']**2)**2)

# Now, save the data for plotting and fitting
for ptype in ['e', 'm', 't', 'h']:
    df[['meanenergy', 'meanenergy_err', 'crosssection', 'crosssection_err'
        ]].loc[df['guess'] == ptype].to_csv(path_data + ptype + '.csv',
                                            index=False)

if __name__ == "__main__":
    print(df[['meanenergy', 'meanenergy_err', 'crosssection',
              'crosssection_err']].loc[df['guess'] == 'e'])
