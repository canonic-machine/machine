MACHINE (/)

inherits: /

axioms:

1. input:
   a machine consumes a structure and a specification

2. evaluation:
   a machine evaluates the structure against the specification

3. decision:
   a machine produces a binary outcome

4. signal:
   a machine emits non-authoritative signals describing evaluation

5. determinism:
   identical inputs produce identical outcomes

6. protocols:
   a machine hosts CANONIC protocols that enforce CANONIC axioms, CANONIC SPEC constraints, and machine axioms
   protocols accept input and yield a decision and a signal

7. nomenclature:
   non-triad artifacts use `###-SPEC_stub` naming
   the prefix is a three-digit numeric prefix
   the prefix order is static in CANON
   artifacts are consecutive and generative
   the `000` prefix is reserved for the SPEC artifact itself
   the stub is lowercase kebab-case
