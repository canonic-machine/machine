# CANON Template

Use this blueprint for any CANON scope. Replace placeholders with statements specific to the scope you are governing. This template is generic; the root CANON is simply one instance with `inherits: /`. Include only the axioms that apply to your scope and add additional axioms as needed.

```
{{NAME}} ({{scope path}})

inherits: {{parent scope path}}

axioms:

1. triad:
   {{triad requirement}}

2. inheritance:
   {{parent linkage statement}}
   inherited axioms are final and cannot be overridden

3. introspection:
   VOCAB defines every term used by this CANON, the SPEC, the README, and itself

4. {{axiom name}}:
   {{axiom statement}}

5. {{axiom name}}:
   {{axiom statement}}
```
