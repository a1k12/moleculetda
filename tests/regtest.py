import numpy as np
import pytest

from moleculetda.structure_to_vectorization import structure_to_pd


def test_regression_mof_tda(mof_path, hkust_paths):
    """Regression test for the TDA calculation."""
    dgms = structure_to_pd(mof_path, supercell_size=10)
    assert isinstance(dgms, dict)
    assert len(dgms) == 4
    assert list(dgms.keys()) == ["dim0", "dim1", "dim2", "dim3"]
    assert isinstance(dgms["dim1"], np.ndarray)

    dgms = structure_to_pd(mof_path, supercell_size=10, periodic=True)
    assert isinstance(dgms, dict)
    assert len(dgms) == 4
    assert list(dgms.keys()) == ["dim0", "dim1", "dim2", "dim3"]
    assert isinstance(dgms["dim1"], np.ndarray)

    dgms_hkust_1 = structure_to_pd(hkust_paths[0], supercell_size=10)
    dgms_hkust_2 = structure_to_pd(hkust_paths[1], supercell_size=10)

    assert dgms_hkust_1["dim1"] == pytest.approx(dgms_hkust_2["dim1"])

    dgms_hkust_1 = structure_to_pd(hkust_paths[0], supercell_size=10, weighted=True)
    dgms_hkust_2 = structure_to_pd(hkust_paths[1], supercell_size=10, weighted=True)

    assert dgms_hkust_1["dim1"] != pytest.approx(dgms_hkust_2["dim1"])
