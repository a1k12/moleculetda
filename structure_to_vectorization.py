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

def tick_labels(dgm, pixel_size):
    """Convert image units to units of the persistence diagram.

    Args:
        dgm: Array containing (birth, death) points, output of "structure_to_pd function.
        pixel_size: Pixel size resolution for the image (int).
    """
    max_birth = np.max(dgm['birth'])
    max_persistence = np.max(dgm['death'] - dgm['birth'])

    ticks = np.linspace(0, pixel_size, 6)

    ticklabels_x = [(max_birth/pixel_size)*i for i in ticks]
    ticklabels_y = [(max_persistence/pixel_size)*i for i in ticks]

    ticklabels_x = [round(elem, 2) for elem in ticklabels_x]
    ticklabels_y = [round(elem, 2) for elem in ticklabels_y]

    # start from (0, 0)
    ticklabels_x.insert(0, 0)
    ticklabels_y.insert(0, 0)

    return ticklabels_x, ticklabels_y

def plot_pds(dgm_1d, dgm_2d):
    """Plot persistence diagrams here for visualization, example includes 1D and 2D.

    Args:
        dgm_1d, dgm_2d: 1d and 2d persistence diagrams
    """
    import matplotlib.pyplot as plt

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
    return None

def plot_pers_images(images, arr_dgms):
    """Take a list of the 1D and 2D persistence images and plot it.

    Args:
        images: List of persistence images to be plotted
        arr_dgms: Contains the persistence diagrams, can be used if wanting to be
        accurate with the tick labels.
    """

    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))

    reverse_1d = images[0][::-1, :]
    reverse_2d = images[1][::-1, :]

    ticklabels_x_1d, ticklabels_y_1d = tick_labels(arr_dgms['dim1'], 50)
    ticklabels_x_2d, ticklabels_y_2d = tick_labels(arr_dgms['dim2'], 50)

    oned = axes[0].imshow(reverse_1d, cmap=plt.cm.viridis_r)
    axes[0].invert_yaxis()
    axes[0].set_xticklabels(ticklabels_x_1d)
    axes[0].set_yticklabels(ticklabels_y_1d)
    axes[0].set_xlabel('Birth')
    axes[0].set_ylabel('Persistence')
    axes[0].set_title('1D vectorization')
    twod = axes[1].imshow(reverse_2d, cmap=plt.cm.viridis_r)
    axes[1].invert_yaxis()
    axes[1].set_xticklabels(ticklabels_x_2d)
    axes[1].set_yticklabels(ticklabels_y_2d)
    axes[1].set_xlabel('Birth')
    axes[1].set_ylabel('Persistence')
    axes[1].set_title('2D vectorization')
    plt.colorbar(twod, ax=axes[1])
    plt.tight_layout()
    plt.show()
    return None

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
