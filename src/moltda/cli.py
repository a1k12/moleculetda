import click
from loguru import logger

from .construct_pd import construct_pds
from .read_file import read_data
from .vectorize_pds import diagrams_to_arrays


@click.command("cli")
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    "--supercell-size",
    "-s",
    default=None,
    help="Size of supercell. Use if wanting all systems to be a certain cubic size. Only works if lattice constants exist.",
    type=click.INT,
)
@click.option(
    "--spread",
    "-sp",
    default=0.15,
    help="Gaussian spread for vectorizing persistence diagram transformation.",
    type=click.FLOAT,
)
def file2diagrams(file, supercell_size, spread):
    """
    Convert a molecule/structurefile to vecotrized persistence diagrams.
    """
    sc = True if supercell_size else False
    coords = read_data(file, size=supercell_size, supercell=sc)
    dgms = construct_pds(coords)

    np_dgms = diagrams_to_arrays(dgms)
    print(np_dgms)
    # separate dgms into 0D, 1D, 2D
    dgm_0d = np_dgms["dim0"]
    dgm_1d = np_dgms["dim1"]
    dgm_2d = np_dgms["dim2"]
