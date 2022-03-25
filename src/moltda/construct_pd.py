"""Construct persistence diagram from a "point cloud" (represented as an array)."""

from typing import Tuple

import diode
import dionysus as d
import numpy as np


def construct_pds(coords: np.ndarray, exact: bool = True) -> Tuple[d.Diagram]:
    """
    Coordinates to persistence diagrams.
    Args:
        coords (np.ndarray): point cloud represented as an array
    Returns:
        dgms: persistence diagram objects (dgms[0] is 0d, dgms[1] is 1d, etc.)
    """
    f = get_alpha_shapes(coords, exact)
    f = d.Filtration(f)
    m = get_persistence(f)
    dgms = d.init_diagrams(m, f)
    return dgms


def get_alpha_shapes(coords: np.ndarray, exact=True):
    """
    Args:
        coords (np.ndarray): matrix with xyz data
    Returns:
        simplices
    """
    return diode.fill_alpha_shapes(coords[:, :3], exact=exact)


def get_persistence(f: d.Filtration):
    """
    Args:
        f: filtration
    Returns:
        m: reduced boundary matrix
    """
    m = d.homology_persistence(f)
    return m
