import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from opal_import import get_luminosity_dataframe
from mc_import import get_mc_dataframe
from cuts import opal_df
from matrix_inversion import get_cached_inverse


# Read in the luminosity data
lum = get_luminosity_dataframe()
# Corrections for the forward-backward asymmetry (no units)
rad_corr = [0.021512, 0.019262, 0.016713, 0.018293, 0.030286, 0.062196,
            0.093850]
# Inversed efficiency matrix and the errors.
mat_eff, mat_err = get_cached_inverse()


# Function to calculate the forward-backward asymmetrie for given forward and
# backward cross sections.
def A_FB(N_f, N_b):
    return (N_f - N_b) / (N_f + N_b)


# Error calculation of the forward-backward asymmetrie.
def err_afb(N_f_err, N_b_err, N_f, N_b):
    return (A_FB(N_b, N_f) * np.sqrt((N_f_err / (N_f + N_b))**2 +
            (N_b_err / (N_f + N_b))**2 + ((N_f - N_b) / (N_f + N_b)**2
            * N_b_err)**2 + ((N_f - N_b) / (N_f + N_b)**2 * N_f_err)**2))


# Function to calculate the sin squared of the weinberg angle out of the
# forward-backward asymmetrie.
def sin_W(A_FB):
    return 0.25 * (1 - np.sqrt(np.abs(A_FB) / 3))


def err_sinW(sin_W, A_FB, err_AFB):
    return (sin_W * np.sqrt((err_AFB / (8 * np.sqrt(3 * np.abs(A_FB))))**2))


# Function to calculate the errors for the real event number.
def Num_error(N, eff, eff_err):
    return (N * eff_err + np.sqrt(N) * eff)


# MC Data ##################################################################

# Initializing the mc dataframe.
MC_df = get_mc_dataframe()

# Cutting out the events of the forward and backward hemisphere respectly.
MC_muonb = MC_df.loc[(MC_df['ptype'] == 'm') & (MC_df['cos_thet'] < 0) &
                     (MC_df['cos_thet'] > -1)]
MC_muonf = MC_df.loc[(MC_df['ptype'] == 'm') & (MC_df['cos_thet'] < 1) &
                     (MC_df['cos_thet'] > 0)]

# Calculating the forward and backward cross section using the luminosity for
# the nearest beam energy to the one used in the mc simulations.
# Number of muon events in the forward region
MC_N_f = len(MC_muonf)
# Number of muon events in the backward region
MC_N_b = len(MC_muonb)
# Estimate the error on both using the square root (this is a counting
# experiment with a sufficiently low error rate)
MC_N_f_err = np.sqrt(MC_N_f)
MC_N_b_err = np.sqrt(MC_N_b)

# Calculating the forward-backward asymmetry for the mc data.
MC_afb = A_FB(MC_N_f, MC_N_b) + rad_corr[3]
MC_afb_err = err_afb(MC_N_f_err, MC_N_b_err, MC_N_f, MC_N_b)
# Calculatin the sin squared of the weinberg angle
MC_sin = sin_W(MC_afb)
MC_sin_err = err_sinW(MC_sin, MC_afb, MC_afb_err)

if __name__ == "__main__":
    # Printing the MC data.
    print("MC data:")
    print("A_FB, error A_FB, sin(theta_W)**2, err sin")
    print(MC_afb, MC_afb_err, MC_sin, MC_sin_err)

#### OPAL data ################################################################

# Sorting the opal data into forward and backward data and the different beam
# energies, by the new collumns hemisphere and lum_beam.
opal_df['hemisphere'] = 'u'
opal_df['lum_beam'] = 'u'

opal_df.loc[(opal_df['cos_thet'] < 0) & (opal_df['cos_thet'] > -1), 'hemisphere'] = 'b'
opal_df.loc[(opal_df['cos_thet'] < 1) & (opal_df['cos_thet'] > 0),
    'hemisphere'] = 'f'

opal_df.loc[(opal_df['E_lep'] * 2 < (89.46658 + 88.47630) / 2), 'lum_beam'] = lum['lumi'][0]
opal_df.loc[(opal_df['E_lep'] * 2 > (89.46658 + 88.47630) / 2) &
(opal_df['E_lep'] * 2 < (89.46658 + 90.21986) / 2), 'lum_beam'] = lum['lumi'][1]
opal_df.loc[(opal_df['E_lep'] * 2 > (89.46658 + 90.21986) / 2) &
(opal_df['E_lep'] * 2 < (91.22910 + 90.21986) / 2), 'lum_beam'] = lum['lumi'][2]
opal_df.loc[(opal_df['E_lep'] * 2 > (91.22910 + 90.21986) / 2) &
(opal_df['E_lep'] * 2 < (91.22910 + 91.96428) / 2), 'lum_beam'] = lum['lumi'][3]
opal_df.loc[(opal_df['E_lep'] * 2 > (91.22910 + 91.96428) / 2) &
(opal_df['E_lep'] * 2 < (92.96229 + 91.96428) / 2), 'lum_beam'] = lum['lumi'][4]
opal_df.loc[(opal_df['E_lep'] * 2 > (92.96229 + 91.96428) / 2) &
(opal_df['E_lep'] * 2 < (92.96229 + 93.71362) / 2), 'lum_beam'] = lum['lumi'][5]
opal_df.loc[(opal_df['E_lep'] * 2 > (92.96229 + 93.71362) / 2), 'lum_beam'] = lum['lumi'][6]

# Calculating the number of muon events for each sorted event.
N_forward = []
N_backward = []
for i in range(0, 7):
   N_forward.append(len(opal_df[(opal_df['hemisphere'] == 'f') & (opal_df['lum_beam'] ==
   lum['lumi'][i]) & (opal_df['guess'] == 'e')]) * mat_eff[1][0] 
   + len(opal_df[(opal_df['hemisphere'] == 'f') & (opal_df['lum_beam'] ==
   lum['lumi'][i]) & (opal_df['guess'] == 'm')]) * mat_eff[1][1] 
   + len(opal_df[(opal_df['hemisphere'] == 'f') & (opal_df['lum_beam'] ==
   lum['lumi'][i]) & (opal_df['guess'] == 't')]) * mat_eff[1][2]
   + len(opal_df[(opal_df['hemisphere'] == 'f') & (opal_df['lum_beam'] ==
   lum['lumi'][i]) & (opal_df['guess'] == 'h')]) * mat_eff[1][3])
   N_backward.append(len(opal_df[(opal_df['hemisphere'] == 'b') & (opal_df['lum_beam'] ==
   lum['lumi'][i]) & (opal_df['guess'] == 'e')]) * mat_eff[1][0] 
   + len(opal_df[(opal_df['hemisphere'] == 'b') & (opal_df['lum_beam'] ==
   lum['lumi'][i]) & (opal_df['guess'] == 'm')]) * mat_eff[1][1] 
   + len(opal_df[(opal_df['hemisphere'] == 'b') & (opal_df['lum_beam'] ==
   lum['lumi'][i]) & (opal_df['guess'] == 't')]) * mat_eff[1][2]
   + len(opal_df[(opal_df['hemisphere'] == 'b') & (opal_df['lum_beam'] ==
   lum['lumi'][i]) & (opal_df['guess'] == 'h')]) * mat_eff[1][3])

# Calculating the error for the number of events
Nerr_b = []
Nerr_f = []
for i in range(0, 7):
    Nerr_b.append(Num_error(len(opal_df[(opal_df['hemisphere'] == 'b') &
        (opal_df['lum_beam'] == lum['lumi'][i]) & (opal_df['guess'] == 'e')]),
        mat_eff[1][0], mat_err[1][0])
        + Num_error(len(opal_df[(opal_df['hemisphere'] == 'b') &
        (opal_df['lum_beam'] == lum['lumi'][i]) & (opal_df['guess'] == 'm')]),
        mat_eff[1][1], mat_err[1][1])
        + Num_error(len(opal_df[(opal_df['hemisphere'] == 'b') &
        (opal_df['lum_beam'] == lum['lumi'][i]) & (opal_df['guess'] == 't')]),
        mat_eff[1][2], mat_err[1][2])
        + Num_error(len(opal_df[(opal_df['hemisphere'] == 'b') &
        (opal_df['lum_beam'] == lum['lumi'][i]) & (opal_df['guess'] == 'h')]),
        mat_eff[1][3], mat_err[1][3]))
    Nerr_f.append(Num_error(len(opal_df[(opal_df['hemisphere'] == 'f') &
        (opal_df['lum_beam'] == lum['lumi'][i]) & (opal_df['guess'] == 'e')]),
        mat_eff[1][0], mat_err[1][0])
        + Num_error(len(opal_df[(opal_df['hemisphere'] == 'f') &
        (opal_df['lum_beam'] == lum['lumi'][i]) & (opal_df['guess'] == 'm')]),
        mat_eff[1][1], mat_err[1][1])
        + Num_error(len(opal_df[(opal_df['hemisphere'] == 'f') &
        (opal_df['lum_beam'] == lum['lumi'][i]) & (opal_df['guess'] == 't')]),
        mat_eff[1][2], mat_err[1][2])
        + Num_error(len(opal_df[(opal_df['hemisphere'] == 'f') &
        (opal_df['lum_beam'] == lum['lumi'][i]) & (opal_df['guess'] == 'h')]),
        mat_eff[1][3], mat_err[1][3]))

# Calculating the forward and backward cross section and the errors.
O_sigb = []
O_sigf = []
Oerr_sigb = []
Oerr_sigf = []
for i in range(0, 7):
    O_sigb.append(N_backward[i] / lum['lumi'][i])
    O_sigf.append(N_forward[i] / lum['lumi'][i])
    Oerr_sigb.append(O_sigb[i] / lum['lumi'][i] * lum['all'][i] +
            Nerr_b[i] / lum['lumi'][i])
    Oerr_sigf.append(O_sigf[i] / lum['lumi'][i] * lum['all'][i] +
            Nerr_f[i] / lum['lumi'][i])

# Calculating the forward-backward asymmetry for the opal data and the errors.
O_afb = []
Oerr_afb = []
for i in range(0,7):
    O_afb.append(A_FB(O_sigb[i], O_sigf[i]) + rad_corr[i])
    Oerr_afb.append(err_afb(Oerr_sigb[i], Oerr_sigf[i], O_sigb[i],
        O_sigf[i]))

# Calculating sin squared of the weinberg angle.
O_sin = []
Oerr_sin = []
for i in range(0,7):
    O_sin.append(sin_W(O_afb[i]))
    Oerr_sin.append(err_sinW(O_sin[i], O_afb[i], Oerr_afb[i]))

if __name__ == "__main__":
    # Print data
    print("Opal data:")
    print("A_FB, error A_FB, sin(theta_W)**2, err sin")
    for i in range(0, 7):
        print(O_afb[i], Oerr_afb[i], O_sin[i], Oerr_sin[i])
