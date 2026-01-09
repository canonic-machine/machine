# MACHINE Spec

1. Purpose
   - Enforce the minimal CANONIC triad and invariants through the validation layer.

2. Scope
   - Applies to `/machine` and informs downstream validation behavior.

3. Constraints
   - Maintain the triad for machine scopes.
   - Perform correction through history-preserving change.
   - Enforce required ordering (e.g., alphabetical VOCAB terms).
   - Use CANONIC templates as the blueprint for governance artifacts.

4. Validation
   - Confirm triad presence and inheritance declarations.
   - Validate ordering requirements where defined.
   - Apply correction without rewriting history.

5. Consumption notes
   - Downstream layers inherit these constraints without contradicting CANONIC.
   - When machine terms change, downstream VOCABs must add the new terms.

This SPEC inherits the root triad and references VOCAB for definitions.
