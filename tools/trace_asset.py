#!/usr/bin/env python3
"""
Asset Traceability Tool

Traces assets from source episodes through prose references to output.
Implements traceability requirements from MACHINE.md.

Usage:
  python3 trace_asset.py <asset-id>
  python3 trace_asset.py --all
  python3 trace_asset.py --orphaned
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Optional, Set
import argparse

class AssetTracer:
    """Trace assets through the FSM."""

    def __init__(self, root: Path = Path('.')):
        self.root = root.resolve()
        self.episodes_dir = self.root / 'episodes'
        self.assets_dir = self.root / 'assets'
        self.prose_dir = self.root / 'prose'
        self.output_dir = self.root / 'output'

    def read_ledger(self) -> Dict[str, Dict]:
        """Read asset ledger and parse entries."""
        ledger_file = self.assets_dir / 'LEDGER.md'
        if not ledger_file.exists():
            return {}

        content = ledger_file.read_text()
        assets = {}

        # Parse asset entries (looking for asset-NNNN pattern)
        # Simple parser - assumes format like:
        # **asset-0001**: Name
        # - type: endpoint
        # - source: 001
        # - notes: ...

        current_asset = None
        for line in content.split('\n'):
            # Match asset header (## asset-NNNN)
            header_match = re.match(r'##\s+(asset-\d{4})', line)
            if header_match:
                asset_id = header_match.group(1)
                current_asset = asset_id
                assets[asset_id] = {
                    'id': asset_id,
                    'name': None,
                    'type': None,
                    'source_episode': None,
                    'notes': None
                }
                continue

            if current_asset:
                # Parse fields - **Name:** value format (simple string parsing)
                if line.startswith('- **') and '**:' in line:
                    parts = line.replace('- **', '').split('**:', 1)
                    if len(parts) == 2:
                        field = parts[0].strip().lower()
                        value = parts[1].strip()
                        if field == 'name':
                            assets[current_asset]['name'] = value
                        elif field == 'type':
                            assets[current_asset]['type'] = value
                        elif field == 'source':
                            assets[current_asset]['source_episode'] = value
                        elif field == 'notes':
                            assets[current_asset]['notes'] = value

        return assets

    def find_asset_in_prose(self, asset_id: str) -> List[tuple]:
        """Find references to asset in prose files."""
        references = []

        if not self.prose_dir.exists():
            return references

        for prose_file in self.prose_dir.glob('*.md'):
            # Skip triad files
            if prose_file.name in ['CANON.md', 'VOCABULARY.md', 'README.md']:
                continue

            content = prose_file.read_text()
            for line_num, line in enumerate(content.split('\n'), 1):
                if asset_id in line:
                    references.append((prose_file.name, line_num, line.strip()))

        return references

    def find_asset_in_output(self, asset_id: str) -> List[tuple]:
        """Find references to asset in output files."""
        references = []

        if not self.output_dir.exists():
            return references

        for output_file in self.output_dir.glob('*.md'):
            # Skip triad and metadata files
            if output_file.name in ['CANON.md', 'VOCABULARY.md', 'README.md', 'METADATA.md']:
                continue

            content = output_file.read_text()
            for line_num, line in enumerate(content.split('\n'), 1):
                if asset_id in line:
                    references.append((output_file.name, line_num, line.strip()))

        return references

    def get_episode_path(self, episode_num: str) -> Optional[Path]:
        """Get episode file path from episode number."""
        if not self.episodes_dir.exists():
            return None

        # Look for files matching NNN-*.md pattern
        pattern = f"{episode_num.zfill(3)}-*.md"
        matches = list(self.episodes_dir.glob(pattern))
        return matches[0] if matches else None

    def trace_asset(self, asset_id: str) -> None:
        """Trace a single asset through the FSM."""
        print("=" * 70)
        print(f"ASSET TRACE: {asset_id}")
        print("=" * 70)
        print()

        # Read ledger
        assets = self.read_ledger()

        if asset_id not in assets:
            print(f"❌ Asset not found in ledger: {asset_id}")
            print()
            print("Available assets:")
            for aid in sorted(assets.keys()):
                print(f"  - {aid}: {assets[aid]['name']}")
            return

        asset = assets[asset_id]

        # Display asset info
        print(f"Asset ID:   {asset['id']}")
        print(f"Name:       {asset['name']}")
        print(f"Type:       {asset['type'] or '(not specified)'}")
        print(f"Source:     Episode {asset['source_episode']}")
        if asset['notes']:
            print(f"Notes:      {asset['notes']}")
        print()

        # Trace to source episode
        print("SOURCE EPISODE:")
        print("-" * 70)
        if asset['source_episode']:
            episode_file = self.get_episode_path(asset['source_episode'])
            if episode_file:
                print(f"✓ {episode_file.name}")
                print(f"  Location: {episode_file}")
            else:
                print(f"❌ Episode {asset['source_episode']} not found")
        else:
            print("❌ No source episode specified")
        print()

        # Find in prose
        print("PROSE REFERENCES:")
        print("-" * 70)
        prose_refs = self.find_asset_in_prose(asset_id)
        if prose_refs:
            for filename, line_num, line in prose_refs:
                print(f"✓ {filename}:{line_num}")
                print(f"  {line[:100]}{'...' if len(line) > 100 else ''}")
        else:
            print("○ Not referenced in prose")
        print()

        # Find in output
        print("OUTPUT REFERENCES:")
        print("-" * 70)
        output_refs = self.find_asset_in_output(asset_id)
        if output_refs:
            for filename, line_num, line in output_refs:
                print(f"✓ {filename}:{line_num}")
                print(f"  {line[:100]}{'...' if len(line) > 100 else ''}")
        else:
            print("○ Not in output (output may not exist or asset unused)")
        print()

        # Traceability status
        print("TRACEABILITY STATUS:")
        print("-" * 70)
        has_source = asset['source_episode'] and self.get_episode_path(asset['source_episode'])
        has_prose = len(prose_refs) > 0
        has_output = len(output_refs) > 0

        if has_source:
            print("✓ Traced to source episode")
        else:
            print("❌ Source episode missing or not found")

        if has_prose:
            print(f"✓ Referenced in prose ({len(prose_refs)} reference(s))")
        else:
            print("○ Not yet used in prose")

        if has_output:
            print(f"✓ Appears in output ({len(output_refs)} reference(s))")
        elif self.output_dir.exists() and list(self.output_dir.glob('*.md')):
            print("⚠️  Not in output (possibly unused or filtered)")
        else:
            print("○ Output not yet generated")

        print()

    def trace_all(self) -> None:
        """Trace all assets."""
        assets = self.read_ledger()

        if not assets:
            print("No assets found in ledger.")
            return

        print("=" * 70)
        print(f"ASSET TRACE: ALL ({len(assets)} assets)")
        print("=" * 70)
        print()

        for asset_id in sorted(assets.keys()):
            asset = assets[asset_id]
            prose_refs = self.find_asset_in_prose(asset_id)
            output_refs = self.find_asset_in_output(asset_id)

            status = "✓"
            if not asset['source_episode']:
                status = "❌"
            elif not prose_refs and self.prose_dir.exists():
                status = "○"

            print(f"{status} {asset_id}: {asset['name']}")
            print(f"   Source: Episode {asset['source_episode'] or 'MISSING'}")
            print(f"   Prose: {len(prose_refs)} ref(s) | Output: {len(output_refs)} ref(s)")
            print()

    def find_orphaned(self) -> None:
        """Find assets without valid source episodes."""
        assets = self.read_ledger()

        orphaned = []
        for asset_id, asset in assets.items():
            if not asset['source_episode']:
                orphaned.append((asset_id, "No source episode specified"))
            else:
                episode_file = self.get_episode_path(asset['source_episode'])
                if not episode_file:
                    orphaned.append((asset_id, f"Episode {asset['source_episode']} not found"))

        print("=" * 70)
        print("ORPHANED ASSETS (missing source episodes)")
        print("=" * 70)
        print()

        if not orphaned:
            print("✓ No orphaned assets found")
            print("  All assets have valid source episodes")
        else:
            print(f"❌ Found {len(orphaned)} orphaned asset(s):")
            print()
            for asset_id, reason in orphaned:
                asset = assets[asset_id]
                print(f"  {asset_id}: {asset['name']}")
                print(f"    Issue: {reason}")
                print()

        print()


def main():
    parser = argparse.ArgumentParser(
        description='Trace assets from episodes through prose to output',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Trace specific asset
  python3 trace_asset.py asset-0001

  # Trace all assets
  python3 trace_asset.py --all

  # Find orphaned assets (missing source episodes)
  python3 trace_asset.py --orphaned
        """
    )

    parser.add_argument('asset_id', nargs='?', help='Asset ID to trace (e.g., asset-0001)')
    parser.add_argument('--all', action='store_true', help='Trace all assets')
    parser.add_argument('--orphaned', action='store_true', help='Find orphaned assets')

    args = parser.parse_args()

    if not any([args.asset_id, args.all, args.orphaned]):
        parser.print_help()
        sys.exit(1)

    tracer = AssetTracer()

    try:
        if args.all:
            tracer.trace_all()
        elif args.orphaned:
            tracer.find_orphaned()
        elif args.asset_id:
            tracer.trace_asset(args.asset_id)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
