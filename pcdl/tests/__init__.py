import unittest

from pcdl.tests import test_grid
from pcdl.tests import test_svg


loader = unittest.TestLoader()
suite = unittest.TestSuite((
    loader.loadTestsFromModule(test_grid),
    loader.loadTestsFromModule(test_svg),
))
