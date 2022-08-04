import matplotlib.pyplot as plt
import numpy as np


def tick_labels(dgm, pixel_size):
    """Convert image units to units of the persistence diagram.

    Args:
        dgm: Array containing (birth, death) points, output of "structure_to_pd function.
        pixel_size: Pixel size resolution for the image (int).
    """
    max_birth = np.max(dgm["birth"])
    max_persistence = np.max(dgm["death"] - dgm["birth"])

    ticks = np.linspace(0, pixel_size, 6)

    ticklabels_x = [(max_birth / pixel_size) * i for i in ticks]
    ticklabels_y = [(max_persistence / pixel_size) * i for i in ticks]

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

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))
    axes[0].scatter(dgm_1d["birth"], dgm_1d["death"])
    axes[0].plot([0, np.max(dgm_1d["death"])], [0, np.max(dgm_1d["death"])])
    axes[0].set_xlabel("Birth")
    axes[0].set_ylabel("Death")
    axes[0].set_title("1D persistence diagram")
    axes[1].scatter(dgm_2d["birth"], dgm_2d["death"])
    axes[1].plot([0, np.max(dgm_2d["death"])], [0, np.max(dgm_2d["death"])])
    axes[1].set_xlabel("Birth")
    axes[1].set_ylabel("Death")
    axes[1].set_title("2D persistence diagram")
    plt.show()
    return None


def plot_pers_images(images, arr_dgms):
    """Take a list of the 1D and 2D persistence images and plot it.

    Args:
        images: List of persistence images to be plotted
        arr_dgms: Contains the persistence diagrams, can be used if wanting to be
        accurate with the tick labels.
    """

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))

    reverse_1d = images[0][::-1, :]
    reverse_2d = images[1][::-1, :]

    ticklabels_x_1d, ticklabels_y_1d = tick_labels(arr_dgms["dim1"], 50)
    ticklabels_x_2d, ticklabels_y_2d = tick_labels(arr_dgms["dim2"], 50)

    oned = axes[0].imshow(reverse_1d, cmap=plt.cm.viridis_r)
    axes[0].invert_yaxis()
    axes[0].set_xticklabels(ticklabels_x_1d)
    axes[0].set_yticklabels(ticklabels_y_1d)
    axes[0].set_xlabel("Birth")
    axes[0].set_ylabel("Persistence")
    axes[0].set_title("1D vectorization")
    twod = axes[1].imshow(reverse_2d, cmap=plt.cm.viridis_r)
    axes[1].invert_yaxis()
    axes[1].set_xticklabels(ticklabels_x_2d)
    axes[1].set_yticklabels(ticklabels_y_2d)
    axes[1].set_xlabel("Birth")
    axes[1].set_ylabel("Persistence")
    axes[1].set_title("2D vectorization")
    plt.colorbar(twod, ax=axes[1])
    plt.tight_layout()
    plt.show()
    return None
