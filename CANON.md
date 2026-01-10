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
   upper case is reserved for artifacts that govern like SPEC, CANON, VOCAB, README, PROTOCOLS
   lower case is reserved for governed artifacts like episodes and templates
   non-triad artifacts use `SPEC-###_stub` naming
   the prefix is a three-digit numeric prefix
   the `000` prefix is reserved for the SPEC artifact itself
   the stub is lowercase kebab-case
