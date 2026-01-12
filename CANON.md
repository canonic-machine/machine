# MACHINE (/canonic/machine/)

inherits: /canonic

---

## Axioms

### 1. Authority

MACHINE **MUST** enforce inherited CANON only.

MACHINE **MUST NOT** introduce, modify, or extend governance.

---

### 2. Input

MACHINE **MUST** consume:

- candidate system states, and
- governing CANON (including inherited CANON)

---

### 3. Evaluation

MACHINE **MUST** evaluate candidate system states exclusively against governing CANON.

---

### 4. Decision

MACHINE **MUST** produce a binary outcome for each evaluated candidate state:

- accept, or
- reject

---

### 5. Signal

MACHINE **MAY** emit non-authoritative signals describing evaluation results.

Signals **MUST NOT** be treated as governance or persistence.

---

### 6. Determinism

Given identical inputs, MACHINE **MUST** produce identical outcomes.

---

**This CANON defines validity for the MACHINE scope.**
**Protocols, agents, and tooling are defined in downstream scopes.**

---