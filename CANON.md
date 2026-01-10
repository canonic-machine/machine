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
   CANON, TRIAD, and SPEC are uppercase identifiers
   other artifact labels are lowercase in prose, including vocab, readme, protocols, templates, and episodes
   non-triad artifacts use `series-###_stub` naming
   the prefix is a numeric order
   the `00` prefix is reserved for the SPEC artifact itself, named `series-00-SPEC.md`
   the spec stub is SPEC; other stubs are lowercase kebab-case
