# Publication acceptance criteria

The bar for each area, and the common reasons a publisher, registry, or reviewer rejects a
submission. This is the review checklist — hold every file to *this* standard, not the
codebase's existing habits. Mark each area as meets-bar, fixed-to-meet, or blocker.

A **blocker** is something a competent gatekeeper would reject or that would harm users
(crashes, security holes, missing license, broken build). **Polish** is below the ideal but
wouldn't get you rejected — fix it if cheap, note it if not. The verdict is "Ready" only when no
blockers remain.

## Contents
- [Correctness & robustness](#correctness--robustness)
- [Code quality](#code-quality)
- [Tests](#tests)
- [Security](#security)
- [Performance](#performance)
- [Documentation](#documentation)
- [Packaging & metadata](#packaging--metadata)
- [Licensing & hygiene](#licensing--hygiene)

---

## Correctness & robustness
**Standard:** the code does what it documents, and degrades sanely on bad input instead of
crashing or corrupting state.
**Reject when:** happy-path-only logic that throws on empty/boundary/absent input; off-by-ones;
null/None reaching a dereference; leaked files/connections/locks on the error path; silent data
corruption; race conditions in concurrent code.
**Fix:** walk each path with a hostile input (empty, zero, one, max, duplicate, absent) and
handle or explicitly reject it; release resources deterministically (context managers / defer /
try-with-resources).

## Code quality
**Standard:** readable at the language's canonical bar (see `language-standards.md`) — a stranger
can follow it.
**Reject when:** meaningless names (`data`, `tmp`, `doStuff`); functions that do four things;
deep nesting; copy-paste duplication; dead code, debug prints, or commented-out blocks left in;
swallowed errors (`except: pass`, empty `catch`); inconsistent, un-formatted code.
**Fix:** intention-revealing names; one function one job; early returns; reuse existing utilities
instead of duplicating; delete dead/debug code; handle errors where there's context or propagate
with it; run the standard formatter + linter to clean.

## Tests
**Standard:** an automated suite that runs green and covers the shipped behavior, including its
edges.
**Reject when:** no tests for non-trivial logic; a failing or flaky suite; tests that restate the
implementation rather than assert behavior; tests skipped or weakened to force a pass.
**Fix:** get the existing suite green by fixing the *code* (a failing test usually means a real
bug); add tests for new behavior and its edges (empty, boundary, error, concurrency); test
contracts, not line-by-line internals. Never weaken/delete a test to go green.

## Security
**Standard:** no known-dangerous patterns on anything touching input, secrets, or a trust
boundary. These are hard blockers.
**Reject when:** SQL/shell/HTML built by string concat from input (injection); hardcoded secrets,
keys, or credentials; unvalidated boundary input; unsafe deserialization (`pickle`, `eval`, YAML
`load` on untrusted data); missing authn/authz on a sensitive path; secrets or PII in logs;
weak or home-rolled crypto; obviously-vulnerable dependency versions.
**Fix:** parameterized queries and safe APIs; secrets from config/env, never in source; validate
at the boundary; least privilege; vetted crypto libraries; bump vulnerable deps.

## Performance
**Standard:** no pathological behavior on realistic inputs. Not micro-optimization — the goal is
"won't fall over," not "fastest possible."
**Reject when:** N+1 queries; O(n²) (or worse) over inputs that can be large; unbounded memory
growth; blocking I/O on a hot path; repeated expensive work that could be hoisted.
**Fix:** batch queries, pick the right data structure, stream large data, hoist invariants. Leave
cold paths alone; don't trade readability for speed nobody will notice.

## Documentation
**Standard:** someone who's never seen the project can understand, install, and use it.
**Reject when:** no README, or one that doesn't say what the thing is; no install/usage
instructions; undocumented public API; stale docs that contradict the code; examples that don't
run.
**Fix:** a README with a one-line description, install steps, a minimal usage example, and a
pointer to more; docstrings/JSDoc/godoc on the public surface to the language's norm; remove or
correct stale docs.

## Packaging & metadata
**Standard:** the artifact **builds and installs cleanly from scratch**, and its manifest is
correct and complete.
**Reject when:** the build/install fails on a clean checkout; missing or wrong manifest fields
(name, version, entry point, author, license); undeclared dependencies (works only because
they're on your machine); unpinned/reckless version ranges; a version that doesn't follow semver
where the ecosystem expects it; shipping tests/build junk in the published artifact.
**Fix:** complete the manifest; declare every runtime dependency; verify a clean build/install in
a fresh environment; set an appropriate version; configure what's included in the package.

## Licensing & hygiene
**Standard:** clear legal status and a clean tree.
**Reject when:** no LICENSE file; a license incompatible with the project's dependencies;
committed secrets/credentials; missing or inadequate `.gitignore`; stray build artifacts, caches,
`.env` files, editor cruft, or large binaries committed; leftover `TODO`/`FIXME` on the shipped
path.
**Fix:** add a LICENSE (ask the user which if unclear — this is a genuine decision, not something
to guess); remove committed secrets and rotate if they were real; add a proper `.gitignore` and
untrack artifacts; resolve or ticket TODOs on the shipping path.
