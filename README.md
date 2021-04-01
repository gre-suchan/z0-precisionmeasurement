# z0-precisionmeasurement
Precision measurements and tests of the Standard Model using OPAL data at LEP

# Dependencies
The following programs are required for running our analysis:
- `python` (≥3.6)
- `R` (We use version 4.0.5 but I guess anything your package manager gives should be enough)
- A make utility, e. g. `gnu make`
- `udunits`


For R and python you also require the following packages:
- Python packages: `pandas`, `numpy`, `scipy`, `matplotlib`, `uproot3`
- R packages: `deming`, `dplyr`, `magrittr`, `ggplot2`, `units`

The python packages can be installed either via pip (`pip install <package name>` without `<>`)) or your package manager. The R packages can be installed by running R via `R` and entering `install.packages("<package name>")`. Choose a mirror that is near to you and wait for the installation to finish. Please don't forget the quotes; they are required.

# Running the analysis

To generate all .csv files we use for plotting in our report, run `make all`. This generates the required files in a new directory `plot_data/`

The structure of the first part of our analysis can be viewed [here](./flowchart/part1.pdf). Tabular .csv which contain data from GROPE are read in  in `hists` and `export.r` found in `part1/preliminary_tables/`. `hists.r` was used by us to inspect the GROPE data and try to construct some preliminary cuts. `export.r` on the other hands generates .csv files plotted in our report in `plot_data/part1/hists` and is automatically run by the `make` command.

The structure of the second part of our analysis can be viewed [here](./flowchart/part2.pdf). The purpose of each file is briefly listed below:
- `mc_import.py` contains methods to import the Monte Carlo .root files into a pandas data frame
- `opal_import.py` contains methods to import the real OPAL .root files into a pandas data frame as well as a method to import the correct luminosity data
- `cuts.py` is one of the most important files for analysis as it contains the cuts (with the exception of the s-t-cut) used to select the events. For that it creates a column `guess` in the MC or the OPAL dataframe
- `cosfit.py` is responsible for the fits on the differential cross section of the MC data and contains the lower and upper bounds for the s-t-cuts. Running it shows a plot as well as a calculation for the efficiency of that cut. It also contains the ratio needed to correct the amount of electron s-channel events in `opal_crosssection.py` 
- `s_t_cut.py` imports the lower and upper bounds from `cosfit.py`and provides a method for the s-t-cut
- `efficiencies.py` calculates all efficiencies from the MC data frame as well as their errors
- `matrix_inversion.py` imports the efficiency matrix and inverts it. The error calculation is both done using the exact and the Monte Carlo method. Currently, the further analysis uses the inverse errors from the Monte Carlo method.
- `opal_crosssection.py` calculates the total cross section of the OPAL data for each COM-energy and writes those to four .csv files used for further analysis
- `forward_backward.py` computes the forward-backward scattering of the OPAL data for each COM-energy and writes those to a .csv

After the heavy data processing is finished, further analysis happens in `crossfits.r` (for evaluation of the OPAL cross sections where e.g. lepton universality is checked) and `afb.r` (for analysis of the forward backward scattering to compute the squared sine of the Weinberg angle).
