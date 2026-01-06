#!/usr/bin/env python3
"""Test cases for validation logic."""

import sys
import tempfile
import unittest
from pathlib import Path
from typing import Dict, List, Set

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from validators import FSMValidator


class TestAssetLedgerParsing(unittest.TestCase):
    """Test asset ledger parsing and validation."""

    def test_valid_asset_ledger(self) -> None:
        """Test parsing a valid asset ledger."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("""# Asset Ledger

| ID | Name | Type | Source Episode |
|----|------|------|----------------|
| asset-0001 | First Asset | concept | 01 |
| asset-0002 | Second Asset | person | 02 |
""")
            ledger_path = Path(f.name)

        try:
            root = ledger_path.parent
            validator = FSMValidator(root)
            asset_ids, asset_sources = validator._parse_asset_ledger(ledger_path)

            self.assertEqual(len(asset_ids), 2)
            self.assertIn("asset-0001", asset_ids)
            self.assertIn("asset-0002", asset_ids)
            self.assertEqual(len(validator.violations), 0)
        finally:
            ledger_path.unlink()

    def test_invalid_asset_id_format(self) -> None:
        """Test detection of invalid asset ID format."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("""# Asset Ledger

| ID | Name | Type | Source Episode |
|----|------|------|----------------|
| asset-1 | Invalid | concept | 01 |
| asset-0002 | Valid | person | 02 |
""")
            ledger_path = Path(f.name)

        try:
            root = ledger_path.parent
            validator = FSMValidator(root)
            asset_ids, asset_sources = validator._parse_asset_ledger(ledger_path)

            # Should detect invalid format
            self.assertTrue(any("invalid format" in v["details"].lower() for v in validator.violations))
        finally:
            ledger_path.unlink()

    def test_non_sequential_asset_ids(self) -> None:
        """Test detection of non-sequential asset IDs."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("""# Asset Ledger

| ID | Name | Type | Source Episode |
|----|------|------|----------------|
| asset-0001 | First | concept | 01 |
| asset-0003 | Skipped | person | 02 |
""")
            ledger_path = Path(f.name)

        try:
            root = ledger_path.parent
            validator = FSMValidator(root)
            asset_ids, asset_sources = validator._parse_asset_ledger(ledger_path)

            # Should detect sequential violation
            self.assertTrue(any("sequential" in v["details"].lower() for v in validator.violations))
        finally:
            ledger_path.unlink()


class TestEpisodeValidation(unittest.TestCase):
    """Test episode filename validation."""

    def test_valid_episode_filenames(self) -> None:
        """Test that valid episode filenames pass."""
        with tempfile.TemporaryDirectory() as tmpdir:
            episodes_dir = Path(tmpdir)

            # Create valid episodes
            (episodes_dir / "episode-01.md").write_text("# Episode 1")
            (episodes_dir / "episode-02.md").write_text("# Episode 2")

            validator = FSMValidator(episodes_dir.parent)
            episode_ids = validator._list_episode_ids(episodes_dir)

            self.assertEqual(len(episode_ids), 2)
            self.assertEqual(len(validator.violations), 0)

    def test_invalid_episode_filenames(self) -> None:
        """Test detection of invalid episode filenames."""
        with tempfile.TemporaryDirectory() as tmpdir:
            episodes_dir = Path(tmpdir)

            # Create invalid episodes
            (episodes_dir / "episode-1.md").write_text("# Episode 1")  # Only 1 digit
            (episodes_dir / "episode-001.md").write_text("# Episode 2")  # 3 digits

            validator = FSMValidator(episodes_dir.parent)
            episode_ids = validator._list_episode_ids(episodes_dir)

            # Should detect format violations
            self.assertTrue(len(validator.violations) >= 2)
            self.assertTrue(all("invalid format" in v["details"].lower() for v in validator.violations))


class TestProseValidation(unittest.TestCase):
    """Test prose validation against asset references."""

    def test_valid_prose_references(self) -> None:
        """Test that prose with valid asset references passes."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("""# Prose

This mentions asset-0001 and asset-0002.
""")
            prose_path = Path(f.name)

        try:
            asset_ids = {"asset-0001", "asset-0002"}
            root = prose_path.parent
            validator = FSMValidator(root)

            validator._validate_prose_references(prose_path, asset_ids)

            self.assertEqual(len(validator.violations), 0)
        finally:
            prose_path.unlink()

    def test_unregistered_asset_references(self) -> None:
        """Test detection of unregistered asset references."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("""# Prose

This mentions asset-0001 and asset-9999.
""")
            prose_path = Path(f.name)

        try:
            asset_ids = {"asset-0001"}
            root = prose_path.parent
            validator = FSMValidator(root)

            validator._validate_prose_references(prose_path, asset_ids)

            # Should detect unregistered reference
            self.assertEqual(len(validator.violations), 1)
            self.assertIn("asset-9999", validator.violations[0]["details"])
        finally:
            prose_path.unlink()


class TestStructureValidation(unittest.TestCase):
    """Test structure outline validation."""

    def test_structure_section_parsing(self) -> None:
        """Test parsing structure sections."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("""# Structure

## Section 1: Introduction
## Section 2: Background
## Section 3: Conclusion
""")
            structure_path = Path(f.name)

        try:
            validator = FSMValidator(structure_path.parent)
            sections = validator._parse_structure_sections(structure_path)

            self.assertEqual(len(sections), 3)
            self.assertEqual(sections[0]["name"], "Introduction")
            self.assertEqual(sections[1]["name"], "Background")
            self.assertEqual(sections[2]["name"], "Conclusion")
        finally:
            structure_path.unlink()

    def test_prose_section_order(self) -> None:
        """Test that prose sections match structure order."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, prefix="structure_") as sf:
            sf.write("""# Structure

## Section 1: Introduction
## Section 2: Conclusion
""")
            structure_path = Path(sf.name)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, prefix="prose_") as pf:
            pf.write("""# Prose

## Introduction

Text here.

## Conclusion

More text.
""")
            prose_path = Path(pf.name)

        try:
            root = structure_path.parent
            validator = FSMValidator(root)
            structure_sections = validator._parse_structure_sections(structure_path)
            prose_sections = validator._parse_prose_sections(prose_path)

            validator._validate_structure_order(
                structure_sections, prose_sections, structure_path, prose_path
            )

            # Should pass - sections in correct order
            self.assertEqual(len(validator.violations), 0)
        finally:
            structure_path.unlink()
            prose_path.unlink()


class TestAssetSourceValidation(unittest.TestCase):
    """Test asset source episode validation."""

    def test_valid_asset_sources(self) -> None:
        """Test that assets with valid episode sources pass."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            ledger_path = Path(f.name)

        try:
            asset_sources = {
                "asset-0001": {"line": 5, "sources": ["01", "02"]},
                "asset-0002": {"line": 6, "sources": ["02"]},
            }
            episode_ids = {"01", "02"}
            root = ledger_path.parent
            validator = FSMValidator(root)

            validator._validate_asset_sources(asset_sources, episode_ids, ledger_path)

            self.assertEqual(len(validator.violations), 0)
        finally:
            ledger_path.unlink()

    def test_missing_episode_source(self) -> None:
        """Test detection of assets referencing non-existent episodes."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            ledger_path = Path(f.name)

        try:
            asset_sources = {
                "asset-0001": {"line": 5, "sources": ["01", "99"]},
            }
            episode_ids = {"01"}
            root = ledger_path.parent
            validator = FSMValidator(root)

            validator._validate_asset_sources(asset_sources, episode_ids, ledger_path)

            # Should detect missing episode
            self.assertEqual(len(validator.violations), 1)
            self.assertIn("99", validator.violations[0]["details"])
        finally:
            ledger_path.unlink()


def run_tests() -> int:
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
