# sculptor-dwarf-galaxy-gaiadr3
Code to reproduce Sculptor galaxy membership selection described in [Tolstoy et al (2023)](https://doi.org/10.1051/0004-6361/202245717)

## Folders in this repository
* `data/` Contains the input data. Table E1 from the paper is included. The Gaia data must be downloaded first in FITS format
  (see [notebook](SculptorGaiaMemberSelect.ipynb)).
* `memdata/` Contains the output membership tables after running the notebook.
* `img/` Contains plots produced with the notebook, specifically the ones that were used in the paper.

## Python dependencies
* [NumPy](https://numpy.org/)
* [SciPy](https://scipy.org/)
* [Matplotlib](https://matplotlib.org/) 
* [Astropy](https://www.astropy.org/)
* [PyGaia](https://pypi.org/project/PyGaia/)
* [gaiadr3_zeropoint](https://gitlab.com/icc-ub/public/gaiadr3_zeropoint)
