# molecule-tda
A framework to use topological data analysis to extract topological information
from a structure (e.g., molecular or crystal), which can then be used in
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

```
@article{krishnapriyan2020persistent,
  title={Persistent homology advances interpretable machine learning for nanoporous materials},
  author={Krishnapriyan, Aditi S and Montoya, Joseph and Hummelsh{\o}j, Jens and Morozov, Dmitriy},
  journal={arXiv preprint arXiv:2010.00532},
  year={2020}
}
```
[Aditi S. Krishnapriyan, Joseph Montoya, Maciej Haranczyk, Jens Hummelshoej.
Persistence homology advances interpretable machine learning for nanoporous materials.
Arxiv, 2010.00532 (2020)](https://arxiv.org/abs/2010.00532)
