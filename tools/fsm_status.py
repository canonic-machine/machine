#!/usr/bin/env python3
"""
FSM Status Visualization Tool

Displays current FSM state across the 4-state machine.
Shows: episodes count, assets registered, prose files, output existence, REINDEX status.

Implements visualization requirements from tools/CANON.md.
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional

class FSMStatus:
    """Analyze and display FSM state."""

    def __init__(self, root: Path = Path('.')):
        self.root = root.resolve()
        self.episodes_dir = self.root / 'episodes'
        self.assets_dir = self.root / 'assets'
        self.prose_dir = self.root / 'prose'
        self.output_dir = self.root / 'output'

    def count_episodes(self) -> int:
        """Count episode files."""
        if not self.episodes_dir.exists():
            return 0

        episodes = list(self.episodes_dir.glob('[0-9]*-*.md'))
        return len(episodes)

    def count_assets(self) -> int:
        """Count registered assets in LEDGER."""
        ledger = self.assets_dir / 'LEDGER.md'
        if not ledger.exists():
            return 0

        content = ledger.read_text()
        # Count asset-NNNN patterns
        import re
        assets = re.findall(r'asset-\d{4}', content)
        return len(set(assets))  # Unique assets

    def count_prose_files(self) -> int:
        """Count prose files."""
        if not self.prose_dir.exists():
            return 0

        prose_files = list(self.prose_dir.glob('*.md'))
        # Exclude triad files
        prose_files = [f for f in prose_files if f.name not in ['CANON.md', 'VOCABULARY.md', 'README.md']]
        return len(prose_files)

    def count_output_files(self) -> int:
        """Count output artifacts."""
        if not self.output_dir.exists():
            return 0

        output_files = list(self.output_dir.glob('*.md'))
        # Exclude triad and metadata
        output_files = [f for f in output_files if f.name not in ['CANON.md', 'VOCABULARY.md', 'README.md', 'METADATA.md']]
        return len(output_files)

    def check_reindex(self) -> Optional[str]:
        """Check for active REINDEX protocol."""
        for state_dir in [self.episodes_dir, self.assets_dir, self.prose_dir, self.output_dir]:
            reindex_file = state_dir / 'REINDEX.md'
            if reindex_file.exists():
                return state_dir.name
        return None

    def get_violations(self) -> List[str]:
        """Check for basic FSM violations."""
        violations = []

        # Check prose without assets
        if self.prose_dir.exists() and self.count_prose_files() > 0:
            if not (self.assets_dir / 'LEDGER.md').exists():
                violations.append("Prose exists but assets/LEDGER.md missing")

        # Check output with REINDEX active
        if self.output_dir.exists() and self.count_output_files() > 0:
            reindex_state = self.check_reindex()
            if reindex_state:
                violations.append(f"Output exists despite active REINDEX in {reindex_state}/")

        # Check episodes without assets
        if self.count_episodes() > 0 and self.count_assets() == 0:
            violations.append("Episodes exist but no assets extracted (FSM stalled at Episode state)")

        return violations

    def determine_current_state(self) -> str:
        """Determine primary FSM state."""
        episode_count = self.count_episodes()
        asset_count = self.count_assets()
        prose_count = self.count_prose_files()
        output_count = self.count_output_files()

        if output_count > 0:
            return "Output"
        elif prose_count > 0:
            return "Prose"
        elif asset_count > 0:
            return "Asset"
        elif episode_count > 0:
            return "Episode"
        else:
            return "Empty (no states initialized)"

    def display(self):
        """Display FSM status."""
        print("=" * 60)
        print("FSM STATUS")
        print("=" * 60)
        print()

        # Current state
        current_state = self.determine_current_state()
        print(f"Current State: {current_state}")
        print()

        # State breakdown
        print("State Breakdown:")
        print("-" * 60)

        # Episodes
        episode_count = self.count_episodes()
        episode_status = "✓" if episode_count > 0 else "○"
        episode_immutable = " (immutable)" if self.count_assets() > 0 else ""
        print(f"  {episode_status} Episodes:  {episode_count} files{episode_immutable}")

        # Assets
        asset_count = self.count_assets()
        asset_status = "✓" if asset_count > 0 else "○"
        ledger_exists = (self.assets_dir / 'LEDGER.md').exists()
        ledger_note = " (LEDGER.md exists)" if ledger_exists else " (no LEDGER.md)"
        print(f"  {asset_status} Assets:    {asset_count} registered{ledger_note}")

        # Prose
        prose_count = self.count_prose_files()
        prose_status = "✓" if prose_count > 0 else "○"
        print(f"  {prose_status} Prose:     {prose_count} files")

        # Output
        output_count = self.count_output_files()
        output_status = "✓" if output_count > 0 else "○"
        metadata_exists = (self.output_dir / 'METADATA.md').exists()
        metadata_note = " (with METADATA.md)" if metadata_exists else ""
        print(f"  {output_status} Output:    {output_count} files{metadata_note}")

        print()

        # REINDEX status
        reindex_state = self.check_reindex()
        if reindex_state:
            print(f"⚠️  REINDEX: Active in {reindex_state}/")
            print("   (Output blocked until REINDEX.md removed)")
            print()
        else:
            print("✓  REINDEX: None")
            print()

        # Violations
        violations = self.get_violations()
        if violations:
            print("❌ Violations:")
            for v in violations:
                print(f"   - {v}")
            print()
        else:
            print("✓  No basic violations detected")
            print()

        # Next steps suggestion
        print("Next Steps:")
        print("-" * 60)
        if episode_count == 0:
            print("  1. Create episodes/001-*.md with raw input")
        elif asset_count == 0:
            print("  1. Extract assets from episodes")
            print("  2. Register in assets/LEDGER.md")
        elif prose_count == 0:
            print("  1. Compose prose referencing registered assets")
        elif output_count == 0:
            print("  1. Validate prose")
            print("  2. If valid → output generated")
        else:
            print("  FSM complete! Output exists.")
            if not metadata_exists:
                print("  (Consider adding output/METADATA.md)")

        print()
        print("=" * 60)

    def json_output(self) -> str:
        """Return status as JSON."""
        import json

        status = {
            "current_state": self.determine_current_state(),
            "episodes": {
                "count": self.count_episodes(),
                "immutable": self.count_assets() > 0
            },
            "assets": {
                "count": self.count_assets(),
                "ledger_exists": (self.assets_dir / 'LEDGER.md').exists()
            },
            "prose": {
                "count": self.count_prose_files()
            },
            "output": {
                "count": self.count_output_files(),
                "metadata_exists": (self.output_dir / 'METADATA.md').exists()
            },
            "reindex": {
                "active": self.check_reindex() is not None,
                "state": self.check_reindex()
            },
            "violations": self.get_violations()
        }

        return json.dumps(status, indent=2)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Display FSM state status')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--path', type=str, default='.', help='Path to FSM root directory')

    args = parser.parse_args()

    root = Path(args.path)
    if not root.exists():
        print(f"Error: Path does not exist: {root}", file=sys.stderr)
        sys.exit(1)

    status = FSMStatus(root)

    if args.json:
        print(status.json_output())
    else:
        status.display()

    # Exit code: 0 if no violations, 1 if violations found
    violations = status.get_violations()
    sys.exit(1 if violations else 0)


if __name__ == '__main__':
    main()
