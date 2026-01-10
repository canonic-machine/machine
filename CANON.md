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
   spec artifacts are named `00-SPECNAME.md` and are the human entry point
   SPECNAME is uppercase and matches the governed series name
   governing sub-series use `NN-SERIES.md` with uppercase SERIES names
   series order is inherited; numbering is positional and may change to preserve the inherited order
   governed artifacts use a lowercase series abbreviation plus a three-digit order and stub
   governed pattern: `abNNN-stub.md` (example: `ep000-constitutional-compliance.md`)
