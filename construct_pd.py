"""Construct persistence diagram from a "point cloud" (represented as an array)."""

import numpy as np
import diode
import dionysus as d
from read_file import *

def construct_pds(coords, exact = True):
    """
    Coordinates to persistence diagrams.
    Args:
        filename - file type with xyz data (.cif, etc.)
    Returns:
        dgms - persistence diagram objects (dgms[0] is 0d, dgms[1] is 1d, etc.)
    """
    f = get_alpha_shapes(coords, exact)
    f = d.Filtration(f)
    m = get_persistence(f)
    dgms = d.init_diagrams(m, f)
    return dgms

def get_alpha_shapes(coords, exact = True):
    """
    Args:
        coords - matrix with xyz data
    Returns:
        simplices
    """
    return diode.fill_alpha_shapes(coords[:,:3], exact = exact)

def get_persistence(f):
    """
    Args:
        f - filtration
    Returns:
        m - reduced boundary matrix
    """
    m = d.homology_persistence(f)
    return m
