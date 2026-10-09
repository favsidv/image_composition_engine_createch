"""Check that the shared filter file works outside the project package."""

from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from image_composition_engine_createch import contracts, filters


class FilterPortabilityTests(unittest.TestCase):
    def test_contract_reexports_the_same_base_class(self):
        self.assertIs(contracts.Filter, filters.Filter)

    def test_copied_file_runs_without_importing_the_project(self):
        script = """
import sys
import numpy as np

sys.path.insert(0, sys.argv[1])
from filters import Brightness, Contrast, Invert, Blur, GaussianBlur

for dtype in (np.float32, np.float64):
    image = np.full((3, 4, 3), 0.3, dtype=dtype)
    before = image.copy()
    operations = [
        (Brightness(0.1), 0.4),
        (Contrast(2), 0.1),
        (Invert(), 0.7),
        (Blur(1), 0.3),
        (GaussianBlur(1, 1.0), 0.3),
    ]
    for operation, expected in operations:
        result = operation.apply(image)
        assert result.shape == image.shape
        assert result.dtype == dtype
        assert not np.shares_memory(result, image)
        np.testing.assert_allclose(result, expected, atol=1e-6)
        np.testing.assert_array_equal(image, before)

for image, error_type in [
    (np.zeros((1, 1, 3), dtype=np.uint8), TypeError),
    (np.zeros((1, 1, 4)), ValueError),
    (np.zeros((0, 1, 3)), ValueError),
    (np.full((1, 1, 3), np.nan), ValueError),
    (np.full((1, 1, 3), 2.0), ValueError),
]:
    try:
        Brightness(0).apply(image)
    except error_type:
        pass
    else:
        raise AssertionError('Invalid input was accepted.')

assert not any(
    name == 'image_composition_engine_createch'
    or name.startswith('image_composition_engine_createch.')
    for name in sys.modules
)
"""
        with TemporaryDirectory() as directory:
            shutil.copyfile(Path(filters.__file__), Path(directory) / "filters.py")
            result = subprocess.run(
                [sys.executable, "-I", "-c", script, directory],
                cwd=directory,
                capture_output=True,
                text=True,
                timeout=30,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
