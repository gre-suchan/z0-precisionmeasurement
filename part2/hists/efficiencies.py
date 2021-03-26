import numpy as np
from cuts import mc_df as df

ptypes = ['e', 'm', 't', 'h']

mat = np.zeros((4, 4))
err_mat = np.zeros((4, 4))

for i, p1 in enumerate(ptypes):
    for j, p2 in enumerate(ptypes):
        num = sum((df['guess'] == p2) & (df['ptype'] == p1))
        denom = sum(df['ptype'] == p2)
        mat[i, j] = num / denom
        err_mat[i, j] = np.sqrt(num / denom**2 + num**2 / denom**3)


if __name__ == "__main__":
    print(mat)
    print(err_mat)
