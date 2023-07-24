import os
import shutil
import tempfile
import unittest
from unittest import mock

import click
import json5 as json
import jsonpatch
from parameterized import parameterized

from builder.helpers import (copy_file, create_patch_file,
                             set_unpacker_packer_paths)


class TestHelpers(unittest.TestCase):
    @classmethod
    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.source_dir = os.path.join(self.temp_dir, "source")
        self.mod_dir = os.path.join(self.temp_dir, "mod")
        self.build_dir = os.path.join(self.temp_dir, "build")
        os.makedirs(self.source_dir)
        os.makedirs(self.mod_dir)
        os.makedirs(self.build_dir)

    @classmethod
    def tearDown(self):
        # Clean up the temporary directory after testing
        shutil.rmtree(self.temp_dir)

    def test_create_patch_file_identical_files(self):
        # Create test files with different content
        file_content = '{"somevar": 40}'
        mod_content = '{"somevar": 40}'

        file_path = os.path.join(self.source_dir, "file.config")
        mod_path = os.path.join(self.mod_dir, "file.config")

        with open(file_path, "w") as f:
            f.write(file_content)

        with open(mod_path, "w") as f:
            f.write(mod_content)

        # Call create_patch_file function
        dst_path = os.path.join(self.build_dir, "file.config")
        create_patch_file(self.source_dir, mod_path, dst_path, self.mod_dir)

        # Assert that the patch file is empty
        self.assertEqual(os.path.getsize(dst_path+".patch"), 2)

    def test_create_patch_file_different_files(self):
        # Create test files with different content
        file_content = '{"somevar": 40}'
        mod_content = '{"somevar": 50}'

        file_path = os.path.join(self.source_dir, "file.config")
        mod_path = os.path.join(self.mod_dir, "file.config")

        with open(file_path, "w") as f:
            f.write(file_content)

        with open(mod_path, "w") as f:
            f.write(mod_content)

        # Call create_patch_file function
        dst_path = os.path.join(self.build_dir, "file.config")
        create_patch_file(self.source_dir, mod_path, dst_path, self.mod_dir)

        # Assert that the patch file is not empty and contains valid JSON patch data
        self.assertGreater(os.path.getsize(dst_path+".patch"), 4)
        with open(dst_path+".patch", "r") as f:
            patch_data = f.read()
            new_patched = jsonpatch.apply_patch(
                json.loads(file_content), patch_data)
            self.assertDictEqual(json.loads(mod_content), new_patched)
            # Add your assertion tests here for the patch_data

    def test_copy_file(self):
        # Create a test file
        src_file = os.path.join(self.temp_dir, "original.txt")
        dst_file = os.path.join(self.temp_dir, "copied.txt")
        with open(src_file, "w") as f:
            f.write("Test content")

        # Call copy_file function
        copy_file(src_file, dst_file)

        # Your assertion tests for copy_file
        self.assertTrue(os.path.exists(dst_file))
        with open(dst_file, "r") as f:
            content = f.read()
            self.assertEqual(content, "Test content")

    @parameterized.expand([
        ('Windows', 'starbound/win32/asset_unpacker.exe',
         'starbound/win32/asset_packer.exe'),
        ('Linux', 'starbound/linux/asset_unpacker', 'starbound/linux/asset_packer'),
        ('Darwin', 'starbound/osx/asset_unpacker', 'starbound/osx/asset_packer'),
        ('invalid_platform', None, None)
    ])
    @mock.patch('platform.system')
    def test_set_unpacker_packer_paths(self, platform_name, expected_unpacker, expected_packer, mock_system):
        mock_system.return_value = platform_name

        class ctxMock:
            obj: dict
            command: object

        ctx = ctxMock
        ctx.obj = {}
        ctx.command = None
        if (expected_packer == None and expected_unpacker == None):
            with self.assertRaises(click.UsageError):
                set_unpacker_packer_paths(ctx, "starbound")
        else:
            set_unpacker_packer_paths(ctx, "starbound")
            self.assertEqual(ctx.obj["UNPACKER"],
                             os.path.abspath(expected_unpacker))
            self.assertEqual(ctx.obj["PACKER"],
                             os.path.abspath(expected_packer))


if __name__ == '__main__':
    unittest.main()
