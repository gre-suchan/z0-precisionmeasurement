import pandas as pd
import numpy as np
from opal_import import get_luminosity_dataframe
from mc_import import get_mc_dataframe
from cuts import opal_df as opal_df2
from matrix_inversion import get_cached_inverse

# Corrections for the forward-backward asymmetry (no units)
rad_corr = [
    0.021512, 0.019262, 0.016713, 0.018293, 0.030286, 0.062196, 0.093850
]


# Function to calculate the forward-backward asymmetrie for given forward and
# backward cross sections.
def A_FB(N_f, N_b):
    return (N_f - N_b) / (N_f + N_b)


# Error calculation of the forward-backward asymmetrie.
def A_FB_err(N_f_err, N_b_err, N_f, N_b):
    return (A_FB(N_f, N_b) *
            np.sqrt((N_f_err / (N_f + N_b))**2 + (N_b_err / (N_f + N_b))**2 +
                    ((N_f - N_b) / (N_f + N_b)**2 * N_b_err)**2 +
                    ((N_f - N_b) / (N_f + N_b)**2 * N_f_err)**2))


# Function to calculate the sin squared of the weinberg angle out of the
# forward-backward asymmetrie.
def sin_W(A_FB):
    return 0.25 * (1 - np.sqrt(np.abs(A_FB) / 3))


def sin_W_err(sin_W, A_FB, err_AFB):
    return (sin_W * np.sqrt((err_AFB / (8 * np.sqrt(3 * np.abs(A_FB))))**2))


# Function to calculate the errors for the real event number.
def Num_error(N, eff, eff_err):
    return (N * eff_err + np.sqrt(N) * eff)


# Data Import
opal_df = opal_df2.copy()  # I hate pandas (copying is necessary)
lum = get_luminosity_dataframe()
# Inversed efficiency matrix and the errors.
E_inv, E_inv_err = get_cached_inverse()
path_data = '../../plot_data/part2/forward_backward/'

# MC Data ##################################################################

# Initializing the mc dataframe.
MC_df = get_mc_dataframe()

# Cutting out the events of the forward and backward hemisphere respectly.
MC_muon_b = MC_df.loc[(MC_df['ptype'] == 'm') & (MC_df['cos_thet'] < 0) &
                      (MC_df['cos_thet'] > -1)]
MC_muon_f = MC_df.loc[(MC_df['ptype'] == 'm') & (MC_df['cos_thet'] < 1) &
                      (MC_df['cos_thet'] > 0)]

# Calculating the forward and backward cross section using the luminosity for
# the nearest beam energy to the one used in the mc simulations.
# Number of muon events in the forward/backward region
MC_N_f = len(MC_muon_f)
MC_N_b = len(MC_muon_b)
# Estimate the error on both using the square root (this is a counting
# experiment with a sufficiently low error rate)
MC_N_f_err = np.sqrt(MC_N_f)
MC_N_b_err = np.sqrt(MC_N_b)

# Calculating the forward-backward asymmetry and sin^2 for the mc data.
MC_afb = A_FB(MC_N_f, MC_N_b) + rad_corr[3]
MC_afb_err = A_FB_err(MC_N_f_err, MC_N_b_err, MC_N_f, MC_N_b)
MC_sin = sin_W(MC_afb)
MC_sin_err = sin_W_err(MC_sin, MC_afb, MC_afb_err)

if __name__ == "__main__":
    # Printing the MC data.
    print("MC data:")
    print("A_FB, error A_FB, sin(theta_W)**2, err sin")
    print(MC_afb, MC_afb_err, MC_sin, MC_sin_err)

# OPAL data

# Sorting the opal data into forward and backward data and the different beam
# energies, by the new column hemisphere.
# Further, set categorical variables.
opal_df['hemisphere'] = 'u'
opal_df.loc[(opal_df['cos_thet'] < 0) & (opal_df['cos_thet'] > -1),
            'hemisphere'] = 'b'
opal_df.loc[(opal_df['cos_thet'] < 1) & (opal_df['cos_thet'] > 0),
            'hemisphere'] = 'f'
opal_df = opal_df.loc[opal_df['hemisphere'] != 'u']
opal_df['guess'] = pd.Categorical(opal_df['guess'], ['e', 'm', 't', 'h'])
opal_df['hemisphere'] = pd.Categorical(opal_df['hemisphere'], ['f', 'b'])

# Integrate the luminosity data frame. While we don't need the luminosity for
# the calculation of A_FB, the correction terms are only available for the
# seven energy observations found in the luminosity data frame so we merge the
# two just as in opal_crosssections.py
opal_df.sort_values(by='sqrt_s', inplace=True)
opal_df = pd.merge_asof(opal_df,
                        lum,
                        left_on='sqrt_s',
                        right_on='meanenergy',
                        direction='nearest')
# Calculate an 'error' on the mean energy by the nearest merging
meanenergy_err = opal_df.groupby('meanenergy').agg('std')['sqrt_s']
# Now, group by the rows meanenergy and guess
df = opal_df.groupby(['hemisphere', 'meanenergy',
                      'guess']).size().reset_index(name='NTilde')

# Sort the data frame by the hemisphere, the meanenergy and the guess variable.
df.sort_values(by=['hemisphere', 'meanenergy', 'guess'], inplace=True)
# (Create and) Multiply the block diagonal inverse efficiency matrix...
big_E_inv = np.kron(np.eye(14, dtype=int), E_inv)
big_E_inv_err = np.kron(np.eye(14, dtype=int), E_inv_err)
df['N'] = big_E_inv.dot(df.NTilde)
# Fix some frequencies to be zero (this is the result of discarding some values
# based on their cosine)
df.loc[df['N'] < 0, 'N'] = 0
# Calculate the error on N_err
df['N_err'] = np.sqrt(((big_E_inv_err)**2).dot(df['N']**2) +
                      ((big_E_inv)**2).dot(np.sqrt(df['N']**2)))

# Discard every non-muonic events
df = df[df['guess'] == 'm']
# Convert hemisphere observation to variable
df = pd.pivot_table(df,
                    values=['N', 'N_err'],
                    index='meanenergy',
                    columns='hemisphere')

# Calculate the forward backward asymmetry and the sin^2 of the Weinberg angle
# and their respective errors
# These three lines I don't understand tbh
df.columns = df.columns.get_level_values(0)
df.reset_index(inplace=True)
df.columns = ['meanenergy', 'Nf', 'Nb', 'Nferr', 'Nberr']

df['A_FB'] = A_FB(df['Nf'], df['Nb']) + rad_corr
df['A_FB_err'] = A_FB_err(df['Nferr'], df['Nberr'],
                                     df['Nf'], df['Nb'])
df['sin_W'] = sin_W(df['A_FB'])
df['sin_W_err'] = sin_W_err(df['sin_W'], df['A_FB'], df['A_FB_err'])

# df = df.assign(A_FB=A_FB(df[('N', 'f')], df[('N', 'b')]) + rad_corr,
#                A_FB_err=A_FB_err(df[('N_err', 'f')], df[('N_err', 'b')],
#                                  df[('N', 'f')], df[('N', 'b')]))
# df = df.assign(sin_W=sin_W(df['A_FB']))
# df = df.assign(sin_W_err=sin_W_err(df['sin_W'], df['A_FB'], df['A_FB_err']))
df['meanenergy_err'] = meanenergy_err.values

df.to_csv(path_data + "A_FB.csv", index=False)

if __name__ == "__main__":
    print(df)
