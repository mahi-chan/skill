# Review checklist

The lens for step C (self code-review), and a description of what "good" looks like when you're
writing code from scratch. Don't grind through this as a literal checklist on every line —
carry it in your head and let it flag what's off. Each dimension pairs a **smell** (what makes
a reviewer pause) with the **fix** (what earns approval).

## Contents

- [Correctness & edge cases](#correctness--edge-cases)
- [Error handling](#error-handling)
- [Naming & readability](#naming--readability)
- [Function size & single responsibility](#function-size--single-responsibility)
- [Duplication & reuse](#duplication--reuse)
- [Interface & API design](#interface--api-design)
- [Consistency with the codebase](#consistency-with-the-codebase)
- [Tests](#tests)
- [Security](#security)
- [Performance](#performance)
- [Dependencies & hygiene](#dependencies--hygiene)
- [Comments & docs](#comments--docs)

---

## Correctness & edge cases

The happy path is the easy 80%; reviewers live in the other 20%.

- **Smell:** logic that only accounts for well-formed, non-empty, in-range input. Off-by-one in
  a loop or slice. A `None`/`null` that can reach a dereference. A dictionary/map access that
  assumes the key is present. Integer division or overflow. A resource (file, connection, lock)
  opened on the happy path but leaked on the error path.
- **Fix:** walk each new branch with a hostile input in mind — empty, zero, negative, one
  element, the maximum, a duplicate, out of order, absent. Handle or explicitly reject each.
  Close resources deterministically (context managers / `defer` / `try-with-resources` /
  `finally`).

## Error handling

- **Smell:** errors swallowed (`except: pass`, `catch {}`), or caught only to be re-thrown with
  the original context stripped. Failures that surface to the user as a raw stack trace or a
  generic "something went wrong." Error paths that leave state half-mutated.
- **Fix:** handle errors where you have the context to do something meaningful; otherwise let
  them propagate with that context attached. Fail loudly in development, gracefully in
  production. Validate inputs at trust boundaries, not deep in the call stack.

## Naming & readability

- **Smell:** `data`, `tmp`, `res`, `handle2`, `doStuff`, a boolean named `flag`. A function
  whose body you must read to learn what it returns. Deep nesting (arrow code). A clever
  one-liner that takes a minute to decode.
- **Fix:** names that state intent and units (`retry_count`, `timeout_seconds`,
  `is_eligible`). Prefer early returns to reduce nesting. Reach for clarity over cleverness —
  the reader's time is the scarce resource.

## Function size & single responsibility

- **Smell:** a function that fetches, transforms, validates, and writes. A 150-line method you
  scroll to read. A flag parameter that switches the function into two different behaviors.
- **Fix:** one function, one job, named for that job. Extract cohesive chunks into helpers with
  intention-revealing names. If describing what a function does needs an "and," it's probably
  two functions.

## Duplication & reuse

- **Smell:** a block copy-pasted with small tweaks. A helper reimplemented because the existing
  one wasn't found. Reinventing something the standard library or an existing project utility
  already does.
- **Fix:** **search the codebase before writing a new helper** — reuse beats reinvention and is
  the single most common thing that makes a change feel native. Factor genuine duplication into
  one well-named place. (But don't over-DRY: two things that look alike today yet change for
  different reasons are better left separate.)

## Interface & API design

- **Smell:** functions with many positional parameters (especially several booleans). Leaking
  internal representations (returning a mutable internal list, exposing a DB row shape to
  callers). Inconsistent return types (sometimes a value, sometimes `None`, sometimes raises).
- **Fix:** small, honest signatures; group related params into a struct/object/dataclass when
  they travel together. Keep public surfaces minimal and stable. Return one predictable shape.

## Consistency with the codebase

- **Smell:** a change that's technically fine but stylistically foreign — different import
  ordering, different error idiom, camelCase in a snake_case module, a test in a place tests
  don't live here.
- **Fix:** match the files around it. The reviewer who owns this code reads foreign style as
  friction. Consistency you can see beats any rule in the abstract.

## Tests

- **Smell:** new logic with no test. Tests that assert the code does what it does (restating
  the implementation) rather than what it should. A test weakened or `skip`ped to make the
  suite pass. Tests coupled to incidental details so they break on any refactor.
- **Fix:** test behavior and contracts, including the edges (empty, boundary, error, and — for
  concurrent code — the racy path). Make each test's intent obvious from its name. Match the
  project's existing framework and layout. Never trade a real assertion for a green bar.

## Security

The findings that block merges outright.

- **Smell:** string-built SQL/shell/HTML from user input (injection). Hardcoded secrets, keys,
  or credentials. Input from outside a trust boundary used without validation. Unsafe
  deserialization (`pickle`, `eval`, YAML `load`). Missing authentication/authorization checks
  on a sensitive path. Secrets or PII written to logs. Weak or home-rolled crypto.
- **Fix:** parameterized queries and safe APIs; secrets from config/env, never in source;
  validate and sanitize at the boundary; least privilege on every access; keep secrets and PII
  out of logs; use vetted crypto libraries, never your own.

## Performance

Fix the problems that actually bite; ignore the ones that don't.

- **Smell:** a query inside a loop (N+1). Repeated work that could be hoisted or memoized. An
  O(n²) scan over input that can be large. Loading an unbounded dataset fully into memory.
  Blocking I/O on a hot path.
- **Fix:** batch queries, hoist invariants, pick the right data structure, stream large data.
  But don't micro-optimize cold paths or sacrifice readability for speed nobody will notice —
  premature optimization is its own review smell.

## Dependencies & hygiene

- **Smell:** a whole library pulled in for a one-liner. A new dependency that duplicates one
  already present. Debug prints, commented-out code, stray `TODO`/`FIXME` left in the diff.
  Unused imports or variables.
- **Fix:** justify new dependencies; prefer what's already in the tree or the standard library.
  Strip debug scaffolding and dead code before it ships. Resolve or ticket the `TODO`s you're
  leaving.

## Comments & docs

- **Smell:** comments that narrate the obvious (`i += 1  # increment i`). Stale comments that
  now contradict the code. A genuinely non-obvious decision left unexplained.
- **Fix:** delete redundant comments — clear code carries itself. Reserve comments for the
  *why*: the constraint, the edge case, the reason the non-obvious approach was chosen. Add or
  update docstrings on public functions where the project expects them.
