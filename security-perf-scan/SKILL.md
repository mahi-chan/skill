---
name: security-perf-scan
description: >-
  Scan changed code for security vulnerabilities and performance problems, and fix them. Use
  whenever the user asks whether code is secure or efficient, to check for vulnerabilities, do a
  security review, look for injection / secrets / auth issues, or find performance problems like
  slow loops or N+1 queries. Scans the changed code against a security and performance checklist
  and fixes the real issues, without micro-optimizing. Reach for it before shipping code that
  handles input, data, requests, or anything crossing a trust boundary.
---

# Security & performance scan

Catch the two classes of problem that block merges outright or bite in production. **Scope to
the changed code** (`git diff`), and fix what you find in place.

## Security

The findings a reviewer will not let through:

- **Injection** — SQL / shell / HTML built by string concatenation from input → parameterized
  queries and safe APIs.
- **Secrets** — hardcoded keys, tokens, credentials → move to config/env, never in source.
- **Unvalidated input** crossing a trust boundary → validate and sanitize at the boundary.
- **Unsafe deserialization** — `pickle`, `eval`, YAML `load` on untrusted data → safe loaders.
- **Missing authz** on a sensitive path → enforce least privilege on every access.
- **Secrets / PII in logs** → strip them. **Weak or home-rolled crypto** → use vetted libraries.

## Performance

Fix the problems that actually matter; ignore the ones that don't:

- **N+1** — a query inside a loop → batch it.
- **Repeated work in a hot loop** → hoist invariants, memoize.
- **O(n²) over large input** → pick the right data structure.
- **Unbounded memory** — loading a whole large dataset → stream it.
- **Blocking I/O on a hot path** → make it async or move it off the path.

Don't micro-optimize cold paths or trade readability for speed nobody will notice — that's its
own review smell. Weigh perf fixes against clarity; only reshape code where the cost is real.

**Close with:** what you scanned and the findings — each fix in a line, or `no issues found`.
Flag anything you changed that alters behavior so the reviewer sees it.
