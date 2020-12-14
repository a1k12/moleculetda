# molecule-tda
A framework to use topological data analysis to extract topological information
from a structure (e.g., molecule or crystal), which can then be used in
downstream tasks.

## Installation

Installation of all necessary packages can either be done via `poetry` or through
setup.py. All required packages are in requirements.txt. For example:

```
git clone git@github.com:a1k12/molecule-tda.git
cd molecule-tda
pip install .
```

## Examples

`structure_to_vectorization.py` contains functions that allow generating
an example persistence diagram vectorization from a structure file
(which can then be used in other tasks, e.g., fed into a machine learning algorithm).

Persistence diagrams can be generated from an example structure file such as a .cif file:

```
from structure_to_vectorization import *
import matplotlib.pyplot as plt
import numpy as np

filename = 'files/mof_structs/str_m4_o1_o1_acs_sym.10.cif'

# return a dict containing persistence diagrams for different dimensions (1d - channels, 2d - voids)
arr_dgms = structure_to_pd(filename, supercell_size=None)

# plot out the 1d and 2d diagrams
dgm_1d = arr_dgms['dim1']
dgm_2d = arr_dgms['dim2']

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))
axes[0].scatter(dgm_1d['birth'], dgm_1d['death'])
axes[0].plot([0, np.max(dgm_1d['death'])], [0, np.max(dgm_1d['death'])])
axes[0].set_xlabel('Birth')
axes[0].set_ylabel('Death')
axes[0].set_title('1D persistence diagram')
axes[1].scatter(dgm_2d['birth'], dgm_2d['death'])
axes[1].plot([0, np.max(dgm_2d['death'])], [0, np.max(dgm_2d['death'])])
axes[1].set_xlabel('Birth')
axes[1].set_ylabel('Death')
axes[1].set_title('2D persistence diagram')
plt.show()
```
<img src="https://github.com/a1k12/figures/1d_2d_pers_diagrams.png" width="750">


Starting from `arr_dgms` (array corresponding to the persistence diagrams), vectorized representations
can be generated:
```
# initialize parameters for the "image" representation:
# spread: Gaussian spread of the kernel, pixels: size of representation (n, n),
# weighting_type: how to weigh the persistence diagram points
# Optional: specs can be provided to give bounds on the representation

pim = PersImage(spread=0.15,
            pixels=[50, 50],
            weighting_type = 'identity',
            verbose=False)

# get both the 1d and 2d representations
images = []
for dim in [1, 2]:
    dgm = arr_dgms[f"dim{dim}"]
    images.append(pd_vectorization(dgm, spread=0.15, weighting='identity', pixels=[50, 50]))

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))

reverse_1d = images[0][::-1, :]
reverse_2d = images[1][::-1, :]

oned = axes[0].imshow(reverse_1d, cmap=plt.cm.viridis_r)
axes[0].invert_yaxis()
axes[0].set_xlabel('Birth')
axes[0].set_ylabel('Persistence')
axes[0].set_title('1D vectorization')
twod = axes[1].imshow(reverse_2d, cmap=plt.cm.viridis_r)
axes[1].invert_yaxis()
axes[1].set_xlabel('Birth')
axes[1].set_ylabel('Persistence')
axes[1].set_title('2D vectorization')
plt.colorbar(twod, ax=axes[1])
plt.show()
```
<img src="https://github.com/a1k12/figures/1d_2d_pers_images.png" width="750">

The resulting 1d and 2d image representations can be used for other tasks.

## Citing

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
[Aditi S. Krishnapriyan, Joseph Montoya, Maciej Haranczyk, Jens Hummelshoej, Dmitriy Morozov.
Persistence homology advances interpretable machine learning for nanoporous materials.
Arxiv, 2010.00532 (2020)](https://arxiv.org/abs/2010.00532)

```
@article{krishnapriyan2020persistent,
  title={Persistent homology advances interpretable machine learning for nanoporous materials},
  author={Krishnapriyan, Aditi S and Montoya, Joseph and Haranczyk, Maciej and Hummelsh{\o}j, Jens and Morozov, Dmitriy},
  journal={arXiv preprint arXiv:2010.00532},
  year={2020}
}
```
