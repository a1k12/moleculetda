# moleculetda
A framework to use topological data analysis to extract topological information
from a structure (e.g., molecule or crystal), which can then be used in
downstream tasks.

## Installation

The library can be installed as follows:

```
pip install moleculetda
```

## Examples

As an example, we will start with the following metal-organic framework (MOF) and
construct topological summaries of all the channels and voids in the structure:

<img src="https://github.com/a1k12/moleculetda/blob/main/examples/figures/str_m4_o1_o1_acs_sym.10.png" width="500">

Persistence diagrams can be generated from an example structure file such as a `.cif` file.

```python
from moleculetda.structure_to_vectorization import structure_to_pd
import matplotlib.pyplot as plt
import numpy as np

filename = 'files/mof_structs/str_m4_o1_o1_acs_sym.10.cif'

# return a dict containing persistence diagrams for different dimensions (1d - channels, 2d - voids)
arr_dgms = structure_to_pd(filename, supercell_size=20)

# plot out the 1d and 2d diagrams
dgm_1d = arr_dgms['dim1']
dgm_2d = arr_dgms['dim2']

plot_pds(dgm_1d, dgm_2d)
```
 ̰
<img src="https://github.com/a1k12/moleculetda/blob/main/examples/figures/1d_2d_pers_diagrams.png" width="750">


Starting from `arr_dgms` (dict storing the persistence diagrams), vectorized representations
can be generated. Axes units are the same as the units of the original structure file:

```python
# initialize parameters for the "image" representation:
# spread: Gaussian spread of the kernel, pixels: size of representation (n, n),
# weighting_type: how to weigh the persistence diagram points
# Optional: specs can be provided to give bounds on the representation
from moleculetda.vectorize_pds import PersImage, pd_vectorization
from moleculetda.plotting import plot_per_images

pim = PersImage(spread=0.15,
            pixels=[50, 50],
            weighting_type = 'identity')

# get both the 1d and 2d representations
images = []
for dim in [1, 2]:
    dgm = arr_dgms[f"dim{dim}"]
    images.append(pd_vectorization(dgm, spread=0.15, weighting='identity', pixels=[50, 50]))

plot_pers_images(images, arr_dgms)
```

<img src="https://github.com/a1k12/moleculetda/blob/main/examples/figures/1d_2d_pers_images.png" width="750">

The resulting 1d and 2d image representations can be used for other tasks.

## Citation

[Aditi S. Krishnapriyan, Maciej Haranczyk, Dmitriy Morozov. Topological Descriptors
Help Predict Guest Adsorption in Nanoporous Materials. J. Phys. Chem. C (2020)](https://pubs.acs.org/doi/abs/10.1021/acs.jpcc.0c01167)

```
@article{doi:10.1021/acs.jpcc.0c01167,
author = {Krishnapriyan, Aditi S. and Haranczyk, Maciej and Morozov, Dmitriy},
title = {Topological Descriptors Help Predict Guest Adsorption in Nanoporous Materials},
journal = {The Journal of Physical Chemistry C},
volume = {124},
number = {17},
pages = {9360-9368},
year = {2020},
doi = {10.1021/acs.jpcc.0c01167},

}
```
[Aditi S. Krishnapriyan, Joseph Montoya, Maciej Haranczyk, Jens Hummelshoej, Dmitriy Morozov. Machine learning with persistent homology and chemical word embeddings improves predictive accuracy and interpretability in metal--organic frameworks. Scientific Reports (2021)](https://www.nature.com/articles/s41598-021-88027-8)
```
@article{krishnapriyan_machine_2021,
  title={Machine learning with persistent homology and chemical word embeddings improves prediction accuracy and interpretability in metal-organic frameworks},
  author={Krishnapriyan, Aditi S and Montoya, Joseph and Haranczyk, Maciej and Hummelsh{\o}j, Jens and Morozov, Dmitriy},
  journal = {Scientific Reports},
  volume = {11},
  numer = {1},
  issn = {2045-2322},
  pages = {8888},
  year={2021},
  doi = {10.1038/s41598-021-88027-8}
}
```
