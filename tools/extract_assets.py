#!/usr/bin/env python3
"""
Asset extraction implementing transition_protocol.

AI-assisted extraction of assets from episodes.
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

try:
    # Try relative imports first (when run as module)
    from .llm import LLMClient, LLMMessage
    from .config import REQUIREMENTS, TRIAD_FILES
except ImportError:
    # Fall back to absolute imports (when run as script)
    from llm import LLMClient, LLMMessage
    from config import REQUIREMENTS, TRIAD_FILES


class AssetExtractor:
    """Extracts assets from episodes implementing transition_protocol."""

    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client or LLMClient()
        self.episode_dir = None
        self.assets_dir = None

    def extract_from_episode(self, episode_path: Path, interactive: bool = False) -> Dict[str, Any]:
        """
        Extract assets from a single episode.

        Args:
            episode_path: Path to episode file
            interactive: Whether to require human approval

        Returns:
            Dict with extraction results
        """
        if not episode_path.exists():
            raise FileNotFoundError(f"Episode not found: {episode_path}")

        # Read episode content
        episode_content = episode_path.read_text(encoding="utf-8")

        # Extract episode number for asset ID generation
        episode_name = episode_path.name
        episode_num = self._extract_episode_number(episode_name)

        # Use LLM to extract assets
        assets = self._llm_extract_assets(episode_content, episode_num)

        if interactive:
            assets = self._interactive_review(assets, episode_content)

        return {
            "episode": str(episode_path),
            "episode_number": episode_num,
            "assets": assets,
            "status": "extracted"
        }

    def _extract_episode_number(self, filename: str) -> int:
        """Extract episode number from filename (e.g., '001-topic.md' -> 1)."""
        import re
        match = re.match(r'^(\d+)', filename)
        if match:
            return int(match.group(1))
        raise ValueError(f"Cannot extract episode number from filename: {filename}")

    def _llm_extract_assets(self, episode_content: str, episode_num: int) -> List[Dict[str, Any]]:
        """Use LLM to extract assets from episode content."""
        system_prompt = """You are an expert at extracting structured information from raw content for a CANONIC FSM system.

Your task is to identify and extract ASSETS from EPISODE content. Assets are:
- Entities (people, places, objects, concepts)
- Structured information that will be referenced in prose
- Stable identifiers that won't change

For each asset, provide:
- name: Human-readable name
- type: One of [person, place, object, concept, event, data]
- description: Brief explanation of what this asset represents
- context: Why this matters in the episode

Return ONLY a JSON array of asset objects. No markdown, no explanations."""

        user_prompt = f"""Extract assets from this episode content:

{episode_content}

Return as JSON array:"""

        messages = [
            LLMMessage(role="system", content=system_prompt),
            LLMMessage(role="user", content=user_prompt)
        ]

        try:
            response = self.llm.chat_completion(messages, temperature=0.3, max_tokens=2000)

            # Parse JSON response
            assets_data = json.loads(response.content.strip())

            # Validate and format assets
            formatted_assets = []
            for i, asset_data in enumerate(assets_data):
                if isinstance(asset_data, dict) and 'name' in asset_data:
                    # Generate asset ID
                    asset_id = "02d"

                    formatted_asset = {
                        "id": asset_id,
                        "name": asset_data["name"],
                        "type": asset_data.get("type", "concept"),
                        "source_episode": episode_num,
                        "description": asset_data.get("description", ""),
                        "context": asset_data.get("context", ""),
                        "notes": f"Extracted from episode {episode_num}"
                    }
                    formatted_assets.append(formatted_asset)

            return formatted_assets

        except Exception as e:
            print(f"LLM extraction failed: {e}", file=sys.stderr)
            return []

    def _interactive_review(self, assets: List[Dict], episode_content: str) -> List[Dict]:
        """Allow human review and editing of extracted assets."""
        print("Episode content preview:")
        print("=" * 50)
        print(episode_content[:500] + "..." if len(episode_content) > 500 else episode_content)
        print("=" * 50)
        print()

        approved_assets = []

        for i, asset in enumerate(assets):
            print(f"Asset {i+1}:")
            print(f"  ID: {asset['id']}")
            print(f"  Name: {asset['name']}")
            print(f"  Type: {asset['type']}")
            print(f"  Description: {asset['description']}")
            print()

            while True:
                response = input("Approve this asset? (y/n/e=edit/s=skip): ").lower().strip()
                if response == 'y':
                    approved_assets.append(asset)
                    break
                elif response == 'n':
                    break  # Skip this asset
                elif response == 'e':
                    asset = self._edit_asset(asset)
                    approved_assets.append(asset)
                    break
                elif response == 's':
                    break
                else:
                    print("Please enter y, n, e, or s")

        return approved_assets

    def _edit_asset(self, asset: Dict) -> Dict:
        """Allow editing of asset fields."""
        print("Current asset:")
        print(json.dumps(asset, indent=2))

        # Simple field editing
        for field in ['name', 'type', 'description', 'context']:
            current = asset.get(field, '')
            new_value = input(f"{field.capitalize()} [{current}]: ").strip()
            if new_value:
                asset[field] = new_value

        return asset

    def register_assets(self, assets: List[Dict], ledger_path: Path) -> None:
        """Register extracted assets in the ledger."""
        # Read existing ledger
        existing_assets = []
        if ledger_path.exists():
            content = ledger_path.read_text(encoding="utf-8")
            # Parse simple markdown table format
            existing_assets = self._parse_ledger(content)

        # Check for duplicates and merge
        for new_asset in assets:
            # Check if asset already exists
            existing = next((a for a in existing_assets if a['name'] == new_asset['name']), None)
            if existing:
                # Merge notes
                if new_asset['notes'] not in existing.get('notes', ''):
                    existing['notes'] = f"{existing.get('notes', '')}; {new_asset['notes']}"
            else:
                existing_assets.append(new_asset)

        # Write updated ledger
        ledger_content = self._format_ledger(existing_assets)
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        ledger_path.write_text(ledger_content, encoding="utf-8")

    def _parse_ledger(self, content: str) -> List[Dict]:
        """Parse assets from ledger markdown table."""
        assets = []
        lines = content.split('\n')

        # Find table start
        table_start = -1
        for i, line in enumerate(lines):
            if line.startswith('| ID |'):
                table_start = i + 2  # Skip header and separator
                break

        if table_start == -1:
            return assets

        # Parse table rows
        for line in lines[table_start:]:
            if not line.strip() or not line.startswith('|'):
                continue

            columns = [col.strip() for col in line.strip('|').split('|')]
            if len(columns) >= 4:
                asset = {
                    'id': columns[0],
                    'name': columns[1],
                    'type': columns[2],
                    'source_episode': columns[3],
                    'notes': columns[4] if len(columns) > 4 else ''
                }
                assets.append(asset)

        return assets

    def _format_ledger(self, assets: List[Dict]) -> str:
        """Format assets as markdown table."""
        lines = [
            "# Asset Ledger",
            "",
            "| ID | Name | Type | Source Episode | Notes |",
            "|----|------|------|----------------|-------|"
        ]

        for asset in sorted(assets, key=lambda x: x['id']):
            notes = asset.get('notes', '')
            line = f"| {asset['id']} | {asset['name']} | {asset['type']} | {asset['source_episode']} | {notes} |"
            lines.append(line)

        return '\n'.join(lines) + '\n'


def main():
    """CLI interface for asset extraction."""
    import argparse

    parser = argparse.ArgumentParser(description="Extract assets from episodes")
    parser.add_argument('episode', help='Path to episode file')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Interactive review mode')
    parser.add_argument('--register', action='store_true',
                       help='Register assets in ledger')
    parser.add_argument('--ledger', type=Path, default=Path('../assets/LEDGER.md'),
                       help='Path to asset ledger')
    parser.add_argument('--json', action='store_true',
                       help='Output results as JSON')

    args = parser.parse_args()

    try:
        extractor = AssetExtractor()
        episode_path = Path(args.episode)

        # Extract assets
        result = extractor.extract_from_episode(episode_path, args.interactive)

        if args.register:
            extractor.register_assets(result['assets'], args.ledger)
            print(f"✅ Registered {len(result['assets'])} assets in {args.ledger}")

        # Output results
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Extracted {len(result['assets'])} assets from {episode_path.name}")
            for asset in result['assets']:
                print(f"  - {asset['id']}: {asset['name']} ({asset['type']})")

    except Exception as e:
        print(f"❌ Asset extraction failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
