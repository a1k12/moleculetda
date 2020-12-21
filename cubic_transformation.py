from pymatgen import Structure
from pymatgen.transformations.transformation_abc import AbstractTransformation

import numpy as np

__author__ = "Jimmy-Xuan Shen"
__email__ = "jmmshn@gmail.com"


class CubicTransformation(AbstractTransformation):
    """
    A transformation that generates a cubic cell from a given structure without
    with no regard for the periodic boundary conditions of the large cell.

    The algorithm starts at the (0,0,0) cell and checks the cells in (+/- 1,+/- 1,+/- 1) directions
    and performs a depth-first search to completely tile the space.

    For each new cell to being considered we only move to the next cell in the same direction if at least one atom
    in the current cell is inside of the cube

    An atom at position is considered to be in the cubic cell
    (whose lattice vectors are a0, a1, a2 in units of the UC lattice)
    p . cross_product[i] > 0 & p . cross_product[i] - box_product[i] < 0
    Where the definition for each coordinate of the cross and box product are:
    cross_product :
    0 -> a1 x a2
    1 -> a2 x a0
    2 -> a0 x a1

    box_product:
    0 -> a0 . a1 x a2
    1 -> a1 . a2 x a0
    2 -> a2 . a0 x a1
    """

    def __init__(self, side_length: float):
        """
        Args:
            side_length:
        """
        self.side_length = side_length

    def apply_transformation(self, structure):

        n_dim = len(structure.lattice.matrix)  # should just be 3

        target_sc_lat_vecs = np.eye(n_dim, n_dim) * self.side_length
        sc_mat = np.linalg.inv(structure.lattice.matrix) @ target_sc_lat_vecs

        cross_product = np.array([np.cross(sc_mat[(i + 1) % n_dim], sc_mat[(i + 2) % n_dim]) for i in range(n_dim)])
        box_product = np.array([np.dot(sc_mat[i], cross_product[i]) for i in range(n_dim)])

        big_struct = Structure(lattice=target_sc_lat_vecs, species=[], coords=[])

        def is_inside(p):
            """
            Once the cross_product and box_product has been defined we can check if a given point is inside the cell
            """
            p_cross_a = cross_product @ p.T
            for i in range(n_dim):
                if p_cross_a[i] < 0 or p_cross_a[i] > box_product[i]:
                    return False
            return True

        def yield_atoms_in_sc(*ijk):
            """
            Force the supercell to have the same origin as the unit cell.
            For the unit cell indexed by (a,b,c), yield all of the points inside the SC

            For the three vectors, take the cross product of cyclic pairs cyclic pairs
            """
            for isite in structure.sites:
                p = isite.frac_coords + np.array([*ijk])
                if is_inside(p):
                    yield 0, isite.species_string, np.dot(structure.lattice.matrix, p)

        def check_cell(a, b, c):
            """
            check the cell at (a,b,c) return True if found any atoms inside
            add atoms found within the big cell as we do the checks
            """
            to_insert = [*yield_atoms_in_sc(a, b, c)]
            if len(to_insert) == 0:
                return False
            else:
                for insert_params in to_insert:
                    big_struct.insert(*insert_params, coords_are_cartesian=True)
                return True

        # do DFS
        seent = set()
        queue = [(0, 0, 0)]
        while queue:
            cur = queue.pop()
            if check_cell(*cur):
                seent.add(cur)
                for diff in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
                    new_cell = tuple(cur[d_] + diff[d_] for d_ in range(3))
                    if new_cell not in seent:
                        queue.append(new_cell)

        return big_struct.get_sorted_structure()

    @property
    def inverse(self):
        return None

    @property
    def is_one_to_many(self):
        return False
