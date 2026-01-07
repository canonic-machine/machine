#!/usr/bin/env python3
"""
REINDEX Protocol Tool

Manages coordinated multi-state changes per MACHINE.md REINDEX protocol.
Coordinates changes that invalidate downstream states.

Usage:
  python3 reindex.py start <state> --reason "..." [--changes "..."] [--impacts "..."]
  python3 reindex.py status
  python3 reindex.py complete <state>
  python3 reindex.py abort <state>
"""

import sys
from pathlib import Path
from typing import Optional
import argparse
from datetime import datetime

class REINDEXManager:
    """Manage REINDEX protocol across FSM states."""

    VALID_STATES = {'episodes', 'assets', 'prose', 'output'}

    def __init__(self, root: Path = Path('.')):
        self.root = root.resolve()

    def get_state_dir(self, state: str) -> Path:
        """Get state directory path."""
        if state not in self.VALID_STATES:
            raise ValueError(f"Invalid state: {state}. Must be one of: {', '.join(self.VALID_STATES)}")
        return self.root / state

    def get_reindex_file(self, state: str) -> Path:
        """Get REINDEX.md file path for state."""
        return self.get_state_dir(state) / 'REINDEX.md'

    def is_reindex_active(self, state: str) -> bool:
        """Check if REINDEX is active in state."""
        return self.get_reindex_file(state).exists()

    def get_active_reindexes(self) -> list[str]:
        """Get list of states with active REINDEX."""
        active = []
        for state in self.VALID_STATES:
            if self.is_reindex_active(state):
                active.append(state)
        return active

    def start_reindex(self, state: str, reason: str, changes: str = "", impacts: str = "") -> None:
        """Start REINDEX in a state."""
        state_dir = self.get_state_dir(state)

        if not state_dir.exists():
            raise FileNotFoundError(f"State directory does not exist: {state_dir}")

        reindex_file = self.get_reindex_file(state)

        if reindex_file.exists():
            print(f"⚠️  REINDEX already active in {state}/")
            print(f"Use 'reindex.py complete {state}' or 'reindex.py abort {state}' first")
            sys.exit(1)

        # Create REINDEX.md
        content = self._generate_reindex_content(state, reason, changes, impacts)
        reindex_file.write_text(content)

        print(f"✓ REINDEX started in {state}/")
        print(f"  File: {reindex_file}")
        print()
        print("Next steps:")
        print(f"  1. Make coordinated changes in {state}/")
        print(f"  2. Update downstream states if needed")
        print(f"  3. Run: python3 reindex.py complete {state}")
        print()
        print(f"⚠️  Output blocked while REINDEX active")

    def _generate_reindex_content(self, state: str, reason: str, changes: str, impacts: str) -> str:
        """Generate REINDEX.md content."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        content = f"""# REINDEX: {state}/

**Started:** {timestamp}

## Reason

{reason if reason else "(No reason provided)"}

## Changes

{changes if changes else "(Changes to be documented)"}

## Impacts

{impacts if impacts else "(Downstream impacts to be analyzed)"}

## Status

- [ ] Change completed
- [ ] Downstream adapted
- [ ] Validation passed

## Notes

(Add notes during REINDEX process)

---

**REINDEX Protocol:** This file signals coordinated multi-state changes.
While this file exists, output generation is blocked. Delete this file
to trigger full validation and allow output generation.
"""
        return content

    def complete_reindex(self, state: str) -> None:
        """Complete REINDEX and remove marker file."""
        reindex_file = self.get_reindex_file(state)

        if not reindex_file.exists():
            print(f"❌ No active REINDEX in {state}/")
            sys.exit(1)

        # Read and display final state
        content = reindex_file.read_text()
        print(f"Completing REINDEX in {state}/")
        print()
        print("REINDEX content:")
        print("=" * 60)
        print(content)
        print("=" * 60)
        print()

        # Confirm completion
        response = input("Delete REINDEX.md and trigger validation? [y/N]: ")
        if response.lower() != 'y':
            print("Aborted. REINDEX still active.")
            sys.exit(0)

        # Remove REINDEX.md
        reindex_file.unlink()
        print(f"✓ REINDEX completed in {state}/")
        print(f"✓ {reindex_file} deleted")
        print()
        print("Next steps:")
        print("  1. Run full validation")
        print("  2. If valid → output can be generated")
        print("  3. If invalid → fix violations and retry")

    def abort_reindex(self, state: str) -> None:
        """Abort REINDEX without completing."""
        reindex_file = self.get_reindex_file(state)

        if not reindex_file.exists():
            print(f"❌ No active REINDEX in {state}/")
            sys.exit(1)

        print(f"⚠️  Aborting REINDEX in {state}/")
        print("This will remove the REINDEX marker without validation.")
        print()

        response = input("Confirm abort? [y/N]: ")
        if response.lower() != 'y':
            print("Cancelled.")
            sys.exit(0)

        reindex_file.unlink()
        print(f"✓ REINDEX aborted in {state}/")
        print(f"✓ {reindex_file} deleted")

    def show_status(self) -> None:
        """Show REINDEX status across all states."""
        print("=" * 60)
        print("REINDEX STATUS")
        print("=" * 60)
        print()

        active = self.get_active_reindexes()

        if not active:
            print("✓ No active REINDEX protocols")
            print()
            print("All states are stable. Output generation allowed.")
        else:
            print(f"⚠️  Active REINDEX: {len(active)} state(s)")
            print()

            for state in active:
                reindex_file = self.get_reindex_file(state)
                content = reindex_file.read_text()

                print(f"State: {state}/")
                print("-" * 60)
                print(content)
                print()

            print("=" * 60)
            print("⚠️  Output blocked while REINDEX active")
            print()
            print("To complete:")
            for state in active:
                print(f"  python3 reindex.py complete {state}")


def main():
    parser = argparse.ArgumentParser(
        description='Manage REINDEX protocol for coordinated FSM changes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start REINDEX in assets state
  python3 reindex.py start assets --reason "Changing asset ID format"

  # Check status
  python3 reindex.py status

  # Complete REINDEX
  python3 reindex.py complete assets

  # Abort REINDEX
  python3 reindex.py abort assets
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Start command
    start_parser = subparsers.add_parser('start', help='Start REINDEX in a state')
    start_parser.add_argument('state', choices=['episodes', 'assets', 'prose', 'output'],
                             help='FSM state to REINDEX')
    start_parser.add_argument('--reason', required=True,
                             help='Reason for REINDEX (required)')
    start_parser.add_argument('--changes',
                             help='Description of changes being made')
    start_parser.add_argument('--impacts',
                             help='Description of downstream impacts')

    # Status command
    subparsers.add_parser('status', help='Show REINDEX status')

    # Complete command
    complete_parser = subparsers.add_parser('complete', help='Complete REINDEX')
    complete_parser.add_argument('state', choices=['episodes', 'assets', 'prose', 'output'],
                                help='FSM state to complete')

    # Abort command
    abort_parser = subparsers.add_parser('abort', help='Abort REINDEX')
    abort_parser.add_argument('state', choices=['episodes', 'assets', 'prose', 'output'],
                             help='FSM state to abort')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    manager = REINDEXManager()

    try:
        if args.command == 'start':
            manager.start_reindex(args.state, args.reason,
                                args.changes or "", args.impacts or "")
        elif args.command == 'status':
            manager.show_status()
        elif args.command == 'complete':
            manager.complete_reindex(args.state)
        elif args.command == 'abort':
            manager.abort_reindex(args.state)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
