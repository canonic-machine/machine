#!/usr/bin/env python3
"""
Semantic validation implementing validation_protocol.

Comprehensive FSM state validation with protocol enforcement.
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

try:
    # Try relative imports first (when run as module)
    from .config import REQUIREMENTS, TRIAD_FILES
    from .validators import (
        TriadValidator,
        RequiredArtifactsValidator,
        TerminologyValidator,
        FSMValidator,
        FSMSpecNamingValidator
    )
except ImportError:
    # Fall back to absolute imports (when run as script)
    from config import REQUIREMENTS, TRIAD_FILES
    from validators import (
        TriadValidator,
        RequiredArtifactsValidator,
        TerminologyValidator,
        FSMValidator,
        FSMSpecNamingValidator
    )


@dataclass
class ValidationResult:
    """Result of validation operation."""
    valid: bool
    violations: List[Dict[str, Any]]
    summary: Dict[str, int]

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON output."""
        return {
            "valid": self.valid,
            "violations": self.violations,
            "summary": self.summary
        }


class FSMValidatorRunner:
    """Runs comprehensive FSM validation implementing validation_protocol."""

    def __init__(self, root: Path, json_output: bool = False):
        self.root = root.resolve()
        self.json_output = json_output
        self.validators = self._initialize_validators()

    def _initialize_validators(self) -> List:
        """Initialize all FSM validators."""
        return [
            TriadValidator(self.root),
            RequiredArtifactsValidator(self.root),
            TerminologyValidator(self.root),
            FSMValidator(self.root),
            FSMSpecNamingValidator(self.root)
        ]

    def validate_all(self) -> ValidationResult:
        """Run all validators and collect results."""
        all_violations = []

        for validator in self.validators:
            try:
                violations = validator.validate()
                all_violations.extend(violations)
            except Exception as e:
                # Add error as violation
                all_violations.append({
                    "artifact": str(validator.__class__.__name__),
                    "requirement": "validation_protocol",
                    "details": f"Validator failed: {e}",
                    "line": None
                })

        # Create summary
        summary = {
            "total_violations": len(all_violations),
            "validators_run": len(self.validators)
        }

        # Group violations by type
        violation_types = {}
        for violation in all_violations:
            req = violation.get("requirement", "unknown")
            violation_types[req] = violation_types.get(req, 0) + 1

        summary["by_requirement"] = violation_types

        return ValidationResult(
            valid=len(all_violations) == 0,
            violations=all_violations,
            summary=summary
        )

    def validate_state(self, state: str) -> ValidationResult:
        """Validate specific FSM state."""
        state_validators = {
            "episodes": [TriadValidator, TerminologyValidator],
            "assets": [TriadValidator, FSMValidator, FSMSpecNamingValidator],
            "prose": [TriadValidator, TerminologyValidator, FSMValidator],
            "output": [TriadValidator, FSMValidator]
        }

        if state not in state_validators:
            return ValidationResult(
                valid=False,
                violations=[{
                    "artifact": state,
                    "requirement": "fsm_state_pattern",
                    "details": f"Unknown FSM state: {state}",
                    "line": None
                }],
                summary={"total_violations": 1, "validators_run": 0}
            )

        validator_classes = state_validators[state]
        violations = []

        for validator_class in validator_classes:
            try:
                validator = validator_class(self.root)
                state_violations = validator.validate()
                violations.extend(state_violations)
            except Exception as e:
                violations.append({
                    "artifact": f"{state}/{validator_class.__name__}",
                    "requirement": "validation_protocol",
                    "details": f"Validator failed: {e}",
                    "line": None
                })

        return ValidationResult(
            valid=len(violations) == 0,
            violations=violations,
            summary={
                "total_violations": len(violations),
                "validators_run": len(validator_classes),
                "state": state
            }
        )


def print_violations(result: ValidationResult, verbose: bool = True) -> None:
    """Print violations in human-readable format."""
    if result.valid:
        print("✅ All validations passed!")
        return

    print(f"❌ Found {result.summary['total_violations']} violations:")

    if verbose:
        for i, violation in enumerate(result.violations, 1):
            print(f"\n{i}. {violation['artifact']}")
            print(f"   Requirement: {violation['requirement']}")
            print(f"   Issue: {violation['details']}")
            if violation.get('line'):
                print(f"   Line: {violation['line']}")
    else:
        # Group by requirement
        by_req = result.summary.get('by_requirement', {})
        for req, count in by_req.items():
            print(f"  - {req}: {count} violations")

    print(f"\nSummary: {result.summary}")


def main():
    """CLI interface for validation."""
    import argparse

    parser = argparse.ArgumentParser(description="CANONIC FSM Validation")
    parser.add_argument('--state', help='Validate specific FSM state (episodes, assets, prose, output)')
    parser.add_argument('--json', action='store_true', help='Output results as JSON')
    parser.add_argument('--quiet', action='store_true', help='Minimal output')
    parser.add_argument('--root', type=Path, default=Path('../'),
                       help='Root directory of FSM (default: ../)')

    args = parser.parse_args()

    try:
        # Initialize validator
        root_path = args.root.resolve()
        runner = FSMValidatorRunner(root_path, args.json)

        # Run validation
        if args.state:
            result = runner.validate_state(args.state)
        else:
            result = runner.validate_all()

        # Output results
        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print_violations(result, verbose=not args.quiet)

        # Exit with appropriate code
        sys.exit(0 if result.valid else 1)

    except Exception as e:
        if args.json:
            error_result = {
                "valid": False,
                "error": str(e),
                "violations": [],
                "summary": {"total_violations": 1, "error": True}
            }
            print(json.dumps(error_result, indent=2))
        else:
            print(f"❌ Validation failed: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
