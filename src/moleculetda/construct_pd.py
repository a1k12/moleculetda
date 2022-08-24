"""Construct persistence diagram from a "point cloud" (represented as an array)."""

from typing import Iterable, Optional, Tuple

import diode
import dionysus as d
import numpy as np


def construct_pds(
    coords: np.ndarray,
    exact: bool = True,
    periodic: bool = False,
    weights: Optional[Iterable] = None,
) -> Tuple[d.Diagram]:
    """
    Coordinates to persistence diagrams.
    Args:
        coords (np.ndarray): point cloud represented as an array
        exact (bool): if True, use exact alpha shapes
        periodic (bool): if True, use periodic alpha shapes
        weights (Iterable, optional): weights for each point,
            e.g. atomic radii for each point

    Returns:
        dgms: persistence diagram objects (dgms[0] is 0d, dgms[1] is 1d, etc.)
    """
    f = get_alpha_shapes(coords, exact, periodic=periodic, weights=weights)
    f = d.Filtration(f)
    m = get_persistence(f)
    dgms = d.init_diagrams(m, f)
    return dgms


def get_alpha_shapes(
    coords: np.ndarray, exact=True, periodic=False, weights: Optional[Iterable] = None
):
    """
    Args:
        coords (np.ndarray): matrix with xyz data
        periodic (bool): if True, use periodic alpha shapes
        weights (Iterable, optional): weights for each point,
            e.g. atomic radii for each point

    Returns:
        simplices
    """
    if weights is not None:
        if len(weights) != len(coords):
            raise ValueError("weights must be the same length as coords")
    if periodic:
        if weights is not None:
            return diode.fill_weighted_periodic_alpha_shapes(
                np.hstack((coords, np.array(weights).reshape(-1, 1))), exact=exact
            )
        return diode.fill_periodic_alpha_shapes(coords, exact=False)

    if weights is not None:
        return diode.fill_weighted_alpha_shapes(
            np.hstack((coords, np.array(weights).reshape(-1, 1))), exact=exact
        )
    return diode.fill_alpha_shapes(coords, exact=exact)


def get_persistence(f: d.Filtration):
    """
    Args:
        f: filtration
    Returns:
        m: reduced boundary matrix
    """
    m = d.homology_persistence(f)
    return m
