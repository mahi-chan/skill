---
name: test-hardening
description: >-
  Run the test suite and fill in the missing tests for changed code. Use whenever the user asks
  to run the tests, add or write tests, improve or check coverage, make sure something is
  tested, fix failing tests, or cover edge cases. Detects the project's test framework, gets the
  suite green — fixing the code, never weakening the tests — and adds tests for new behavior and
  its edges. Reach for it after writing or changing logic that isn't covered yet.
---

# Test hardening

Get the changed code properly tested: the existing suite green, and the new behavior covered
where it matters — the edges, not just the happy path.

**Scope to what changed** — the logic added or modified this session.

**Run the existing suite first.** Detect the framework and run it:

- **Python:** `pytest` (or `python -m pytest` / `unittest`)
- **JS/TS:** the `test` script (usually `vitest run`, `jest`, or `node --test`)
- **Go:** `go test ./...` (`-race` for concurrent code)  ·  **Rust:** `cargo test`
- **Ruby:** `rspec` / `rake test`  ·  **Java/Kotlin:** `mvn test` / `./gradlew test`  ·  **C#:** `dotnet test`

**When a test fails, assume the code is wrong** until you've proven otherwise — fixing a test to
match a bug just hides it. Never weaken, `skip`, or delete a test to make the bar go green; that
is the fastest way to lose a reviewer's trust.

**Add the tests the change is missing.** Cover the new behavior and — more importantly — its
edges: empty input, the boundary value, the error path, the concurrent case if it's concurrent
code. Test behavior and contracts, not the implementation line-by-line, so the tests survive a
refactor. Match the project's existing framework and layout so the new tests look native. If the
project has no test setup at all, add a minimal idiomatic one rather than inventing something
elaborate, and say you did.

**Close with one line:** e.g. `pytest → 18 passed (6 added: empty file, bad amount, n>len, ties); new code covered`.
