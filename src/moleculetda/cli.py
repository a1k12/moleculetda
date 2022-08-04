from ast import dump
from pathlib import Path

import click
from loguru import logger

from .construct_pd import construct_pds
from .io import dump_json
from .read_file import read_data
from .vectorize_pds import diagrams_to_arrays, pd_vectorization


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
@click.option(
    "--maxB",
    default=18,
    help="Maximum birth value for persistence diagram vectorization.",
    type=click.FLOAT,
)
@click.option(
    "--maxP",
    default=18,
    help="Maximum persistence value for persistence diagram vectorization.",
    type=click.FLOAT,
)
@click.option(
    "--minB",
    default=0,
    help="Minimum birth value for persistence diagram vectorization.",
    type=click.FLOAT,
)
def main(filename, supercell_size, spread, maxB, maxP, minB):
    """
    Convert a molecule/structurefile to vecotrized persistence diagrams.
    """
    file = Path(filename)
    sc = True if supercell_size else False
    coords = read_data(file, size=supercell_size, supercell=sc)
    dgms = construct_pds(coords)

    np_dgms = diagrams_to_arrays(dgms)

    images = []
    for dim in [0, 1, 2, 3]:
        dgm = np_dgms[f"dim{dim}"]
        images.append(
            pd_vectorization(
                dgm,
                spread=spread,
                weighting="identity",
                pixels=[50, 50],
                specs={"maxB": maxB, "maxP": maxP, "minBD": minB},
            )
        )

    result = {
        "diagrams": np_dgms,
        "images": images,
    }

    dump_json(result, f"{file.stem}_result.json")
