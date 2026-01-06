#!/usr/bin/env python3
"""
Prose composition implementing transition_protocol.

AI-assisted composition of prose from assets.
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


class ProseComposer:
    """Composes prose from assets implementing transition_protocol."""

    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client or LLMClient()

    def compose_from_assets(self,
                          ledger_path: Path,
                          section: Optional[str] = None,
                          style: str = "narrative") -> Dict[str, Any]:
        """
        Compose prose from asset ledger.

        Args:
            ledger_path: Path to asset ledger
            section: Specific section to compose (optional)
            style: Writing style (narrative, technical, explanatory)

        Returns:
            Dict with composition results
        """
        if not ledger_path.exists():
            raise FileNotFoundError(f"Asset ledger not found: {ledger_path}")

        # Read and parse asset ledger
        assets = self._parse_asset_ledger(ledger_path)

        if not assets:
            return {
                "status": "no_assets",
                "message": "No assets found in ledger",
                "prose": "",
                "assets_used": []
            }

        # Use LLM to compose prose
        prose = self._llm_compose_prose(assets, section, style)

        return {
            "status": "composed",
            "ledger": str(ledger_path),
            "section": section,
            "style": style,
            "prose": prose,
            "assets_used": [asset['id'] for asset in assets]
        }

    def _parse_asset_ledger(self, ledger_path: Path) -> List[Dict[str, Any]]:
        """Parse assets from ledger file."""
        assets = []
        content = ledger_path.read_text(encoding="utf-8")
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

    def _llm_compose_prose(self,
                          assets: List[Dict],
                          section: Optional[str],
                          style: str) -> str:
        """Use LLM to compose prose from assets."""
        # Format assets for LLM
        assets_text = "\n".join([
            f"- {asset['id']}: {asset['name']} ({asset['type']}) - {asset.get('notes', '')}"
            for asset in assets
        ])

        style_guidelines = {
            "narrative": "Write in engaging narrative style with smooth transitions",
            "technical": "Write in clear technical documentation style",
            "explanatory": "Write in explanatory style that teaches concepts",
            "concise": "Write in concise, direct style focusing on key facts"
        }

        style_guide = style_guidelines.get(style, style_guidelines["narrative"])

        system_prompt = f"""You are a skilled writer composing content for a CANONIC FSM system.

Your task is to compose PROSE that references ASSETS from the ledger. Key requirements:

1. **Reference Assets**: Use asset names/IDs consistently throughout the prose
2. **Stay Grounded**: Only discuss concepts that exist as assets - no inventing new information
3. **Be Cohesive**: Create flowing, coherent content that connects the assets meaningfully
4. **Style**: {style_guide}

Return only the composed prose content. No meta-commentary, no markdown formatting."""

        section_prompt = f" for the '{section}' section" if section else ""

        user_prompt = f"""Compose prose{section_prompt} using these assets:

{assets_text}

Compose coherent content that references these assets:"""

        messages = [
            LLMMessage(role="system", content=system_prompt),
            LLMMessage(role="user", content=user_prompt)
        ]

        try:
            response = self.llm.chat_completion(messages, temperature=0.7, max_tokens=3000)
            return response.content.strip()

        except Exception as e:
            print(f"LLM composition failed: {e}", file=sys.stderr)
            return ""

    def generate_section_draft(self,
                              ledger_path: Path,
                              section_name: str,
                              context: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a specific section draft with additional context.

        Args:
            ledger_path: Path to asset ledger
            section_name: Name of the section to generate
            context: Additional context about what this section should cover

        Returns:
            Dict with section composition results
        """
        assets = self._parse_asset_ledger(ledger_path)

        if not assets:
            return {
                "status": "no_assets",
                "section": section_name,
                "prose": "",
                "message": "No assets available for composition"
            }

        # Enhanced system prompt for section-specific composition
        system_prompt = f"""You are composing a specific section "{section_name}" for CANONIC documentation.

Requirements:
1. **Asset References**: Use asset names/IDs consistently
2. **Section Focus**: Write specifically for the "{section_name}" section
3. **Grounded Content**: Only reference existing assets
4. **Section Structure**: Include appropriate heading and content flow
5. **CANONIC Compliance**: Follow documentation best practices

Return only the section content with proper markdown formatting."""

        context_text = f"\n\nAdditional context: {context}" if context else ""

        assets_text = "\n".join([
            f"- {asset['id']}: {asset['name']} ({asset['type']}) - {asset.get('notes', '')}"
            for asset in assets
        ])

        user_prompt = f"""Write the "{section_name}" section using these assets:

{assets_text}{context_text}

Compose the section:"""

        messages = [
            LLMMessage(role="system", content=system_prompt),
            LLMMessage(role="user", content=user_prompt)
        ]

        try:
            response = self.llm.chat_completion(messages, temperature=0.6, max_tokens=2500)
            prose = response.content.strip()

            return {
                "status": "section_composed",
                "section": section_name,
                "prose": prose,
                "assets_used": [asset['id'] for asset in assets],
                "context_provided": context is not None
            }

        except Exception as e:
            print(f"Section composition failed: {e}", file=sys.stderr)
            return {
                "status": "error",
                "section": section_name,
                "error": str(e),
                "prose": ""
            }

    def validate_prose_references(self, prose: str, assets: List[Dict]) -> List[str]:
        """Validate that prose only references registered assets."""
        violations = []

        # Create lookup of asset names and IDs
        asset_names = {asset['name'].lower() for asset in assets}
        asset_ids = {asset['id'] for asset in assets}

        # Simple validation - check for unregistered references
        # This is a basic implementation; a full one would use NLP
        prose_lower = prose.lower()

        # Look for potential asset references that aren't registered
        words = set(prose_lower.split())
        potential_assets = []

        for word in words:
            # Skip common words and short words
            if len(word) < 4 or word in self._common_words:
                continue
            # Check if it looks like it should be an asset but isn't
            if word not in asset_names and not any(word in name for name in asset_names):
                potential_assets.append(word)

        if potential_assets:
            violations.append(f"Potential unregistered assets found: {', '.join(potential_assets[:5])}")

        return violations

    @property
    def _common_words(self) -> set:
        """Common English words to exclude from asset detection."""
        return {
            'that', 'with', 'have', 'this', 'will', 'your', 'from', 'they', 'know', 'want',
            'been', 'good', 'much', 'some', 'time', 'very', 'when', 'come', 'here', 'just',
            'like', 'long', 'make', 'many', 'over', 'such', 'take', 'than', 'them', 'well',
            'were', 'what', 'would', 'there', 'their', 'about', 'could', 'other', 'after',
            'first', 'never', 'off', 'being', 'always', 'those', 'under', 'last', 'before',
            'found', 'going', 'still', 'right', 'great', 'small', 'every', 'where', 'these',
            'while', 'three', 'being', 'should', 'really', 'something', 'think', 'around'
        }


def main():
    """CLI interface for prose composition."""
    import argparse

    parser = argparse.ArgumentParser(description="Compose prose from assets")
    parser.add_argument('--assets', '-a', type=Path, default=Path('../assets/LEDGER.md'),
                       help='Path to asset ledger')
    parser.add_argument('--section', '-s', help='Specific section to compose')
    parser.add_argument('--style', default='narrative',
                       choices=['narrative', 'technical', 'explanatory', 'concise'],
                       help='Writing style')
    parser.add_argument('--context', help='Additional context for composition')
    parser.add_argument('--validate', action='store_true',
                       help='Validate references after composition')
    parser.add_argument('--output', '-o', type=Path,
                       help='Save output to file')
    parser.add_argument('--json', action='store_true',
                       help='Output results as JSON')

    args = parser.parse_args()

    try:
        composer = ProseComposer()

        if args.section:
            # Compose specific section
            result = composer.generate_section_draft(
                args.assets, args.section, args.context
            )
        else:
            # Compose general prose
            result = composer.compose_from_assets(
                args.assets, args.section, args.style
            )

        # Validate references if requested
        if args.validate and result.get('prose'):
            assets = composer._parse_asset_ledger(args.assets)
            violations = composer.validate_prose_references(result['prose'], assets)
            if violations:
                result['validation_violations'] = violations
                print("⚠️  Validation warnings:", file=sys.stderr)
                for violation in violations:
                    print(f"   {violation}", file=sys.stderr)

        # Save to file if requested
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(result.get('prose', ''), encoding='utf-8')
            print(f"✅ Saved prose to {args.output}")

        # Output results
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result['status'] == 'composed':
                print("Composed prose:")
                print("=" * 50)
                print(result['prose'])
                print("=" * 50)
                print(f"Used {len(result.get('assets_used', []))} assets")
            elif result['status'] == 'section_composed':
                print(f"Composed section '{result['section']}':")
                print("=" * 50)
                print(result['prose'])
                print("=" * 50)
            else:
                print(f"Composition result: {result}")

    except Exception as e:
        print(f"❌ Prose composition failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
