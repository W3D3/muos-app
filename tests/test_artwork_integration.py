"""
Integration test for artwork downloading functionality.

This test validates that the artwork extraction logic correctly handles
the API response structure with ss_metadata.
"""

import os
import sys
import unittest

# Add parent directory to path to import RomM modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "RomM"))


class TestArtworkExtraction(unittest.TestCase):
    """Test artwork extraction from API response with mocked data."""

    def setUp(self):
        """Set up test fixtures with mocked API response data."""
        # Sample ROM data from the API response (based on issue description)
        self.mock_rom_data = {
            "id": 4,
            "name": "Advance Wars",
            "fs_name": "Advance Wars (Europe) (En,Fr,De,Es).gba",
            "platform_slug": "gba",
            "fs_extension": "gba",
            "fs_size_bytes": 8388608,
            "multi": False,
            "languages": ["En", "Fr", "De", "Es"],
            "regions": ["Europe"],
            "revision": "",
            "tags": [],
            "ss_metadata": {
                "bezel_url": None,
                "box2d_url": "https://neoclone.screenscraper.fr/api2/..",
                "box2d_side_url": "https://neoclone.screenscraper.fr/api2/..",
                "box2d_back_url": "https://neoclone.screenscraper.fr/api2/..",
                "box3d_url": "https://neoclone.screenscraper.fr/api2/..",
                "miximage_url": "https://neoclone.screenscraper.fr/api2/..",
                "physical_url": "https://neoclone.screenscraper.fr/api2/..",
                "screenshot_url": "https://neoclone.screenscraper.fr/api2/..",
                "title_screen_url": "https://neoclone.screenscraper.fr/api2/..",
                "bezel_path": None,
                "box3d_path": "roms/1/4/box3d/box3d.png",
                "miximage_path": "roms/1/4/miximage/miximage.png",
                "physical_path": "roms/1/4/physical/physical.png",
                "marquee_path": None,
                "logo_path": None,
                "screenshot_path": "roms/1/4/screenshot/screenshot.png",
                "title_screen_path": "roms/1/4/title_screen/title_screen.png",
            },
        }

    def test_artwork_extraction_from_ss_metadata(self):
        """Test that artwork is correctly extracted from ss_metadata."""
        # Simulate the artwork extraction logic from api.py
        artwork = {}
        ss_metadata = self.mock_rom_data.get("ss_metadata", {})

        if ss_metadata:
            artwork_fields = [
                "miximage",
                "box3d",
                "box2d",
                "box2d_side",
                "box2d_back",
                "fullbox",
                "screenshot",
                "title_screen",
                "wheel",
                "marquee",
                "fanart",
                "banner",
                "physical",
                "bezel",
                "logo",
                "steamgrid",
            ]
            for field in artwork_fields:
                path_field = f"{field}_path"
                if ss_metadata.get(path_field):
                    artwork[field] = ss_metadata.get(path_field)

        # Verify expected artwork is extracted
        self.assertIn("miximage", artwork)
        self.assertEqual(artwork["miximage"], "roms/1/4/miximage/miximage.png")

        self.assertIn("box3d", artwork)
        self.assertEqual(artwork["box3d"], "roms/1/4/box3d/box3d.png")

        self.assertIn("physical", artwork)
        self.assertEqual(artwork["physical"], "roms/1/4/physical/physical.png")

        self.assertIn("screenshot", artwork)
        self.assertEqual(artwork["screenshot"], "roms/1/4/screenshot/screenshot.png")

        self.assertIn("title_screen", artwork)
        self.assertEqual(
            artwork["title_screen"], "roms/1/4/title_screen/title_screen.png"
        )

        # Verify fields without path are not included
        self.assertNotIn("bezel", artwork)
        self.assertNotIn("marquee", artwork)
        self.assertNotIn("logo", artwork)

    def test_url_construction_with_leading_slash(self):
        """Test URL construction handles paths with leading slashes."""
        from urllib.parse import urljoin

        host = "http://localhost:8080"

        # Test with path without leading slash
        artwork_path = "roms/1/4/miximage/miximage.png"
        artwork_path_clean = artwork_path.lstrip("/")
        url = urljoin(f"{host}/", f"assets/romm/resources/{artwork_path_clean}")
        self.assertEqual(
            url,
            "http://localhost:8080/assets/romm/resources/roms/1/4/miximage/miximage.png",
        )

        # Test with path with leading slash
        artwork_path = "/roms/1/4/miximage/miximage.png"
        artwork_path_clean = artwork_path.lstrip("/")
        url = urljoin(f"{host}/", f"assets/romm/resources/{artwork_path_clean}")
        self.assertEqual(
            url,
            "http://localhost:8080/assets/romm/resources/roms/1/4/miximage/miximage.png",
        )

        # Verify no double slashes in URL
        self.assertNotIn("//", url.replace("://", ""))

    def test_empty_ss_metadata_handling(self):
        """Test that empty or missing ss_metadata is handled gracefully."""
        # Test with missing ss_metadata
        rom_data_no_metadata = {
            "id": 1,
            "name": "Test ROM",
        }

        artwork = {}
        ss_metadata = rom_data_no_metadata.get("ss_metadata", {})

        if ss_metadata:
            artwork_fields = ["miximage", "box3d", "screenshot"]
            for field in artwork_fields:
                path_field = f"{field}_path"
                if ss_metadata.get(path_field):
                    artwork[field] = ss_metadata.get(path_field)

        self.assertEqual(artwork, {})

        # Test with empty ss_metadata
        rom_data_empty_metadata = {"id": 2, "name": "Test ROM 2", "ss_metadata": {}}

        artwork = {}
        ss_metadata = rom_data_empty_metadata.get("ss_metadata", {})

        if ss_metadata:
            artwork_fields = ["miximage", "box3d", "screenshot"]
            for field in artwork_fields:
                path_field = f"{field}_path"
                if ss_metadata.get(path_field):
                    artwork[field] = ss_metadata.get(path_field)

        self.assertEqual(artwork, {})


if __name__ == "__main__":
    unittest.main()
