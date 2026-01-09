MACHINE (/)

inherits: /

axioms:

1. triad:
   a machine scope contains CANON.md, VOCAB.md, README.md

2. inheritance:
   every machine CANON declares the scope it inherits from
   inheritance terminates at /
   inherited axioms are final and cannot be overridden

3. coherence:
   a machine scope is coherent iff its CANON statements do not contradict inherited CANON

4. compliance:
   a machine scope is compliant iff the triad exists and inheritance is declared

5. governance:
   a machine scope is governed iff it is coherent and compliant

6. invalidity:
   any machine scope not governed is invalid

7. introspection:
   VOCAB defines the terms used by this CANON and itself

8. correction:
   invalid states are corrected by history-preserving change in the machine layer

9. ordering:
   machine validation enforces required ordering (e.g., alphabetical VOCAB terms)

10. templating:
   machine hosts and applies canonical templates for CANON, VOCAB, README, and SPEC
