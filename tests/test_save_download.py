"""
Integration test for save/state downloading functionality.

This test validates that the save download logic correctly handles
filesystem paths and API integration.
"""

import os
import sys
import unittest

# Add parent directory to path to import RomM modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "RomM"))


class TestSaveDownload(unittest.TestCase):
    """Test save download functionality."""

    def test_filesystem_save_paths_muos(self):
        """Test that filesystem correctly generates save paths for muOS."""
        # Mock muOS environment
        from filesystem import Filesystem
        
        # Create a filesystem instance
        fs = Filesystem()
        
        # Temporarily set muOS flag for testing
        original_is_muos = fs.is_muos
        fs.is_muos = True
        
        try:
            # Test save file path
            save_file_path = fs.get_save_file_path("gba")
            self.assertIsNotNone(save_file_path)
            self.assertIn("/MUOS/save/file/", save_file_path)
            
            # Test save state path
            save_state_path = fs.get_save_state_path("gba")
            self.assertIsNotNone(save_state_path)
            self.assertIn("/MUOS/save/state/", save_state_path)
            
            # Verify paths are different
            self.assertNotEqual(save_file_path, save_state_path)
        finally:
            # Restore original value
            fs.is_muos = original_is_muos

    def test_filesystem_save_paths_non_muos(self):
        """Test that filesystem returns None for save paths on non-muOS."""
        from filesystem import Filesystem
        
        # Create a filesystem instance
        fs = Filesystem()
        
        # Temporarily clear muOS flag for testing
        original_is_muos = fs.is_muos
        fs.is_muos = False
        
        try:
            # Test save file path returns None
            save_file_path = fs.get_save_file_path("gba")
            self.assertIsNone(save_file_path)
            
            # Test save state path returns None
            save_state_path = fs.get_save_state_path("gba")
            self.assertIsNone(save_state_path)
        finally:
            # Restore original value
            fs.is_muos = original_is_muos

    def test_save_base_path_sd1(self):
        """Test save base path for SD1."""
        from filesystem import Filesystem
        
        fs = Filesystem()
        original_is_muos = fs.is_muos
        original_current_sd = fs._current_sd
        
        fs.is_muos = True
        fs._current_sd = 1
        
        try:
            base_path = fs.get_save_base_path()
            self.assertIsNotNone(base_path)
            self.assertIn("/mmc/MUOS/save", base_path)
        finally:
            fs.is_muos = original_is_muos
            fs._current_sd = original_current_sd

    def test_save_base_path_sd2(self):
        """Test save base path for SD2 when available."""
        from filesystem import Filesystem
        
        fs = Filesystem()
        original_is_muos = fs.is_muos
        original_current_sd = fs._current_sd
        original_sd2_path = fs._sd2_roms_storage_path
        
        fs.is_muos = True
        fs._current_sd = 2
        fs._sd2_roms_storage_path = "/mnt/sdcard/ROMS"  # Simulate SD2 available
        
        try:
            base_path = fs.get_save_base_path()
            self.assertIsNotNone(base_path)
            self.assertIn("/sdcard/MUOS/save", base_path)
        finally:
            fs.is_muos = original_is_muos
            fs._current_sd = original_current_sd
            fs._sd2_roms_storage_path = original_sd2_path

    def test_api_saves_endpoint_exists(self):
        """Test that the API has the saves endpoint defined."""
        # Read the api.py file to check for saves endpoint
        api_file_path = os.path.join(
            os.path.dirname(__file__), "..", "RomM", "api.py"
        )
        
        with open(api_file_path, "r") as f:
            api_content = f.read()
        
        # Check that _saves_endpoint is defined
        self.assertIn('_saves_endpoint = "api/saves"', api_content)
        
        # Check that download_saves method exists
        self.assertIn("def download_saves(self, rom: Rom)", api_content)


if __name__ == "__main__":
    unittest.main()
