import os

import pytest

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture()
def mof_path():
    return os.path.join(THIS_DIR, "test_files", "str_m4_o1_o1_acs_sym.10.cif")
