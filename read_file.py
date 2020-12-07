"""
Read the appropriate file type and transform accordingly to point cloud data.
"""
import numpy as np
from typing import Tuple

def read_data(filename: str, size=None, supercell=False) -> np.ndarray:
    """
    Args:
        filename - currently supports cif, .npy
        # TO DO: xyz, POSCAR; extended xyz
        size - if creating a cubic supercell, size of the cell
        supercell - if creating a supercell, only supported by ".cif" option for now
    """
    if filename.endswith('.cif'):
        if supercell:
            lattice_matrix, xyz = read_cif(filename)
            return make_supercell(xyz, lattice_matrix, size)
        else:
            return read_cif(filename)[1] # xyz coordinates
    elif filename.endswith('.npy'):
        return np.load(filename)
    else:
        raise("Other file types not implemented.")

    return None

def read_cif(filename: str) -> Tuple[np.ndarray, np.ndarray]:
    from pymatgen   import Structure

    structure = Structure.from_file(filename)
    lattice_matrix = structure.lattice.matrix
    xyz = structure.cart_coords
    return (lattice_matrix, xyz)

def read_xyz(filename: str):
    from pymatgen import Molecule

    coords = Molecule.from_file(filename)
    return coords

def make_supercell(coords, lattice, size, min_size=-5) -> np.ndarray:
    """
    Generate cubic supercell of a given size.

    Args:
        coords - matrix of xyz coordinates of the system
        lattice - lattice constants of the system
        size - dimension size of cubic cell, e.g., 10x10x10
        min_size - minimum axes size to keep negative xyz coordinates from the original cell

    Returns:
        new_cell - supercell array
    """
    a, b, c = lattice

    xyz_periodic_copies = []
    xyz_periodic_copies.append(coords)
    min_range = -3 # we aren't going in the minimum direction too much, so can make this small
    max_range = 20 # make this large enough, but can modify if wanting an even larger cell

    for x in range(-min_range, max_range):
        for y in range(0, max_range):
            for z in range(0, max_range):
                if x == y == z == 0:
                    continue
                add_vector = x*a + y*b + z*c
                xyz_periodic_copies.append(coords + add_vector)

    # Combine into one array
    xyz_periodic_total = np.vstack(xyz_periodic_copies)

    # Filter out all atoms outside of the cubic box
    new_cell = xyz_periodic_total[np.max(xyz_periodic_total[:,:3], axis=1) < size]
    new_cell = new_cell[np.min(new_cell[:,:3], axis=1) > min_size]

    return new_cell
