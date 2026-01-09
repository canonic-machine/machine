# MACHINE Spec

1. Purpose
   - Enforce the minimal CANONIC triad and invariants through the validation layer.

2. Scope
   - Applies to `/machine` and informs downstream validation behavior.

3. Constraints
   - Maintain the triad for machine scopes.
   - Enforce finality of inherited CANONIC axioms.
   - Perform correction through history-preserving change.
   - Enforce required ordering (e.g., alphabetical VOCAB terms).
   - Host and apply CANONIC templates as the blueprint for governance artifacts.

4. Validation
   - Confirm triad presence and inheritance declarations.
   - Verify inherited axioms are not overridden.
   - Validate ordering requirements where defined.
   - Apply correction without rewriting history.

5. Consumption notes
   - Downstream layers inherit these constraints without contradicting CANONIC.
   - When machine terms change, downstream VOCABs must add the new terms.

This SPEC inherits the root triad and references VOCAB for definitions.
