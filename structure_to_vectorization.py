"""Example going from a structure to its vectorized persistence diagrams."""

from read_file import *
from construct_pd import *
from vectorize_pds import *

def structure_to_pd(filename, supercell_size):
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

    arr_dgms = diagrams_to_arrays(dgms) # convert to array representations
    return arr_dgms

def pd_vectorization(dgm, spread, weighting, pixels):
    """
    Convert persistence diagram array to a vectorized representation.

    Optional: Can add custom specs for scaling the persistence image.

    Args:
        dgm: Array containing (b, d) points of a persistence diagram.
        spread: Gaussian spread.
        weighting: Scheme for weighting points in the persistence diagram.
        pixels: Pixel size of returned persistence image, e.g. [50, 50]

    Return:
        Vectorized representation of a persistence diagram, can be used in
        downstream tasks like machine learning, etc.
    """

    pim = PersImage(spread=spread,
                pixels=pixels,
                weighting_type = weighting,
                verbose=False)

    image = pim.transform([(x['birth'], x['death']) for x in dgm])

    return image # vectorized persistence image

def main(filename, supercell_size=None, spread=0.15, weighting='identity', pixels=[50, 50]):
    """Structure file to vectorized persistence diagram presentation.
    Currently returns a list with the 1D and 2D persistence diagrams of a structure.
    """

    arr_dgms = structure_to_pd(filename, supercell_size)
    images = []
    for dim in [1, 2]:
        dgm = arr_dgms[f"dim{dim}"]
        images.append(pd_vectorization(dgm, spread, weighting, pixels))

    return images

if __name__ == '__main__':
    filename = 'files/mof_structs/str_m4_o1_o1_acs_sym.10.cif'
    images = main(filename, None, 0.15, 'identity', [50, 50])
