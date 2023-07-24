import unittest

from builder.config import os_paths


class TestConfig(unittest.TestCase):
    def test_os_paths_existence(self):
        # Test if os_paths is a dictionary and not empty
        self.assertIsInstance(os_paths, dict)
        self.assertTrue(os_paths)

    def test_os_paths_keys(self):
        # Test if os_paths contains the expected operating system keys
        expected_keys = {"Windows", "Linux", "Darwin"}
        self.assertEqual(set(os_paths.keys()), expected_keys)

    def test_os_paths_values(self):
        # Test if os_paths values are dictionaries with the expected keys
        expected_values = {
            "Windows": {"UNPACKER": "win32/asset_unpacker.exe", "PACKER": "win32/asset_packer.exe"},
            "Linux": {"UNPACKER": "linux/asset_unpacker", "PACKER": "linux/asset_packer"},
            "Darwin": {"UNPACKER": "osx/asset_unpacker", "PACKER": "osx/asset_packer"},
        }
        for key in os_paths:
            self.assertEqual(os_paths[key], expected_values[key])


if __name__ == '__main__':
    unittest.main()
