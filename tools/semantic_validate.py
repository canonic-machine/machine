#!/usr/bin/env python3
"""
Semantic validation tool for CANONIC programming artifacts.
Uses LLM integration to validate constraint compliance beyond syntactic checks.
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from llm import LLMClient  # type: ignore
except ImportError:
    from .llm import LLMClient  # type: ignore

class SemanticValidator:
    """Uses LLM to validate semantic compliance with CANON constraints."""

    def __init__(self, root: Path):
        self.root: Path = root
        self.llm: LLMClient | None = None
        self.llm_available: bool = False

        try:
            self.llm = LLMClient()
            self.llm_available = True
        except Exception:
            # LLM not available - semantic validation limited
            self.llm_available = False

        self.violations: List[Dict[str, Any]] = []

    def read_file_content(self, file_path: Path) -> str:
        """Read file content safely."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"

    def validate_spec_naming(self) -> None:
        """Validate specification file naming against CANON invariant."""
        spec_files = list(self.root.glob("*CANONIC*.md"))

        for spec_file in spec_files:
            content = self.read_file_content(spec_file)

            # Basic validation: check if file follows CANONIC naming
            if self.llm_available:
                prompt = f"""
                Analyze this CANONIC specification file for naming compliance.

                File: {spec_file.name}
                Repository name: "canonic"
                CANON invariant: "Repository specification files must be named <REPO>.md."

                Question: Does "{spec_file.name}" violate the specification naming invariant?

                Return ONLY valid JSON:
                {{
                    "violates_invariant": true,
                    "correct_name": "CANONIC.md",
                    "reasoning": "brief explanation of why it violates or doesn't"
                }}
                """

                try:
                    if self.llm is None:
                        raise Exception("LLM client not available")

                    response = self.llm.chat_completion([{"role": "user", "content": prompt}])  # type: ignore
                    # Handle LLMResponse object
                    if hasattr(response, 'content') and response.content:  # type: ignore
                        response_text = response.content  # type: ignore
                    else:
                        response_text = str(response)

                    result = json.loads(response_text.strip())

                    if result.get("violates_invariant"):
                        self.violations.append({
                            "artifact": str(spec_file.relative_to(self.root)),
                            "requirement": "Specification file naming",
                            "details": f"File should be named {result['correct_name']}. {result['reasoning']}",
                            "severity": "high"
                        })
                except Exception as e:
                    self.violations.append({
                        "artifact": str(spec_file.relative_to(self.root)),
                        "requirement": "Specification file naming",
                        "details": f"LLM validation failed: {e}",
                        "severity": "medium"
                    })
            else:
                # Fallback validation without LLM
                if spec_file.name != "CANONIC.md":
                    self.violations.append({
                        "artifact": str(spec_file.relative_to(self.root)),
                        "requirement": "Specification file naming",
                        "details": f"Specification file should be named CANONIC.md (LLM validation unavailable)",
                        "severity": "medium"
                    })

    def validate_governance_purity(self) -> None:
        """Validate governance purity - no extra files."""
        allowed_files = {
            "CANON.md", "VOCABULARY.md", "README.md", "CANONIC.md",  # Repository specification file
            ".gitignore", ".git"  # Git files are acceptable
        }
        allowed_dirs = {"examples"}

        for item in self.root.iterdir():
            if item.is_file():
                if item.name not in allowed_files:
                    self.violations.append({
                        "artifact": item.name,
                        "requirement": "Governance purity",
                        "details": f"File '{item.name}' violates governance purity - only repository specification file, CANON.md, VOCABULARY.md, README.md, and examples allowed",
                        "severity": "high"
                    })
            elif item.is_dir() and item.name not in allowed_dirs:
                # Check if it's a hidden/system directory
                if not item.name.startswith('.'):
                    self.violations.append({
                        "artifact": item.name + "/",
                        "requirement": "Governance purity",
                        "details": f"Directory '{item.name}' violates governance purity",
                        "severity": "high"
                    })

    def validate_documentation_purity(self) -> None:
        """Validate documentation doesn't reference non-existent tools."""
        readme_path = self.root / "README.md"
        if readme_path.exists():
            content = self.read_file_content(readme_path)

            # Check for tool references
            if "tools/validation/" in content:
                self.violations.append({
                    "artifact": "README.md",
                    "requirement": "Documentation purity",
                    "details": "README.md references 'tools/validation/' which doesn't exist in governance-pure repository",
                    "severity": "medium"
                })

    def validate(self) -> List[Dict[str, Any]]:
        """Run all semantic validations."""
        self.validate_spec_naming()
        self.validate_governance_purity()
        self.validate_documentation_purity()
        return self.violations

def main():
    parser = argparse.ArgumentParser(description="Semantic validation for CANONIC artifacts")
    parser.add_argument("--root", type=str, default=".", help="Root directory to validate")
    parser.add_argument("--provider", type=str, default="deepseek", choices=["openai", "deepseek", "anthropic"])
    parser.add_argument("--format", type=str, default="text", choices=["text", "json"])
    parser.add_argument("--color", action="store_true", help="Use colored output")

    args = parser.parse_args()

    root_path = Path(args.root).resolve()

    if not root_path.exists():
        print(f"Error: Root directory does not exist: {root_path}")
        return 1

    validator = SemanticValidator(root_path)
    violations = validator.validate()

    if args.format == "json":
        result = {
            "valid": len(violations) == 0,
            "violations": violations,
            "summary": {
                "total_violations": len(violations),
                "by_severity": {}
            }
        }

        # Count by severity
        for v in violations:
            severity = v.get("severity", "unknown")
            result["summary"]["by_severity"][severity] = result["summary"]["by_severity"].get(severity, 0) + 1

        print(json.dumps(result, indent=2))

    else:
        # Text format
        if violations:
            print("SEMANTIC VALIDATION FAILED")
            print(f"Found {len(violations)} violations:")
            print()

            for i, violation in enumerate(violations, 1):
                severity = violation.get("severity", "unknown")
                severity_marker = "🔴" if severity == "high" else "🟡" if severity == "medium" else "⚪"
                print(f"{i}. {severity_marker} {violation['artifact']}")
                print(f"   Requirement: {violation['requirement']}")
                print(f"   Issue: {violation['details']}")
                print()
        else:
            print("✅ SEMANTIC VALIDATION PASSED")
            print("No semantic violations found.")

    return 0 if len(violations) == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
