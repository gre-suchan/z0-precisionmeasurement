import numpy as np
from hist import df

ptypes = ['e', 'm', 't', 'h']

mat = np.zeros((4, 4))

for i, p1 in enumerate(ptypes):
    for j, p2 in enumerate(ptypes):
        if i == j:
            mat[i, j] = sum((df['ptype'] == p1) & (df['guess'] == p1)) / \
                sum(df['ptype'] == p1)
        else:
            mat[i, j] = sum((df['guess'] == p1) & (df['ptype'] == p2)) / \
                sum(df['guess'] == p1)

print(mat)
