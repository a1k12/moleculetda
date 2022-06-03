"""Calls that can vectorize a PD,
 such as to be used in an ML algorithm."""

import collections
from typing import List, Tuple

import numpy as np
from loguru import logger
from scipy.stats import multivariate_normal as mvn
from scipy.stats import norm
from sklearn.base import TransformerMixin

__all__ = ["diagrams_to_arrays", "PersImage", "pd_vectorization"]


def diagrams_to_arrays(dgms):
    """Convert persistence diagram objects to persistence diagram arrays."""
    dgm_dtype = np.dtype([("birth", "f4"), ("death", "f4"), ("data", "u4")])
    dgm_arrays = {
        f"dim{dim}": np.array(
            [(np.sqrt(dgm[i].birth), np.sqrt(dgm[i].death), dgm[i].data) for i in range(len(dgm))]
            if dgm
            else [],
            dtype=dgm_dtype,
        )
        for dim, dgm in enumerate(dgms)
    }

    return dgm_arrays


def get_images(
    pd,
    spread: float = 0.2,
    weighting: str = "identity",
    pixels: List[int] = [50, 50],
    specs: List[dict] = None,
):
    images = []
    for dim in [0, 1, 2, 3]:
        dgm = pd[f"dim{dim}"]
        images.append(
            pd_vectorization(
                dgm, spread=spread, weighting=weighting, pixels=pixels, specs=specs[dim]
            )
        )
    return images


class PersImage(TransformerMixin):
    """Generate a persistence image. Modified version of "persim"; github.com/scikit-tda/persim

    Args:
        pixels: Tuple that represents the number of pixels in the returned image along x (birth)
        and y (persistence) axis; pair of ints like (int, int)
        spread: standard deviation of the Gaussian kernel (float)
        specs: dict with parameters for shape of image with respect to diagram domain, for images
        to have a particular range, e.g.:
            { "maxB": float,
             "maxP": float,
             "minBD": float
            }
        kernel_type: Gaussian kernel spread
        weighting_type: weighing scheme for persistence points

    Returns:
        Vectorized persistence image
    """

    def __init__(
        self,
        pixels: Tuple[int, int] = (50, 50),
        spread: float = 0.15,
        specs=None,
        kernel_type="gaussian",
        weighting_type="identity",
    ):

        self.specs = specs
        self.kernel_type = kernel_type
        self.weighting_type = weighting_type
        self.spread = spread
        self.nx_b, self.ny_p = pixels

        logger.debug(
            'PersImage(pixels={}, spread={}, specs={}, kernel_type="{}", weighting_type="{}")'.format(
                pixels, spread, specs, kernel_type, weighting_type
            )
        )

    def transform(self, diagrams: np.array):
        """Convert diagram or list of diagrams to a persistence image.

        Args:
            diagrams - list (or multiple) persistence diagrams [(birth, death)]
        """
        # if diagram is empty, return empty image
        if len(diagrams) == 0:
            return np.zeros((self.nx_b, self.ny_p))
        # if first entry of first entry is not iterable, then diagrams is singular and we need to make it a list of diagrams
        try:
            singular = not isinstance(diagrams[0][0], collections.Iterable)
        except IndexError:
            singular = False

        if singular:
            diagrams = [diagrams]

        dgs = [np.copy(diagram) for diagram in diagrams]

        landscapes = [PersImage.to_landscape(dg) for dg in dgs]

        if not self.specs:
            max_ls = []
            for landscape in landscapes:
                ls = np.vstack((landscape, np.zeros((1, 2))))
                max_ls.append(np.max(ls, axis=0))
            maxB, maxP = np.max(max_ls, axis=0)
            self.specs = {
                "maxB": maxB,
                "maxP": maxP,
                "minBD": np.min(
                    [np.min(np.vstack((landscape, np.zeros((1, 2))))) for landscape in landscapes]
                    + [0]
                ),
            }

        imgs = [self._transform(dgm) for dgm in landscapes]

        # Make sure we return one item.
        if singular:
            imgs = imgs[0]

        return imgs

    def _transform(self, landscape):
        # Define an NxN grid over our landscape
        maxB = self.specs["maxB"]  # maximum birth in the range
        maxP = self.specs["maxP"]  # maximum persistence in the range
        minBD = min(self.specs["minBD"], 0)  # at least show 0, maybe lower

        # Different bins for x and y axis: x by birth, y by persistence
        dx_b = maxB / (self.nx_b)
        dy_p = maxP / (self.ny_p)

        xs_lower = np.linspace(minBD, maxB, self.nx_b)
        xs_upper = np.linspace(minBD, maxB, self.nx_b) + dx_b

        ys_lower = np.linspace(0, maxP, self.ny_p)
        ys_upper = np.linspace(0, maxP, self.ny_p) + dy_p

        weighting = self.weighting(landscape)

        # Define zeros
        img = np.zeros((self.nx_b, self.ny_p))

        # Implement this as a `summed-area table` - it'll be way faster
        spread = self.spread if self.spread else dx_b
        for point in landscape:
            x_smooth = norm.cdf(xs_upper, point[0], spread) - norm.cdf(xs_lower, point[0], spread)
            y_smooth = norm.cdf(ys_upper, point[1], spread) - norm.cdf(ys_lower, point[1], spread)
            img += np.outer(x_smooth, y_smooth) * weighting(point)
        img = img.T[::-1]
        return img

    def weighting(self, landscape=None):
        """Define a weighting function,
        for stability results to hold, the function must be 0 at y=0.
        """

        if landscape is not None:
            if len(landscape) > 0:
                maxy = np.max(landscape[:, 1])
            else:
                maxy = 1

        def linear(interval):
            # linear function of y such that f(0) = 0 and f(max(y)) = 1
            d = interval[1]
            return (1 / maxy) * d if landscape is not None else d

        def identity(interval):
            # identity function, no weighing
            return 1

        if self.weighting_type == "identity":
            return identity

        if self.weighting_type == "linear":
            return linear

        raise NotImplementedError(
            'Weighting type "{}" not implemented.'.format(self.weighting_type)
        )

    def kernel(self, spread=1):
        """Return the kernel for the transformation.
        (ndarray size NxM, ndarray size 1xM) -> ndarray size Nx1
        """

        if self.kernel_type == "gaussian":

            def gaussian(data, pixel):
                return mvn.pdf(data, mean=pixel, cov=spread)

            return gaussian

        raise NotImplementedError("Kernel type {} not implemented".format(self.kernel_type))

    @staticmethod
    def to_landscape(diagram):
        """Convert a diagram to a landscape
        (b,d) -> (b, d-b)
        """
        diagram[:, 1] -= diagram[:, 0]

        return diagram


def pd_vectorization(dgm, spread, weighting, pixels, specs=None):
    """
    Convert persistence diagram array to a vectorized representation.

    Optional: Can add custom specs for scaling the persistence image.

    Args:
        dgm: Array containing (b, d) points of a persistence diagram.
        spread: Gaussian spread.
        weighting: Scheme for weighting points in the persistence diagram.
        pixels: Pixel size of returned persistence image, e.g. [50, 50]
        specs (dict): Dictionary containing maxB, maxP, minBD.
    Return:
        Vectorized representation of a persistence diagram, can be used in
        downstream tasks like machine learning, etc.
    """

    pim = PersImage(spread=spread, pixels=pixels, weighting_type=weighting, specs=specs)

    image = pim.transform([(x["birth"], x["death"]) for x in dgm])

    return image  # vectorized persistence image
