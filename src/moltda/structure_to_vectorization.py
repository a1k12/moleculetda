"""Example going from a structure to its vectorized persistence diagrams."""

from pathlib import Path
from typing import Union

from .construct_pd import construct_pds
from .read_file import read_data
from .vectorize_pds import PersImage, diagrams_to_arrays

__all__ = ["structure_to_pd"]


def structure_to_pd(filename: Union[str, Path], supercell_size):
    """Convert structure file to all dimensions of persistence diagrams.

    Args:
        filename: Path to structure file.
        supercell_size: If wanting to create a cubic supercell, specify in Angstrom
        the dimension (i.e. length/width/height).

    Return:
        Dict where persistence diagrams for each dimension can be accessed via 'dim1', 'dim2', etc.

    """
    if supercell_size:
        coords = read_data(filename, size=supercell_size, supercell=True)
    else:
        coords = read_data(filename, size=None, supercell=False)
    dgms = construct_pds(coords)

    arr_dgms = diagrams_to_arrays(dgms)  # convert to array representations
    return arr_dgms
