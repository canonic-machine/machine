# CANON Template

Use this blueprint for any CANON scope. Replace placeholders with statements specific to the scope you are governing. For the root CANON, set `<NAME>` to the repository name and keep `inherits: /`. Inherited axioms are final. Machine scopes extend the base axioms with correction and ordering.

```
{{NAME}} ({{scope path}})

inherits: {{parent scope path}}

axioms:

1. triad:
   {{triad requirement}}

2. inheritance:
   {{parent linkage statement}}
   inherited axioms are final and cannot be overridden

3. coherence:
   {{coherence definition}}

4. compliance:
   {{compliance definition}}

5. governance:
   {{governance definition}}

6. invalidity:
   {{invalidity definition}}

7. introspection:
   {{vocab defines canon and itself}}

8. correction: (machine-only)
   {{history-preserving remedy}}

9. ordering: (machine-only)
   {{required ordering enforcement}}
```
