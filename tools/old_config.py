#!/usr/bin/env python3
"""Configuration for canonical validation."""

from typing import Dict

# Requirement reference mappings
REQUIREMENTS: Dict[str, str] = {
    "TRIAD": "CANON.md:134-145 (Triad requirement)",
    "REQUIRED_ARTIFACTS": "CANON.md:248-278 (Required artifacts)",
    "USER_GUIDE_ASSET": "user-guide/CANON.md:60-63 (FSM Validation Details)",
    "USER_GUIDE_STRUCTURE": "user-guide/CANON.md:64-66 (FSM Validation Details)",
}

# File constants
TRIAD_FILES = ("CANON.md", "VOCABULARY.md", "README.md")

# Validation settings
DEFAULT_ENCODING = "utf-8"
