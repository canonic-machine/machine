#!/usr/bin/env python3
"""Modular validators for CANONIC programming artifacts."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Set, Optional
import re

from config import REQUIREMENTS, TRIAD_FILES


class Validator(ABC):
    """Base class for all validators."""
    
    def __init__(self, root: Path):
        self.root = root
        self.violations: List[Dict[str, Any]] = []
    
    @abstractmethod
    def validate(self) -> List[Dict[str, Any]]:
        """Run validation and return violations."""
        pass
    
    def format_artifact_path(self, path: Path) -> str:
        """Format artifact path relative to root."""
        rel = path.relative_to(self.root)
        rel_str = str(rel)
        return rel_str if rel_str else "."
    
    def add_violation(
        self,
        artifact: str,
        requirement: str,
        details: str,
        line: Optional[int] = None
    ) -> None:
        """Add a violation to the list."""
        self.violations.append({
            "artifact": artifact,
            "line": line,
            "requirement": requirement,
            "details": details,
        })


class TriadValidator(Validator):
    """Validates that all directories contain the triad files."""
    
    def validate(self) -> List[Dict[str, Any]]:
        """Check for missing triad files in all directories."""
        import os
        
        for dirpath, dirnames, filenames in os.walk(self.root):
            # Skip hidden directories
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            dirnames.sort()
            
            path = Path(dirpath).resolve()
            missing = [name for name in TRIAD_FILES if name not in filenames]
            
            if missing:
                self.add_violation(
                    artifact=self.format_artifact_path(path),
                    requirement=REQUIREMENTS["TRIAD"],
                    details=f"Directory is missing triad files: {', '.join(missing)}.",
                    line=136
                )
        
        return self.violations


class RequiredArtifactsValidator(Validator):
    """Validates that required artifacts exist."""
    
    def validate(self) -> List[Dict[str, Any]]:
        """Check for missing required artifacts."""
        canon_path = self.root / "CANON.md"
        required = self._parse_required_artifacts(canon_path)
        
        for entry in required:
            name = entry["name"]
            artifact_path = self.root / name
            if not artifact_path.exists():
                self.add_violation(
                    artifact=self.format_artifact_path(artifact_path),
                    requirement=REQUIREMENTS["REQUIRED_ARTIFACTS"],
                    details=f"Required artifact '{name}' is missing.",
                    line=entry["line"]
                )
        
        return self.violations
    
    def _parse_required_artifacts(self, canon_path: Path) -> List[Dict[str, Any]]:
        """Parse required artifacts from CANON.md."""
        required: List[Dict[str, Any]] = []
        section_open: bool = False
        
        if not canon_path.exists():
            return required
        
        with canon_path.open(encoding="utf-8") as fp:
            for line_number, line in enumerate(fp, start=1):
                stripped: str = line.strip()
                if stripped == "## Required Artifacts (root level)":
                    section_open = True
                    continue
                if not section_open:
                    continue
                if stripped.startswith("## "):
                    break
                if line.startswith("- "):
                    name_part: str = line[2:].split()[0] if len(line) > 2 else ""
                    if name_part:
                        required.append({"name": name_part, "line": line_number})
        
        return required


class TerminologyValidator(Validator):
    """Validates terminology usage against VOCABULARY.md."""
    
    def validate(self) -> List[Dict[str, Any]]:
        """Check that terms are defined before use."""
        import os
        
        aggregated_terms: Dict[Path, Set[str]] = {}
        
        for dirpath, dirnames, filenames in os.walk(self.root):
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            dirnames.sort()
            
            path = Path(dirpath).resolve()
            
            # Get parent terms
            if path == self.root:
                parent_terms = set()
            else:
                parent_terms = aggregated_terms.get(path.parent, set())
            
            # Parse local vocabulary
            vocab_path = path / "VOCABULARY.md"
            terms = self._parse_vocab_terms(vocab_path)
            
            # Aggregate terms
            aggregated = parent_terms.union(terms.keys())
            aggregated_terms[path] = aggregated
            
            # Validate documents (placeholder - full implementation would check term usage)
            for doc in ("CANON.md", "README.md"):
                doc_path = path / doc
                if doc_path.exists():
                    doc_path.read_text(encoding="utf-8")
        
        return self.violations
    
    def _parse_vocab_terms(self, vocab_path: Path) -> Dict[str, int]:
        """Parse terms from VOCABULARY.md."""
        terms: Dict[str, int] = {}
        if not vocab_path.exists():
            return terms
        
        with vocab_path.open(encoding="utf-8") as fp:
            for line_number, line in enumerate(fp, start=1):
                if line.startswith("### "):
                    term: str = line[4:].strip()
                    if term:
                        terms[term] = line_number
        
        return terms


class FSMValidator(Validator):
    """Validates Finite State Machine artifacts (user-guide specific)."""
    
    def validate(self) -> List[Dict[str, Any]]:
        """Validate FSM structure."""
        user_guide = self.root / "user-guide"
        if not user_guide.exists():
            return self.violations
        
        ledger_path = user_guide / "assets" / "LEDGER.md"
        episodes_dir = user_guide / "episodes"
        prose_path = user_guide / "prose" / "draft.md"
        structure_path = user_guide / "structure" / "outline.md"
        
        # Validate asset ledger
        asset_ids, asset_sources = self._parse_asset_ledger(ledger_path)
        episode_ids = self._list_episode_ids(episodes_dir)
        
        # Validate prose references
        self._validate_prose_references(prose_path, asset_ids)
        
        # Validate asset sources
        self._validate_asset_sources(asset_sources, episode_ids, ledger_path)
        
        # Validate structure
        structure_sections = self._parse_structure_sections(structure_path)
        prose_sections = self._parse_prose_sections(prose_path)
        self._validate_structure_order(structure_sections, prose_sections, structure_path, prose_path)
        
        return self.violations
    
    def _parse_asset_ledger(self, ledger_path: Path) -> tuple[Set[str], Dict[str, Dict[str, Any]]]:
        """Parse asset ledger."""
        asset_ids: Set[str] = set()
        asset_sources: Dict[str, Dict[str, Any]] = {}
        
        if not ledger_path.exists():
            self.add_violation(
                artifact=self.format_artifact_path(ledger_path),
                requirement=REQUIREMENTS["USER_GUIDE_ASSET"],
                details="Missing assets/LEDGER.md; cannot validate asset references."
            )
            return asset_ids, asset_sources
        
        expected_next_id = 1
        with ledger_path.open(encoding="utf-8") as fp:
            for line_number, line in enumerate(fp, start=1):
                stripped = line.strip()
                if not stripped.startswith("| asset-"):
                    continue
                
                columns = [col.strip() for col in stripped.strip("|").split("|")]
                if not columns:
                    continue
                
                asset_id = columns[0]
                
                # Validate format
                if not re.match(r"^asset-\d{4}$", asset_id):
                    self.add_violation(
                        artifact=self.format_artifact_path(ledger_path),
                        requirement=REQUIREMENTS["USER_GUIDE_ASSET"],
                        details=f"Asset ID '{asset_id}' has invalid format (expected: asset-NNNN with 4 digits).",
                        line=line_number
                    )
                else:
                    # Check sequential
                    id_num = int(asset_id.split("-")[1])
                    if id_num != expected_next_id:
                        self.add_violation(
                            artifact=self.format_artifact_path(ledger_path),
                            requirement=REQUIREMENTS["USER_GUIDE_ASSET"],
                            details=f"Asset ID {asset_id} breaks sequential order (expected: asset-{expected_next_id:04d}).",
                            line=line_number
                        )
                    expected_next_id = id_num + 1
                
                source_value = columns[3] if len(columns) > 3 else ""
                sources = [s.strip() for s in source_value.split(",") if s.strip()]
                asset_ids.add(asset_id)
                asset_sources[asset_id] = {"line": line_number, "sources": sources}
        
        return asset_ids, asset_sources
    
    def _list_episode_ids(self, episodes_dir: Path) -> Set[str]:
        """List episode IDs from directory."""
        ids: Set[str] = set()
        if not episodes_dir.exists():
            return ids
        
        for entry in episodes_dir.iterdir():
            if not entry.is_file() or entry.name in TRIAD_FILES:
                continue
            
            name = entry.name
            if not re.match(r"^episode-\d{2}\.md$", name):
                self.add_violation(
                    artifact=self.format_artifact_path(entry),
                    requirement=REQUIREMENTS["USER_GUIDE_ASSET"],
                    details=f"Episode filename '{name}' has invalid format (expected: episode-NN.md with 2 digits)."
                )
            
            if name.startswith("episode-") and name.endswith(".md"):
                id_part = name[len("episode-"):-len(".md")]
                if id_part:
                    ids.add(id_part)
        
        return ids
    
    def _validate_prose_references(self, prose_path: Path, asset_ids: Set[str]) -> None:
        """Validate prose asset references."""
        if not prose_path.exists():
            self.add_violation(
                artifact=self.format_artifact_path(prose_path),
                requirement=REQUIREMENTS["USER_GUIDE_ASSET"],
                details="Missing prose/draft.md; FSM validation requires prose to exist."
            )
            return
        
        pattern = re.compile(r"asset-\d{4}")
        missing: Set[str] = set()
        
        with prose_path.open(encoding="utf-8") as fp:
            for line_number, line in enumerate(fp, start=1):
                for match in pattern.finditer(line):
                    asset_id = match.group(0)
                    if asset_id not in asset_ids and asset_id not in missing:
                        missing.add(asset_id)
                        self.add_violation(
                            artifact=self.format_artifact_path(prose_path),
                            requirement=REQUIREMENTS["USER_GUIDE_ASSET"],
                            details=f"Prose references {asset_id} which is not registered in assets/LEDGER.md.",
                            line=line_number
                        )
    
    def _validate_asset_sources(
        self,
        asset_sources: Dict[str, Dict[str, Any]],
        episode_ids: Set[str],
        ledger_path: Path
    ) -> None:
        """Validate asset source episodes."""
        for asset_id, meta in asset_sources.items():
            sources = meta["sources"]
            if not sources:
                self.add_violation(
                    artifact=self.format_artifact_path(ledger_path),
                    requirement=REQUIREMENTS["USER_GUIDE_ASSET"],
                    details=f"Asset {asset_id} lists no Source Episode in LEDGER.md.",
                    line=meta["line"]
                )
                continue
            
            for episode_id in sources:
                if episode_id not in episode_ids:
                    self.add_violation(
                        artifact=self.format_artifact_path(ledger_path),
                        requirement=REQUIREMENTS["USER_GUIDE_ASSET"],
                        details=f"Asset {asset_id} references episode {episode_id} but no such episode file exists.",
                        line=meta["line"]
                    )
    
    def _parse_structure_sections(self, structure_path: Path) -> List[Dict[str, Any]]:
        """Parse structure sections."""
        sections: List[Dict[str, Any]] = []
        if not structure_path.exists():
            return sections
        
        with structure_path.open(encoding="utf-8") as fp:
            for line_number, line in enumerate(fp, start=1):
                stripped = line.strip()
                if not stripped.startswith("## Section"):
                    continue
                title = stripped.split(":", 1)[1].strip() if ":" in stripped else stripped[len("## Section"):].strip()
                sections.append({"name": title, "line": line_number})
        
        return sections
    
    def _parse_prose_sections(self, prose_path: Path) -> List[Dict[str, Any]]:
        """Parse prose sections."""
        sections: List[Dict[str, Any]] = []
        if not prose_path.exists():
            return sections
        
        with prose_path.open(encoding="utf-8") as fp:
            for line_number, line in enumerate(fp, start=1):
                stripped = line.strip()
                if stripped.startswith("## "):
                    sections.append({"name": stripped[3:].strip(), "line": line_number})
        
        return sections
    
    def _validate_structure_order(
        self,
        structure_sections: List[Dict[str, Any]],
        prose_sections: List[Dict[str, Any]],
        structure_path: Path,
        prose_path: Path
    ) -> None:
        """Validate structure section order."""
        if not structure_path.exists():
            self.add_violation(
                artifact=self.format_artifact_path(structure_path),
                requirement=REQUIREMENTS["USER_GUIDE_STRUCTURE"],
                details="Missing structure/outline.md; cannot verify section order."
            )
            return
        
        if not prose_path.exists():
            return
        
        last_index = -1
        for section in structure_sections:
            name = section["name"]
            structure_line = section["line"]
            found_index = None
            found_line = None
            
            for idx, entry in enumerate(prose_sections):
                if entry["name"] == name:
                    found_index = idx
                    found_line = entry["line"]
                    break
            
            if found_index is None:
                self.add_violation(
                    artifact=self.format_artifact_path(structure_path),
                    requirement=REQUIREMENTS["USER_GUIDE_STRUCTURE"],
                    details=f"Structure section '{name}' cannot be found in prose/draft.md.",
                    line=structure_line
                )
                continue
            
            if found_index <= last_index:
                self.add_violation(
                    artifact=self.format_artifact_path(prose_path),
                    requirement=REQUIREMENTS["USER_GUIDE_STRUCTURE"],
                    details=f"Section '{name}' appears out of order relative to structure/outline.md.",
                    line=found_line
                )

            last_index = found_index


class FSMSpecNamingValidator(Validator):
    """Validates that the FSM specification file is named MACHINE.md in the root of the machine repo."""

    def validate(self) -> List[Dict[str, Any]]:
        machine_root = self.root
        # Only run if this is the machine repo (directory name is 'machine')
        if machine_root.name != "machine":
            return self.violations

        # Check for MACHINE.md
        machine_spec = machine_root / "MACHINE.md"
        if not machine_spec.exists():
            self.add_violation(
                artifact=self.format_artifact_path(machine_root),
                requirement="CANON.md: Required FSM spec file must be named MACHINE.md (matches repo name)",
                details="FSM specification file is missing or not named MACHINE.md."
            )
        # Check for legacy/misnamed FSM_SPECIFICATION.md
        legacy = machine_root / "FSM_SPECIFICATION.md"
        if legacy.exists():
            self.add_violation(
                artifact=self.format_artifact_path(legacy),
                requirement="CANON.md: FSM spec file must be named MACHINE.md",
                details="Legacy FSM_SPECIFICATION.md exists; must be renamed to MACHINE.md."
            )
        return self.violations
