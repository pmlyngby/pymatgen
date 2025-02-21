import numpy as np

from pymatgen.io.vasp.optics import DielectricFunctionCalculator
from pymatgen.io.vasp.outputs import Vasprun
from pymatgen.util.testing import PymatgenTest

__author__ = "Jimmy-Xuan Shen"
__copyright__ = "Copyright 2022, The Materials Project"
__email__ = "jmmshn@gmail.com"


class VasprunTest(PymatgenTest):
    def test_optics(self):
        eps_data_path = self.TEST_FILES_DIR / "reproduce_eps"
        vrun = Vasprun(eps_data_path / "vasprun.xml")
        dfc = DielectricFunctionCalculator.from_directory(eps_data_path)
        egrid, eps = dfc.get_epsilon(0, 0)

        _, eps_real_ref, eps_imag_ref = vrun.dielectric
        eps_real_ref = np.array(eps_real_ref)[:, 0]
        eps_imag_ref = np.array(eps_imag_ref)[:, 0]
        assert np.max(np.abs(eps_real_ref - np.real(eps))) / np.max(np.abs(np.real(eps))) < 0.01

        _, eps = dfc.get_epsilon(0, 1)
        assert np.max(np.abs(eps)) < 0.1
