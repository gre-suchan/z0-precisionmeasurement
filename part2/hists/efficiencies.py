import numpy as np
from cuts import mc_df as df
from cosfit import efficiency as s_efficiency
from cosfit import err_efficiency as err_sefficiency

ptypes = ['e', 'm', 't', 'h']

mat = np.zeros((4, 4))
err_mat = np.zeros((4, 4))

for i, p1 in enumerate(ptypes):
    for j, p2 in enumerate(ptypes):
        num = sum((df['guess'] == p2) & (df['ptype'] == p1))
        denom = sum(df['ptype'] == p2)
        mat[i, j] = num / denom
        err_mat[i, j] = np.sqrt(num / denom**2 + num**2 / denom**3)

c = s_efficiency * mat[:, 0]
err_mat[:, 0] = \
    c * (err_sefficiency / s_efficiency + err_mat[:, 0] / mat[:, 0])
mat[:, 0] = c

if __name__ == "__main__":
    print(mat)
    print(err_mat)
