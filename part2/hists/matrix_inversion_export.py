"""
Exports the efficiency matrix and their errors to a .txt file.
Note that running this file probably changes the .txt files indexed in the repo
so make sure not to commit changes to the .txt files
"""
from os import path
import numpy as np
from matrix_inversion import toy_experiments

inverse_means, inverse_errors, hists = toy_experiments()

PATH = '../../plot_data/part2/efficiencies/'
assert path.exists(PATH)


def export_hist(h: np.array, file, header=''):
    """Saves a matplotlib hist object as tabular txt

    :h: The matplotlib histogram
    :file: The name of the output file
    :header: The header of the txt
    :returns: None

    """
    np.savetxt(file,
               np.array(list(zip((h[1][:-1] + h[1][1:]) / 2, h[0]))),
               header=header,
               comments='')


for j in range(4):
    for k in range(4):
        export_hist(hists[j][k], PATH + f'{j}{k}.txt')

with open(PATH + 'fit_means.txt', 'w') as f:
    f.write("{{\"" + "\",\"".join(map(str, inverse_means.flatten())) + "\"}}")

with open(PATH + 'fit_sds.txt', 'w') as f:
    f.write("{{\"" + "\",\"".join(map(str, inverse_errors.flatten())) + "\"}}")
