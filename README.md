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

```
Aditi S. Krishnapriyan, Maciej Haranczyk, Dmitriy Morozov. Topological Descriptors
Help Predict Guest Adsorption in Nanoporous Materials. J. Phys. Chem. C (2020)
```
[doi](https://pubs.acs.org/doi/abs/10.1021/acs.jpcc.0c01167)


```
Aditi S. Krishnapriyan, Joseph Montoya, Maciej Haranczyk, Jens Hummelshoej.
Persistence homology advances interpretable machine learning for nanoporous materials.
Arxiv, 2010.00532.
```
[doi](https://arxiv.org/abs/2010.00532)
