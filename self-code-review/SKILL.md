---
name: self-code-review
description: >-
  Self-review your own pending code changes and fix what a reviewer would flag, in place. Use
  whenever the user asks to review their code, self-review, look over changes before a PR, check
  whether code is ready for review, or clean up code they just wrote. Reviews the session's diff
  against a checklist — correctness, edge cases, error handling, naming, duplication, consistency
  — fixes issues in place, and surfaces any behavior or interface changes. This is for improving
  your own uncommitted work, not for formally reviewing someone else's pull request.
---

# Self code-review

Read the change the way a careful reviewer would, and fix what they'd send back — before they
see it. The aim is code that looks like it was written carefully the first time, in the style of
the codebase it lives in.

**Scope to the diff** (`git diff`) and **match the neighbors.** Open a file or two near your
change and follow their naming, error style, and structure. A change that's technically cleaner
but stylistically foreign still reads as wrong to the reviewer who owns the code.

Go through the diff against this checklist and **fix issues in place** — each pair is a smell → the fix:

- **Correctness & edge cases** — happy-path-only logic, off-by-ones, null/None, empty
  collections, unhandled error paths, leaked resources → walk each branch with a hostile input
  (empty, zero, boundary, one element, absent) and handle or reject it; close resources deterministically.
- **Error handling** — swallowed errors, raw tracebacks to the user, half-mutated state → handle
  where you have context, else propagate with context; validate at trust boundaries.
- **Naming & clarity** — `data`/`tmp`/`doStuff`, deep nesting, clever one-liners → intention-revealing
  names, early returns, clarity over cleverness.
- **Size & responsibility** — a function that does four things, a flag param that forks behavior →
  one function one job, extract cohesive helpers.
- **Duplication & reuse** — copy-paste, a helper reimplemented because the existing one wasn't
  found → search before adding; reuse the codebase's utilities. (But don't over-DRY things that
  merely look alike.)
- **Consistency** — foreign import order, error idiom, or test placement → match the surrounding code.

**Surface the judgment calls.** Fix in place by default, but anything that **changes behavior**,
**alters a public interface**, or **reshapes architecture** should be called out, not buried in a
large diff — apply it when you're confident, and list it so the reviewer can weigh it.

**Close with:** the substantive fixes (skip the trivia), then a short **Needs your attention**
list of any behavior/interface changes or judgment calls — omit that line if there are none.
