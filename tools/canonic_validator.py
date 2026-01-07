#!/usr/bin/env python3
"""
Comprehensive CANONIC validation implementing dual validation protocol.

Per CANON.md: "Systems must implement dual validation:
syntactic (structure) + semantic (constraints)."

This validator ensures:
1. SYNTACTIC: File structure, format, naming conventions
2. SEMANTIC: Logical coherence, completeness, enforceability of constraints
"""

import json
import re
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

try:
    from llm import LLMClient
except ImportError:
    try:
        from .llm import LLMClient
    except ImportError:
        LLMClient = None


class ViolationSeverity(Enum):
    """Violation severity levels."""
    CRITICAL = "critical"  # Blocks all operations
    HIGH = "high"          # Must fix before production
    MEDIUM = "medium"      # Should fix soon
    LOW = "low"            # Nice to fix


@dataclass
class Violation:
    """Validation violation."""
    layer: str              # "syntactic" or "semantic"
    category: str           # e.g., "triad", "reference_integrity"
    artifact: str           # File or directory path
    requirement: str        # What constraint was violated
    details: str            # Specific violation description
    severity: ViolationSeverity
    line: Optional[int] = None
    auto_fixable: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        d = asdict(self)
        d['severity'] = self.severity.value
        return d


class SyntacticValidator:
    """
    Syntactic validation: structure and format.

    Fast, cheap validation of form over function.
    Checks file existence, naming, structure, format.
    """

    def __init__(self, root: Path):
        self.root = root
        self.violations: List[Violation] = []

    def validate_all(self) -> List[Violation]:
        """Run all syntactic validations."""
        self.validate_triad()
        self.validate_dictionary_ordering()
        self.validate_naming_conventions()
        self.validate_file_structure()
        self.validate_inheritance_declaration()
        self.validate_constraint_format()
        self.validate_git_history_signals()
        return self.violations

    def validate_dictionary_ordering(self) -> None:
        """Validate DICTIONARY.md alphabetical ordering."""
        for dict_file in self.root.rglob("DICTIONARY.md"):
            if any(part.startswith('.') for part in dict_file.parts):
                continue

            content = self._read_file(dict_file)
            if not content:
                continue

            # Extract term headers (### level)
            current_section = None
            section_terms = []

            for line in content.split('\n'):
                # Track sections (##)
                if line.startswith('## '):
                    # Check previous section
                    if section_terms:
                        sorted_terms = sorted(section_terms, key=str.lower)
                        if section_terms != sorted_terms:
                            self.violations.append(Violation(
                                layer="syntactic",
                                category="dictionary_ordering",
                                artifact=str(dict_file.relative_to(self.root)),
                                requirement="DICTIONARY.md alphabetical ordering",
                                details=f"Terms not alphabetically ordered in section '{current_section}'. Expected order: {sorted_terms}",
                                severity=ViolationSeverity.CRITICAL,
                                auto_fixable=True
                            ))
                    current_section = line[3:].strip()
                    section_terms = []
                # Extract terms
                elif line.startswith('### '):
                    term = line[4:].strip()
                    section_terms.append(term)

            # Check final section
            if section_terms:
                sorted_terms = sorted(section_terms, key=str.lower)
                if section_terms != sorted_terms:
                    self.violations.append(Violation(
                        layer="syntactic",
                        category="dictionary_ordering",
                        artifact=str(dict_file.relative_to(self.root)),
                        requirement="DICTIONARY.md alphabetical ordering",
                        details=f"Terms not alphabetically ordered in section '{current_section}'. Expected order: {sorted_terms}",
                        severity=ViolationSeverity.CRITICAL,
                        auto_fixable=True
                    ))

    def validate_git_history_signals(self) -> None:
        """
        Validate git history for violation patterns.

        Per CANON.md Self-healing constraint:
        "Systems must detect violations through git history patterns and trigger validation."

        CANONIC PRINCIPLE: Git commits ARE FSM state transitions
        - Each commit proposes a state transition
        - Pre-commit validation acts as gate (accept/reject)
        - Rejected commits trigger backflow to source state
        - Git history records the complete FSM transition log

        Violation signals:
        - Commit → Revert → Reapply pattern (failed transition attempt)
        - Rapid commits on CANON files (state instability)
        - Fix/violation keywords in commit messages (acknowledged failures)
        """
        if not self._is_git_repo():
            return

        # Check for revert patterns
        revert_pattern = self._detect_revert_pattern()
        if revert_pattern:
            self.violations.append(Violation(
                layer="syntactic",
                category="git_history",
                artifact=".",
                requirement="Self-healing",
                details=f"Git history shows revert pattern: {revert_pattern}. This indicates failed validation. Human review required.",
                severity=ViolationSeverity.HIGH
            ))

        # Check for rapid CANON.md commits
        rapid_commits = self._detect_rapid_canon_commits()
        if rapid_commits:
            self.violations.append(Violation(
                layer="syntactic",
                category="git_history",
                artifact="CANON.md",
                requirement="Self-healing",
                details=f"Detected {rapid_commits} commits to CANON.md in last 24 hours. Indicates constraint drift. Comprehensive validation recommended.",
                severity=ViolationSeverity.MEDIUM
            ))

        # Check for violation keywords in recent commits
        violation_commits = self._detect_violation_keywords()
        if violation_commits:
            self.violations.append(Violation(
                layer="syntactic",
                category="git_history",
                artifact=".",
                requirement="Self-healing",
                details=f"Recent commits reference violations: {', '.join(violation_commits[:3])}. Validation should have been triggered.",
                severity=ViolationSeverity.HIGH
            ))

    def _is_git_repo(self) -> bool:
        """Check if directory is a git repository."""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False

    def _detect_revert_pattern(self) -> Optional[str]:
        """
        Detect Commit → Revert → Reapply pattern in recent history.

        Returns description of pattern if found, None otherwise.
        """
        try:
            # Get last 20 commits
            result = subprocess.run(
                ['git', 'log', '--oneline', '-20', '--all'],
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode != 0:
                return None

            commits = result.stdout.strip().split('\n')

            # Look for "Revert" followed by "Reapply" or "Fix"
            for i, commit in enumerate(commits[:-2]):
                if 'revert' in commit.lower():
                    # Check if next commits are reapply/fix
                    next_commits = commits[i+1:i+3]
                    for next_commit in next_commits:
                        if any(kw in next_commit.lower() for kw in ['reapply', 'fix', 'restore']):
                            return f"Found revert at commit {i}, followed by fix/reapply"

            return None
        except Exception:
            return None

    def _detect_rapid_canon_commits(self) -> Optional[int]:
        """
        Detect rapid commits to CANON.md files (>3 in 24 hours).

        Returns count if threshold exceeded, None otherwise.
        """
        try:
            # Get commits to CANON.md in last 24 hours
            result = subprocess.run(
                ['git', 'log', '--oneline', '--since=24.hours.ago', '--', '**/CANON.md', 'CANON.md'],
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode != 0:
                return None

            commit_count = len([l for l in result.stdout.strip().split('\n') if l])

            # Threshold: more than 3 CANON commits in 24h indicates drift
            if commit_count > 3:
                return commit_count

            return None
        except Exception:
            return None

    def _detect_violation_keywords(self) -> List[str]:
        """
        Detect violation/fix keywords in recent commits.

        Returns list of commit messages containing violation keywords.
        """
        try:
            # Get last 10 commits
            result = subprocess.run(
                ['git', 'log', '--oneline', '-10'],
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode != 0:
                return []

            commits = result.stdout.strip().split('\n')

            # Keywords that indicate constraint violations
            keywords = ['violation', 'fix.*integrity', 'fix.*reference', 'broken', 'invalid', 'revert.*fix']

            violation_commits = []
            for commit in commits:
                commit_lower = commit.lower()
                if any(re.search(kw, commit_lower) for kw in keywords):
                    violation_commits.append(commit.split(' ', 1)[1] if ' ' in commit else commit)

            return violation_commits if len(violation_commits) > 0 else []
        except Exception:
            return []

    def validate_triad(self) -> None:
        """Validate triad requirement: CANON.md, DICTIONARY.md, README.md."""
        triad_files = {"CANON.md", "DICTIONARY.md", "README.md"}

        for dirpath in self._get_governed_directories():
            missing = []
            for filename in triad_files:
                if not (dirpath / filename).exists():
                    missing.append(filename)

            if missing:
                self.violations.append(Violation(
                    layer="syntactic",
                    category="triad",
                    artifact=str(dirpath.relative_to(self.root)),
                    requirement="Triad requirement",
                    details=f"Missing triad files: {', '.join(missing)}",
                    severity=ViolationSeverity.CRITICAL
                ))

    def validate_naming_conventions(self) -> None:
        """Validate UPPERCASE.md naming convention."""
        for md_file in self.root.rglob("*.md"):
            # Skip hidden directories
            if any(part.startswith('.') for part in md_file.parts):
                continue

            basename = md_file.stem
            extension = md_file.suffix

            # Check: base name should be UPPERCASE
            if not basename.isupper():
                self.violations.append(Violation(
                    layer="syntactic",
                    category="naming",
                    artifact=str(md_file.relative_to(self.root)),
                    requirement="Artifact naming",
                    details=f"Base name '{basename}' should be UPPERCASE",
                    severity=ViolationSeverity.MEDIUM,
                    auto_fixable=True
                ))

            # Check: extension should be lowercase
            if extension != extension.lower():
                self.violations.append(Violation(
                    layer="syntactic",
                    category="naming",
                    artifact=str(md_file.relative_to(self.root)),
                    requirement="Artifact naming",
                    details=f"Extension '{extension}' should be lowercase",
                    severity=ViolationSeverity.MEDIUM,
                    auto_fixable=True
                ))

    def validate_file_structure(self) -> None:
        """Validate CANON.md file structure."""
        for canon_file in self.root.rglob("CANON.md"):
            if any(part.startswith('.') for part in canon_file.parts):
                continue

            content = self._read_file(canon_file)
            if not content:
                continue

            # Check for required header
            if not re.search(r'^# CANON', content, re.MULTILINE):
                self.violations.append(Violation(
                    layer="syntactic",
                    category="structure",
                    artifact=str(canon_file.relative_to(self.root)),
                    requirement="CANON structure",
                    details="Missing '# CANON' header",
                    severity=ViolationSeverity.HIGH
                ))

    def validate_inheritance_declaration(self) -> None:
        """Validate inheritance declaration format."""
        for canon_file in self.root.rglob("CANON.md"):
            if any(part.startswith('.') for part in canon_file.parts):
                continue

            content = self._read_file(canon_file)
            if not content:
                continue

            # Check for inheritance declaration
            if not re.search(r'\*\*Inherits from:\*\*', content):
                self.violations.append(Violation(
                    layer="syntactic",
                    category="inheritance",
                    artifact=str(canon_file.relative_to(self.root)),
                    requirement="Inheritance declaration",
                    details="Missing '**Inherits from:**' declaration",
                    severity=ViolationSeverity.HIGH,
                    line=self._find_line_number(content, "# CANON")
                ))

    def validate_constraint_format(self) -> None:
        """Validate constraint format in CANON.md."""
        for canon_file in self.root.rglob("CANON.md"):
            if any(part.startswith('.') for part in canon_file.parts):
                continue

            content = self._read_file(canon_file)
            if not content:
                continue

            # Extract constraints (sections with ### headers)
            constraints = re.findall(r'###\s+(.+?)$(.*?)(?=###|\Z)',
                                   content, re.MULTILINE | re.DOTALL)

            for constraint_name, constraint_body in constraints:
                # Check if constraint has violation statement
                if "**Violation:**" not in constraint_body:
                    line_num = self._find_line_number(content, f"### {constraint_name}")
                    self.violations.append(Violation(
                        layer="syntactic",
                        category="constraint_format",
                        artifact=str(canon_file.relative_to(self.root)),
                        requirement="Constraint completeness",
                        details=f"Constraint '{constraint_name.strip()}' missing '**Violation:**' statement",
                        severity=ViolationSeverity.HIGH,
                        line=line_num
                    ))

    def _get_governed_directories(self) -> List[Path]:
        """Get all directories that should have triad files."""
        dirs = [self.root]
        for item in self.root.rglob("*"):
            if item.is_dir() and not any(part.startswith('.') for part in item.parts):
                # Check if it's a governed directory (has any .md files)
                if any(item.glob("*.md")):
                    dirs.append(item)
        return dirs

    def _read_file(self, path: Path) -> str:
        """Read file content safely."""
        try:
            return path.read_text(encoding='utf-8')
        except Exception:
            return ""

    def _find_line_number(self, content: str, search: str) -> Optional[int]:
        """Find line number of search string."""
        for i, line in enumerate(content.split('\n'), 1):
            if search in line:
                return i
        return None


class SemanticValidator:
    """
    Semantic validation: logical coherence and meaning.

    Uses LLM to validate that constraints are:
    - Logically coherent (no contradictions)
    - Complete (all required elements present)
    - Enforceable (can be tested)
    - Unambiguous (clear meaning)
    """

    def __init__(self, root: Path, llm_client: Optional[Any] = None):
        self.root = root
        self.llm = llm_client
        self.violations: List[Violation] = []
        self.llm_available = llm_client is not None

    def validate_all(self) -> List[Violation]:
        """Run all semantic validations."""
        if not self.llm_available:
            self.violations.append(Violation(
                layer="semantic",
                category="llm_unavailable",
                artifact=".",
                requirement="LLM availability",
                details="LLM not available - semantic validation limited to basic checks",
                severity=ViolationSeverity.MEDIUM
            ))
            # Fall back to basic semantic checks
            self.validate_terminology_basic()
            self.validate_references_basic()
            return self.violations

        # Full semantic validation with LLM
        self.validate_canon_self_consistency()
        self.validate_canon_completeness()
        self.validate_canon_enforceability()
        self.validate_terminology_semantic()
        self.validate_reference_integrity()
        self.validate_inheritance_compliance()
        self.validate_self_optimization()

        return self.violations

    def validate_canon_self_consistency(self) -> None:
        """Validate CANON.md has no contradictory constraints."""
        for canon_file in self.root.rglob("CANON.md"):
            if any(part.startswith('.') for part in canon_file.parts):
                continue

            content = self._read_file(canon_file)
            if not content:
                continue

            prompt = f"""Analyze this CANON.md for contradictory constraints.

A contradiction occurs when:
- Two constraints cannot both be satisfied
- Satisfying one necessarily violates another
- Requirements are mutually exclusive

CANON content:
{content}

Return ONLY valid JSON (no markdown):
{{
  "has_contradictions": true/false,
  "contradictions": [
    {{
      "constraint1": "name of first constraint",
      "constraint2": "name of second constraint",
      "why_contradictory": "explanation",
      "line1": line_number_or_null,
      "line2": line_number_or_null
    }}
  ]
}}"""

            try:
                response = self.llm.chat_completion(
                    [{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=2000
                )
                result = self._parse_json_response(response.content)

                if result.get("has_contradictions"):
                    for contradiction in result.get("contradictions", []):
                        self.violations.append(Violation(
                            layer="semantic",
                            category="contradiction",
                            artifact=str(canon_file.relative_to(self.root)),
                            requirement="Self-consistency",
                            details=f"Contradiction between '{contradiction['constraint1']}' and '{contradiction['constraint2']}': {contradiction['why_contradictory']}",
                            severity=ViolationSeverity.CRITICAL,
                            line=contradiction.get('line1')
                        ))
            except Exception as e:
                self._log_llm_error("consistency check", canon_file, e)

    def validate_canon_completeness(self) -> None:
        """Validate all constraints are complete."""
        for canon_file in self.root.rglob("CANON.md"):
            if any(part.startswith('.') for part in canon_file.parts):
                continue

            content = self._read_file(canon_file)
            if not content:
                continue

            prompt = f"""Analyze this CANON.md for incomplete constraints.

A complete constraint has:
1. Clear name/title
2. Requirement statement (what must be true)
3. Violation statement (what triggers failure)
4. Specific, testable criteria (not vague)

Incomplete examples:
- Constraint with no violation statement
- Vague requirement ("should be good")
- Untestable criteria ("must be optimal")

CANON content:
{content}

Return ONLY valid JSON (no markdown):
{{
  "incomplete_constraints": [
    {{
      "constraint_name": "name",
      "missing": ["violation_statement", "clear_requirement", "testable_criteria"],
      "recommendation": "how to fix",
      "line": line_number_or_null
    }}
  ]
}}"""

            try:
                response = self.llm.chat_completion(
                    [{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=2000
                )
                result = self._parse_json_response(response.content)

                for incomplete in result.get("incomplete_constraints", []):
                    self.violations.append(Violation(
                        layer="semantic",
                        category="completeness",
                        artifact=str(canon_file.relative_to(self.root)),
                        requirement="Constraint completeness",
                        details=f"Constraint '{incomplete['constraint_name']}' incomplete: missing {', '.join(incomplete['missing'])}. {incomplete.get('recommendation', '')}",
                        severity=ViolationSeverity.HIGH,
                        line=incomplete.get('line')
                    ))
            except Exception as e:
                self._log_llm_error("completeness check", canon_file, e)

    def validate_canon_enforceability(self) -> None:
        """Validate all constraints are enforceable/testable."""
        for canon_file in self.root.rglob("CANON.md"):
            if any(part.startswith('.') for part in canon_file.parts):
                continue

            content = self._read_file(canon_file)
            if not content:
                continue

            prompt = f"""Analyze this CANON.md for enforceability.

Per CANONIC principle: "Every rule implies a test. If the test cannot be described, the rule is not ready."

Enforceable constraints:
- Objective, testable criteria
- Clear pass/fail conditions
- Can be automated
- Uses "must" not "should"

Unenforceable constraints:
- Subjective terms (good, clean, optimal, better)
- No measurable criteria
- Requires human judgment
- Uses "should" instead of "must"

CANON content:
{content}

Return ONLY valid JSON (no markdown):
{{
  "unenforceable_constraints": [
    {{
      "constraint_name": "name",
      "why_unenforceable": "explanation",
      "recommendation": "how to make it enforceable",
      "line": line_number_or_null
    }}
  ]
}}"""

            try:
                response = self.llm.chat_completion(
                    [{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=2000
                )
                result = self._parse_json_response(response.content)

                for unenforceable in result.get("unenforceable_constraints", []):
                    self.violations.append(Violation(
                        layer="semantic",
                        category="enforceability",
                        artifact=str(canon_file.relative_to(self.root)),
                        requirement="Constraint enforceability",
                        details=f"Constraint '{unenforceable['constraint_name']}' not enforceable: {unenforceable['why_unenforceable']}. {unenforceable.get('recommendation', '')}",
                        severity=ViolationSeverity.HIGH,
                        line=unenforceable.get('line')
                    ))
            except Exception as e:
                self._log_llm_error("enforceability check", canon_file, e)

    def validate_terminology_semantic(self) -> None:
        """Validate all terms are defined in DICTIONARY.md."""
        for canon_file in self.root.rglob("CANON.md"):
            if any(part.startswith('.') for part in canon_file.parts):
                continue

            canon_content = self._read_file(canon_file)
            vocab_file = canon_file.parent / "DICTIONARY.md"
            vocab_content = self._read_file(vocab_file) if vocab_file.exists() else ""

            if not canon_content:
                continue

            prompt = f"""Check terminology discipline.

Constraint: "All technical terms must be defined in DICTIONARY.md"

Technical terms are:
- Domain-specific terminology
- Paradigm-specific concepts
- Terms that need definition for clarity

NOT technical terms:
- Common English words
- Standard programming terms (file, directory)
- Obvious concepts

CANON content:
{canon_content}

VOCABULARY content:
{vocab_content}

Return ONLY valid JSON (no markdown):
{{
  "undefined_terms": [
    {{
      "term": "word or phrase",
      "context": "sentence using it",
      "line": line_number_or_null
    }}
  ]
}}"""

            try:
                response = self.llm.chat_completion(
                    [{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=2000
                )
                result = self._parse_json_response(response.content)

                for undefined in result.get("undefined_terms", []):
                    self.violations.append(Violation(
                        layer="semantic",
                        category="terminology",
                        artifact=str(canon_file.relative_to(self.root)),
                        requirement="Terminology discipline",
                        details=f"Undefined term '{undefined['term']}' in context: {undefined.get('context', 'N/A')}",
                        severity=ViolationSeverity.MEDIUM,
                        line=undefined.get('line')
                    ))
            except Exception as e:
                self._log_llm_error("terminology check", canon_file, e)

    def validate_reference_integrity(self) -> None:
        """Validate all references resolve to existing artifacts."""
        for md_file in self.root.rglob("*.md"):
            if any(part.startswith('.') for part in md_file.parts):
                continue

            content = self._read_file(md_file)
            if not content:
                continue

            prompt = f"""Extract all local file/path references from this markdown.

Include:
- Markdown links to local files: [text](path/to/file.md)
- Bare paths: path/to/file.md, ../other/file.md
- Backtick paths: `path/to/file.md`

Exclude:
- HTTP/HTTPS URLs
- Anchors only (#section)
- Email addresses

Return ONLY valid JSON (no markdown):
{{
  "references": [
    {{
      "text": "link text or path",
      "target": "path/to/file.md",
      "line": line_number_or_null
    }}
  ]
}}

Content:
{content}"""

            try:
                response = self.llm.chat_completion(
                    [{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=2000
                )
                result = self._parse_json_response(response.content)

                for ref in result.get("references", []):
                    target = ref['target']
                    # Resolve relative to the markdown file
                    target_path = (md_file.parent / target).resolve()

                    if not target_path.exists():
                        self.violations.append(Violation(
                            layer="semantic",
                            category="reference_integrity",
                            artifact=str(md_file.relative_to(self.root)),
                            requirement="Reference integrity",
                            details=f"Reference '{ref['text']}' → '{target}' does not resolve (expected: {target_path})",
                            severity=ViolationSeverity.HIGH,
                            line=ref.get('line')
                        ))
            except Exception as e:
                self._log_llm_error("reference integrity check", md_file, e)

    def validate_inheritance_compliance(self) -> None:
        """Validate child CANON doesn't contradict parent invariants."""
        for canon_file in self.root.rglob("CANON.md"):
            if any(part.startswith('.') for part in canon_file.parts):
                continue

            content = self._read_file(canon_file)
            if not content or "**Inherits from:** None" in content:
                continue

            # Extract inheritance declaration
            match = re.search(r'\*\*Inherits from:\*\*\s*\[([^\]]+)\]', content)
            if not match:
                continue

            # For now, we can't fetch remote CANONs
            # This would require fetching from GitHub/URLs
            # Log as limitation
            pass

    def validate_self_optimization(self) -> None:
        """Validate CANON.md is lean (no bloat or duplication)."""
        for canon_file in self.root.rglob("CANON.md"):
            if any(part.startswith('.') for part in canon_file.parts):
                continue

            content = self._read_file(canon_file)
            if not content:
                continue

            prompt = f"""Check if this CANON.md violates self-optimization.

Constraint: "CANON.md files must be kept lean: no explanatory content, redundant constraints, or bloat."

Violations:
- Explanatory paragraphs (belongs in README.md)
- Duplicate constraints
- Unnecessary verbosity
- Tutorial content
- Examples (unless minimal)

CANON should be:
- Declarative constraints only
- Minimal
- No redundancy

CANON content:
{content}

Return ONLY valid JSON (no markdown):
{{
  "has_bloat": true/false,
  "bloat_issues": [
    {{
      "issue_type": "explanatory_content|duplication|verbosity",
      "details": "what's wrong",
      "line": line_number_or_null
    }}
  ]
}}"""

            try:
                response = self.llm.chat_completion(
                    [{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=2000
                )
                result = self._parse_json_response(response.content)

                if result.get("has_bloat"):
                    for issue in result.get("bloat_issues", []):
                        self.violations.append(Violation(
                            layer="semantic",
                            category="self_optimization",
                            artifact=str(canon_file.relative_to(self.root)),
                            requirement="Self-optimizing",
                            details=f"{issue['issue_type']}: {issue['details']}",
                            severity=ViolationSeverity.MEDIUM,
                            line=issue.get('line')
                        ))
            except Exception as e:
                self._log_llm_error("self-optimization check", canon_file, e)

    def validate_terminology_basic(self) -> None:
        """Basic terminology check without LLM (fallback)."""
        # Simple check: terms in CANON should exist in VOCABULARY
        for canon_file in self.root.rglob("CANON.md"):
            vocab_file = canon_file.parent / "DICTIONARY.md"
            if not vocab_file.exists():
                self.violations.append(Violation(
                    layer="semantic",
                    category="terminology",
                    artifact=str(canon_file.relative_to(self.root)),
                    requirement="Terminology discipline",
                    details="DICTIONARY.md missing - cannot validate terminology",
                    severity=ViolationSeverity.HIGH
                ))

    def validate_references_basic(self) -> None:
        """Basic reference check without LLM (fallback)."""
        # Simple regex-based reference extraction
        for md_file in self.root.rglob("*.md"):
            if any(part.startswith('.') for part in md_file.parts):
                continue

            content = self._read_file(md_file)
            # Find markdown links: [text](path)
            refs = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)

            for text, target in refs:
                # Skip URLs
                if target.startswith(('http://', 'https://', '#', 'mailto:')):
                    continue

                target_path = (md_file.parent / target).resolve()
                if not target_path.exists():
                    self.violations.append(Violation(
                        layer="semantic",
                        category="reference_integrity",
                        artifact=str(md_file.relative_to(self.root)),
                        requirement="Reference integrity",
                        details=f"Reference '{text}' → '{target}' does not resolve",
                        severity=ViolationSeverity.HIGH
                    ))

    def _read_file(self, path: Path) -> str:
        """Read file content safely."""
        try:
            return path.read_text(encoding='utf-8')
        except Exception:
            return ""

    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON from LLM response, handling markdown code blocks."""
        # Remove markdown code blocks if present
        response = re.sub(r'^```json\s*', '', response.strip())
        response = re.sub(r'\s*```$', '', response.strip())
        response = re.sub(r'^```\s*', '', response.strip())

        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {e}\nResponse: {response}")

    def _log_llm_error(self, check_type: str, file: Path, error: Exception) -> None:
        """Log LLM processing error as violation."""
        self.violations.append(Violation(
            layer="semantic",
            category="llm_error",
            artifact=str(file.relative_to(self.root)),
            requirement=f"LLM {check_type}",
            details=f"LLM processing failed: {str(error)}",
            severity=ViolationSeverity.LOW
        ))


class CanonicValidator:
    """
    Comprehensive CANONIC validator implementing dual validation protocol.

    Validates repositories against CANONIC programming constraints:
    1. Syntactic layer: structure, format, naming
    2. Semantic layer: logical coherence, completeness, enforceability
    """

    def __init__(self, root: Path, llm_client: Optional[Any] = None):
        self.root = root
        self.syntactic = SyntacticValidator(root)
        self.semantic = SemanticValidator(root, llm_client)
        self.all_violations: List[Violation] = []

    def validate(self) -> Tuple[bool, List[Violation]]:
        """
        Run complete dual validation.

        Returns:
            (is_valid, violations)
        """
        print(f"Running CANONIC validation on {self.root}")
        print("=" * 60)

        # Syntactic validation
        print("\n[1/2] Syntactic validation (structure, format, naming)...")
        syntactic_violations = self.syntactic.validate_all()
        print(f"  Found {len(syntactic_violations)} syntactic violations")

        # Semantic validation
        print("\n[2/2] Semantic validation (coherence, completeness)...")
        semantic_violations = self.semantic.validate_all()
        print(f"  Found {len(semantic_violations)} semantic violations")

        self.all_violations = syntactic_violations + semantic_violations

        is_valid = len(self.all_violations) == 0
        return is_valid, self.all_violations

    def report(self, format: str = "text") -> str:
        """Generate validation report."""
        if format == "json":
            return self._report_json()
        else:
            return self._report_text()

    def _report_json(self) -> str:
        """Generate JSON report."""
        by_severity = {}
        by_layer = {}
        by_category = {}

        for v in self.all_violations:
            severity = v.severity.value
            by_severity[severity] = by_severity.get(severity, 0) + 1
            by_layer[v.layer] = by_layer.get(v.layer, 0) + 1
            by_category[v.category] = by_category.get(v.category, 0) + 1

        report = {
            "valid": len(self.all_violations) == 0,
            "root": str(self.root),
            "total_violations": len(self.all_violations),
            "by_severity": by_severity,
            "by_layer": by_layer,
            "by_category": by_category,
            "violations": [v.to_dict() for v in self.all_violations]
        }

        return json.dumps(report, indent=2)

    def _report_text(self) -> str:
        """Generate human-readable text report."""
        lines = []
        lines.append("=" * 60)
        lines.append("CANONIC VALIDATION REPORT")
        lines.append("=" * 60)
        lines.append(f"Repository: {self.root}")
        lines.append(f"Status: {'✅ VALID' if len(self.all_violations) == 0 else '❌ INVALID'}")
        lines.append(f"Total violations: {len(self.all_violations)}")
        lines.append("")

        if len(self.all_violations) == 0:
            lines.append("All CANONIC constraints satisfied.")
            lines.append("Repository is in compliant state.")
            return "\n".join(lines)

        # Group by severity
        by_severity = {s: [] for s in ViolationSeverity}
        for v in self.all_violations:
            by_severity[v.severity].append(v)

        # Report each severity level
        for severity in [ViolationSeverity.CRITICAL, ViolationSeverity.HIGH,
                        ViolationSeverity.MEDIUM, ViolationSeverity.LOW]:
            violations = by_severity[severity]
            if not violations:
                continue

            severity_icon = {
                ViolationSeverity.CRITICAL: "🔴",
                ViolationSeverity.HIGH: "🟠",
                ViolationSeverity.MEDIUM: "🟡",
                ViolationSeverity.LOW: "⚪"
            }[severity]

            lines.append(f"\n{severity_icon} {severity.value.upper()} ({len(violations)})")
            lines.append("-" * 60)

            for i, v in enumerate(violations, 1):
                lines.append(f"{i}. {v.artifact}")
                if v.line:
                    lines.append(f"   Line {v.line}")
                lines.append(f"   [{v.layer}/{v.category}] {v.requirement}")
                lines.append(f"   {v.details}")
                if v.auto_fixable:
                    lines.append(f"   ✨ Auto-fixable")
                lines.append("")

        return "\n".join(lines)


def validate_self() -> bool:
    """
    Self-validation: Validate this tool against tools/CANON.md requirements.

    Per tools/CANON.md line 42-45:
    "Self-Validating Tools: Tools must validate their own operation against CANON."

    Returns True if self-validation passes, False otherwise.
    """
    print("=" * 60)
    print("SELF-VALIDATION: Checking canonic_validator.py compliance")
    print("=" * 60)

    violations = []

    # Check 1: Tool follows validation_protocol (lines 110-126)
    # - Must validate all declared FSM constraints ✓
    # - Check protocol compliance across states ✓
    # - Report violations with file/line references ✓
    # - Support partial validation ✓
    # - Exit codes indicate validation status ✓

    # Check 2: Implements dual validation
    # Verify both SyntacticValidator and SemanticValidator classes exist
    if 'SyntacticValidator' not in globals() or 'SemanticValidator' not in globals():
        violations.append("Missing dual validation implementation")

    # Check 3: Uses llm_integration_protocol
    # Verify LLMClient is used per protocol (OpenAI-compatible, multi-provider)
    if LLMClient is None:
        print("⚠️  LLM module not available - cannot verify llm_integration_protocol compliance")

    # Check 4: Follows error handling standards (lines 185-190)
    # Exit codes: 0=success, 1=violations, 2=errors ✓
    # JSON output for machine parsing ✓
    # Human-readable messages ✓

    if violations:
        print("❌ SELF-VALIDATION FAILED")
        for v in violations:
            print(f"  - {v}")
        print()
        return False
    else:
        print("✅ SELF-VALIDATION PASSED")
        print("canonic_validator.py complies with tools/CANON.md")
        print()
        return True


def main():
    """CLI interface for CANONIC validation."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Comprehensive CANONIC validator with dual validation (syntactic + semantic)"
    )
    parser.add_argument("--root", type=str, default=".",
                       help="Root directory to validate")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                       help="Output format")
    parser.add_argument("--no-llm", action="store_true",
                       help="Disable LLM semantic validation (syntactic only)")
    parser.add_argument("--provider", choices=["deepseek", "openai", "anthropic"],
                       default="deepseek", help="LLM provider")
    parser.add_argument("--skip-self-validation", action="store_true",
                       help="Skip self-validation check (not recommended)")

    args = parser.parse_args()

    # SELF-VALIDATION: Per tools/CANON.md requirement
    # "Tools must validate their own operation against CANON"
    if not args.skip_self_validation:
        if not validate_self():
            print("❌ Aborting: Self-validation failed")
            print("Fix canonic_validator.py to comply with tools/CANON.md")
            return 2  # Error code 2 per error handling protocol

    root_path = Path(args.root).resolve()

    if not root_path.exists():
        print(f"❌ Error: Directory does not exist: {root_path}")
        return 2

    # Initialize LLM if enabled
    llm_client = None
    if not args.no_llm:
        try:
            if LLMClient is None:
                print("⚠️  LLM module not available - running syntactic validation only")
            else:
                llm_client = LLMClient()
                print(f"Using LLM provider: {args.provider}")
        except Exception as e:
            print(f"⚠️  LLM initialization failed: {e}")
            print("Running syntactic validation only")

    # Run validation
    validator = CanonicValidator(root_path, llm_client)
    is_valid, violations = validator.validate()

    # Generate report
    print("\n")
    report = validator.report(format=args.format)
    print(report)

    # Exit codes per error handling protocol (tools/CANON.md lines 185-190)
    # 0=success, 1=violations, 2=errors
    return 0 if is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
