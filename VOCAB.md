# VOCAB (/machine)

## Core terms

### CANON
The constraints artifact for a scope.

### CANONIC
The root paradigm scope the machine layer inherits from and enforces.

### SPEC
A declarative artifact that defines patterns or constraints for enforcement.

### README
The narrative artifact that explains a scope.

### VOCAB
The meanings artifact for a scope; it defines the terms used by CANON, SPEC, and README and defines itself.

### triad
The required set of governance artifacts: CANON.md, VOCAB.md, README.md.

### inheritance
The declared linkage from a scope to the scope it inherits from.

### final
The property that inherited axioms cannot be overridden by downstream scopes.

### introspection
The requirement that VOCAB defines itself and the CANON, SPEC, and README it supports.

### machine
The evaluation layer that enforces CANONIC and machine axioms.

### scope
The area governed by a CANON and its triad.

### axiom
A single CANON statement.

### axioms
Plural of axiom.

### input
The structure and specification consumed by the machine.

### structure
The subject evaluated by the machine.

### specification
The criteria a structure is evaluated against.

### evaluation
The act of comparing a structure to a specification.

### decision
The binary outcome of evaluation.

### binary
An outcome with exactly two possible values.

### outcome
The result produced by evaluation.

### signal
A non-authoritative output describing evaluation.

### non-authoritative
Not determining a decision.

### determinism
The property that identical inputs produce identical outcomes.

### identical
The condition that two inputs are the same.

### enforcement
The application of axioms through evaluation.

### validation
The process of checking a scope or evaluation against CANON or SPEC.

### coherence
The property that CANON statements do not contradict inherited CANON.

### compliance
The property that structural requirements (triad + inheritance declaration) are satisfied.

### governance
The state where coherence and compliance both hold.

### invalidity
The state of not being governed.

### documentation
The requirement that README documents the axioms for the scope.

### nomenclature
The canonical naming of governance artifacts and terms; names must not drift.

### minimal canon
The requirement that the machine enforces the smallest sufficient CANON to reduce drift.

### correction
History-preserving change executed by the machine layer to restore governed states.

### ordering
The machine function that enforces required ordering.

### templating
The machine function that hosts and applies canonical templates for CANON, VOCAB, README, and SPEC.

### template
A reusable blueprint for instantiating a governance artifact.

### templates
Plural of template.

### history-preserving
A change that does not rewrite prior states.

### canonical
Conforming to CANON or defined names.

### term
A deliberate word or phrase that must be defined in VOCAB.

### define
To add a term to VOCAB or a rule to CANON or SPEC.

## Supplemental terms

### apply
To use a SPEC to constrain an inherited scope.

### compare
To evaluate a structure against a specification.

### consume
To take an input for evaluation.

### describe
To explain a scope in README.

### derive
To obtain from a prior statement or evaluation.

### emit
To output a signal.

### ensure
To require validation of a statement or constraint.

### enforce
To apply axioms during evaluation.

### include
To require that a term or artifact is present.

### inherit
To take axioms from a parent scope.

### inherited
Taken from a parent scope.

### instantiate
To create a concrete instance from a template.

### note
A short statement recorded for downstream use.

### provide
To supply templates or constraints for downstream use.

### reference
To point from one artifact to another for definitions.

### span
To cover or include terms from another artifact.

### use
To employ an artifact or term.

### yield
To produce an outcome or signal.

### accept
To receive input for evaluation.

### add
To include a term or artifact in a scope.

### added
Past tense of add.

### against
In comparison to a specification or rule.

### applies
Present tense of apply.

### artifact
An output under governance.

### artifacts
Plural of artifact.

### change
A modification to an artifact or state.

### confirm
To validate that a statement holds.

### constraints
Plural of constraint.

### consumes
Present tense of consume.

### consumption
Downstream use of a SPEC or CANON.

### contains
Present tense of contain.

### contradicting
Present tense of contradict.

### declarations
Plural of declaration.

### declaration
A statement of inheritance or scope linkage.

### defines
Present tense of define.

### definitions
Plural of definition.

### derived
Past tense of derive.

### describes
Present tense of describe.

### describing
Present tense of describe.

### downstream
A scope that declares inheritance from another scope.

### evaluate
To compare a structure to a specification.

### evaluates
Present tense of evaluate.

### every
Without exception.

### finality
The property that inherited axioms cannot be overridden.

### here
In this scope.

### hosts
Present tense of host.

### includes
Present tense of include.

### informs
Present tense of inform.

### itself
The same artifact referring to itself.

### local
Belonging to the /machine scope.

### md
The file extension for Markdown.

### notes
Plural of note.

### outcomes
Plural of outcome.

### part
A component within a scope or artifact.

### presence
The state of being present.

### produce
To generate an outcome or signal.

### produces
Present tense of produce.

### purpose
The intent for a scope.

### references
Present tense of reference.

### requirements
Plural of requirement.

### requirement
A statement that must be satisfied.

### results
Plural of result.

### result
The outcome of evaluation.

### rewriting
Changing history rather than preserving it.

### scopes
Plural of scope.

### through
By way of an action or process.

### trace
A list that shows how axioms are derived.

### used
Past tense of use.

### validate
To perform validation against CANON or SPEC.

### when
At the time or condition specified.

End of VOCAB.
