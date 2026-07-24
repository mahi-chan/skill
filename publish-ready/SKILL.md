---
name: publish-ready
description: >-
  Validate a codebase against universal, publication-grade engineering standards — the bar any
  competent publisher, registry, marketplace, or external reviewer expects — and fix it to meet
  that bar before submission. Use whenever the user wants to check whether their code or project
  is ready to publish, submit, release, ship, or hand off; asks for a publisher-grade,
  professional, or industry-standard review; or wants their whole codebase reviewed, tested,
  evaluated, and fixed before submitting it somewhere. This enforces widely-accepted best
  practices — a language's canonical standards plus general software-engineering principles — and
  deliberately does NOT just conform to the codebase's existing local style. It reviews, tests,
  evaluates, and fixes, then delivers a clear go/no-go publish-readiness verdict. Reach for it
  before any external submission or release even if the user doesn't name the skill.
---

# Publish-Ready

This is a pre-submission gate. The user is about to hand this codebase to an external
gatekeeper — a package registry, an app store, a marketplace, a client, a reviewer — and wants
it to clear that gatekeeper's bar the first time. Your job is to **validate the code against
universal, widely-accepted standards, fix it to meet them, and then say plainly whether it's
ready.**

## The bar is external, not local

This is the point that makes the skill useful: **do not infer the standard from the code you're
reviewing.** A submission gate exists precisely because the author's own habits may sit below
what a publisher accepts. So hold every file to the same widely-accepted bar:

- The language's **canonical community standard** — PEP 8 / PEP 621 for Python, Effective Go and
  `gofmt`, the standard ESLint/Prettier conventions for JS/TS, the Rust API guidelines, and so
  on. These *are* the "widespread practice any publisher would accept." See
  `references/language-standards.md`.
- **General software-engineering principles** that hold in any language — correctness, honest
  error handling, tests, security, clear naming, documentation. See `references/standards.md`.

Where the codebase's current style is *below* this bar, raise it. Consistency with the repo's
existing quirks is not a goal here and is not a reason to leave a substandard pattern in place.
(The one nuance: if the project already follows a *stricter* published standard than the
default, keep to the stricter one — never regress quality.)

## Scope

Validate the code being submitted. By default that's the whole project; if the user points you
at a package or subdirectory, scope to that. Focus on the **source that ships** — skip vendored
dependencies, build artifacts, generated files, and anything already git-ignored. On a large
codebase, prioritize the public surface and the modules most likely to be judged, and say what
you covered.

## The pass: review → test → evaluate → fix

Work through the areas below, running the standard tooling and reading the code. Fix issues as
you find them, and re-run the automated checks after fixing so nothing regresses — loop until
they settle. `references/standards.md` has the detailed acceptance criteria for each area (the
standard, and the common reasons a publisher rejects); read it as your checklist.

1. **Correctness & robustness** — the code does what it claims, and holds up on the edges (empty,
   boundary, error, absent input) rather than only the happy path. Resources are released.
2. **Code quality** — measured against the language's canonical standard: clear intention-revealing
   names, functions that do one thing, no dead/debug code, no needless duplication, honest error
   handling. Not the repo's local habits — the published bar.
3. **Tests** — the suite runs and is green; the shipped behavior is covered, including its edges.
   Add tests where they're missing. Never weaken or delete a test to make the bar go green.
4. **Security** — no injection, hardcoded secrets, unvalidated boundary input, unsafe
   deserialization, missing authz, or secrets/PII in logs. These block submissions outright.
5. **Performance** — no needless O(n²) on real inputs, N+1 queries, or unbounded memory on paths
   that matter. Fix the real problems; don't micro-optimize.
6. **Documentation** — a README that says what it is, how to install, and how to use it; public
   APIs documented to the language's norm. Publishers and users read this first.
7. **Packaging & metadata** — the manifest is correct and complete (name, version, entry points,
   declared and reasonably-pinned dependencies), and the project **builds and installs cleanly
   from scratch**. Version follows semver where it applies.
8. **Licensing & hygiene** — a LICENSE is present, no secrets or credentials are committed, a
   sensible `.gitignore` is in place, and no stray artifacts, `TODO`/`FIXME`, or commented-out
   code ships.

Format and lint with the language's standard tools (see `references/language-standards.md`); a
clean lint pass is table stakes and its absence reads as carelessness.

## Fix policy

Fix toward the standard in place — the deliverable is a codebase that's *ready*, not a list of
complaints. But raising code to a published bar can mean real changes: a behavior fix, a
renamed public API, a restructured module. Apply those when you're confident, and **call them
out prominently** so the user sees what moved — never bury a behavior or interface change in a
large diff. Never fake readiness: don't suppress a linter, weaken a test, or paper over a real
security issue to make a category look green.

## Output: the Publish-Readiness Report

End with a clear verdict — this is the "evaluate" the user is asking for, a publisher's go/no-go.

```
## Publish-Readiness Report

**Target:** <what was validated — project / package / dir, languages, rough size>
**Verdict:** ✅ Ready to submit  |  ⛔ Not ready — <N> blocker(s) remain  |  ⚠️ Ready after the fixes below

### Scorecard  (✅ meets bar · 🔧 fixed to meet bar · ⛔ blocker · — n/a)
- Correctness & robustness: <status — one line>
- Code quality (canonical standard): <status>
- Tests: <status — N passed, M added, coverage of shipped code>
- Security: <status>
- Performance: <status>
- Documentation: <status>
- Packaging & metadata (builds/installs clean?): <status>
- Licensing & hygiene: <status>

### Fixed to meet the bar
- <the substantive changes, grouped; skip pure formatting noise>

### Blockers / needs your attention
- <anything still below bar you couldn't safely fix, plus any behavior/interface changes you
   made and want seen — with file and reasoning. Omit if none and the verdict is ✅.>

### Verification
- <exact commands run and their final result — build/install, lint, tests>
```

Be honest in the verdict: if a real blocker remains that you can't resolve (a design flaw, a
missing license the user must choose, a dependency with no clean fix), say **Not ready** and name
it. A gate that always says "ready" is worthless.

## References

- `references/standards.md` — the acceptance criteria per area: the universal standard, and the
  common reasons a publisher rejects. Your review checklist.
- `references/language-standards.md` — per-language canonical style, the standard format/lint/test
  tooling to run, and packaging/metadata expectations.
