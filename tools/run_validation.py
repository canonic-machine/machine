#!/usr/bin/env python3
"""Canonical validator for the writing machine - Modular version."""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from validators import (
    TriadValidator,
    RequiredArtifactsValidator,
    TerminologyValidator,
    FSMValidator,
    FSMSpecNamingValidator,
)


def print_report_text(violations: List[Dict[str, Any]], use_color: bool = False) -> None:
    """Print report in plain text format."""
    status = "compliant" if not violations else "invalid"
    
    # ANSI color codes
    RED = "\033[91m" if use_color else ""
    GREEN = "\033[92m" if use_color else ""
    YELLOW = "\033[93m" if use_color else ""
    RESET = "\033[0m" if use_color else ""
    BOLD = "\033[1m" if use_color else ""
    
    print(f"{BOLD}COMPLIANCE REPORT{RESET}")
    if violations:
        print(f"Status: {RED}{status}{RESET}")
    else:
        print(f"Status: {GREEN}{status}{RESET}")
    print(f"Violations: {len(violations)}")
    
    if violations:
        print()
        for index, violation in enumerate(violations, start=1):
            print(f"{BOLD}{index}. Artifact:{RESET} {YELLOW}{violation['artifact']}{RESET}")
            if violation.get("line"):
                print(f"   Line: {violation['line']}")
            print(f"   Requirement: {violation['requirement']}")
            print(f"   Details: {violation['details']}")
            print()


def print_report_json(violations: List[Dict[str, Any]]) -> None:
    """Print report in JSON format."""
    report = {
        "status": "compliant" if not violations else "invalid",
        "violation_count": len(violations),
        "violations": violations
    }
    print(json.dumps(report, indent=2))


def print_report_summary(violations: List[Dict[str, Any]]) -> None:
    """Print summary statistics."""
    status = "compliant" if not violations else "invalid"
    print(f"Status: {status}")
    print(f"Total violations: {len(violations)}")
    
    if violations:
        # Group by requirement
        by_requirement: Dict[str, int] = {}
        for v in violations:
            req = v["requirement"]
            by_requirement[req] = by_requirement.get(req, 0) + 1
        
        print("\nViolations by requirement:")
        for req, count in sorted(by_requirement.items(), key=lambda x: x[1], reverse=True):
            print(f"  {req}: {count}")


def print_report(violations: List[Dict[str, Any]], format: str = "text", use_color: bool = False) -> None:
    """Print validation report in specified format."""
    if format == "json":
        print_report_json(violations)
    elif format == "summary":
        print_report_summary(violations)
    else:  # text
        print_report_text(violations, use_color)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate CANONIC programming artifacts against governance constraints.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Validate current repository
  %(prog)s --root /path/to/project  # Validate specific directory
  %(prog)s --format json            # Output as JSON
  %(prog)s --format summary         # Show summary statistics
  %(prog)s --color                  # Use colored output
  %(prog)s -v                       # Verbose output
        """
    )
    
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Root directory to validate (default: auto-detect from script location)"
    )
    
    parser.add_argument(
        "--format",
        choices=["text", "json", "summary"],
        default="text",
        help="Output format (default: text)"
    )
    
    parser.add_argument(
        "--color",
        action="store_true",
        help="Use colored output for text format"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output (currently unused, reserved for future)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 2.0.0"
    )
    
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    
    # Determine root directory
    if args.root:
        root = args.root.resolve()
        if not root.exists():
            print(f"Error: Root directory does not exist: {root}", file=sys.stderr)
            sys.exit(1)
        if not root.is_dir():
            print(f"Error: Root path is not a directory: {root}", file=sys.stderr)
            sys.exit(1)
    else:
        root = Path(__file__).resolve().parents[2]
    
    # Run all validators
    all_violations: List[Dict[str, Any]] = []
    
    validators = [
        RequiredArtifactsValidator(root),
        TriadValidator(root),
        TerminologyValidator(root),
        FSMSpecNamingValidator(root),
        FSMValidator(root),
    ]
    
    for validator in validators:
        violations = validator.validate()
        all_violations.extend(violations)
    
    # Print report
    print_report(all_violations, format=args.format, use_color=args.color)
    sys.exit(1 if all_violations else 0)


if __name__ == "__main__":
    main()
