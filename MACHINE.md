# MACHINE SPEC

**Status:** CANONICAL
**Closed:** 2026-01-16

---

## 1. Purpose

Define the enforcement semantics of CANONIC governance.

MACHINE evaluates candidate states against CANON and produces binary outcomes.

---

## 2. Governance Path

```
/canonic/ (ROOT)
├── inherits: / (self-terminating)
│
└──► /canonic/machine/ (THIS SCOPE)
     └── inherits: /canonic/
```

| Field | Value |
|-------|-------|
| Path | `/canonic/machine/` |
| Inherits | `/canonic/` |
| Closes | CANON.md (6 axioms) |

---

## 3. Normative language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are to be interpreted as described in RFC 2119.

---

## 4. Principles

### 4.1 Enforcement without governance

MACHINE enforces but does not govern. It accepts inherited CANON as input and produces accept/reject decisions.

### 4.2 Deterministic evaluation

Given identical inputs (candidate state + governing CANON), MACHINE produces identical outcomes. Non-determinism is a violation.

### 4.3 Signal opacity

MACHINE may emit diagnostic signals, but signals have no governance force. Only accept/reject outcomes matter.

---

## 5. Constraints

MACHINE does not govern:
- CANON definition (governed by root)
- VOCAB semantics (governed by introspection)
- Execution procedures (governed by OS)
- Episode production (governed by WRITING)

---

## 6. Validation

```
VALIDITY = triad(scope) ∧ inheritance(scope) ∧ introspection(scope)
```

MACHINE validity requires:
- CANON.md, VOCAB.md, README.md present
- Inherits from /canonic/
- All CANON terms defined in VOCAB

---

**This SPEC closes CANON. Governance is defined exclusively by CANON.**

---
