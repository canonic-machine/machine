# MACHINE

## 1. Purpose

Define the MACHINE scope as the enforcement layer of the CANONIC system.

MACHINE exists to enforce governing CANON deterministically. It does not define governance, insight, or execution semantics.

---

## 2. Scope

- Applies to `/canonic/machine/`.
- Inherits all constitutional constraints from `/canonic`.
- Provides enforcement semantics for downstream scopes.

---

## 3. Principles

### 3.1 Governance separation

MACHINE enforces governing CANON only.

- Governance is declared exclusively by CANON.
- MACHINE has no authority to introduce, modify, or interpret governance.

---

### 3.2 Enforcement domain

MACHINE operates solely on:

- candidate system states, and
- governing CANON (including inherited CANON).

MACHINE does not consume SPEC, narrative, or insight artifacts.

---

### 3.3 Deterministic evaluation

MACHINE evaluates candidate states deterministically against governing CANON.

Given identical inputs, MACHINE produces identical outcomes.

---

### 3.4 Binary decision

For each evaluated candidate state, MACHINE produces exactly one outcome:

- accept, or
- reject

There are no intermediate or advisory states.

---

### 3.5 Non-authoritative signals

MACHINE may emit signals describing evaluation results.

Signals:
- are non-authoritative,
- do not constitute governance, and
- do not cause persistence.

---

## 4. Validation

A MACHINE scope is valid if and only if:

- the triad (`CANON.md`, `VOCAB.md`, `README.md`) is present,
- the CANON defines enforcement axioms (authority, input, evaluation, decision, determinism), and
- MACHINE produces deterministic binary outcomes for identical inputs.

---

## 5. Consumption notes

- Downstream scopes may rely on MACHINE enforcement but must not redefine it.
- Protocols, automation, agent behavior, and tooling are defined outside this SPEC.

---

**This SPEC defines the enforcement semantics of MACHINE.**
**Validity is defined exclusively by CANON.**

---