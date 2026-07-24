---
name: format-lint
description: >-
  Format and lint changed code to match the project's own style. Use whenever the user asks to
  format, run the formatter, lint, fix lint errors or warnings, tidy up style, clean up
  formatting, or make code conform to the project's conventions. Auto-detects the project's
  formatter and linter (or the language default), runs them over the changed files, and fixes
  the violations. Reach for it once code is written and just needs to pass style/lint checks.
---

# Format & lint

Make the changed code pass style and lint cleanly, in the project's own style. Warnings left in
a diff read as carelessness to a reviewer; a clean pass is table stakes.

**Scope to what changed** — the files from this session (`git diff --name-only`, or the files
you just touched), not the whole tree, unless the project's own script formats everything.

**Use the project's tools, not your preferences.** Detect what the repo configures and run
that; only fall back to a default when nothing is set. If the project sets a line length or
quote style you'd choose differently, follow the project — consistency is the whole point.

- Prefer an existing script/target: `package.json` `scripts`, `Makefile`, `tox`/`nox`, `pre-commit`.
- Else the configured tool (a config file exists), else the language default:
  - **Python:** `ruff format .` + `ruff check --fix .` (or `black` + `flake8`)
  - **JS/TS:** `prettier --write .` + `eslint --fix .` (or `biome check --write .`)
  - **Go:** `gofmt -w .` + `go vet ./...`  ·  **Rust:** `cargo fmt` + `cargo clippy`
  - **Ruby:** `rubocop -A`  ·  **C#:** `dotnet format`  ·  **Java/Kotlin:** the build's Spotless/ktlint target

**Fix, don't silence.** Apply autofixes, then fix the rest by hand. Don't blanket-suppress a
rule with an inline-ignore just to quiet it; if a suppression is genuinely warranted, add it
with a one-line reason so the reviewer sees a judgment, not a dodge. Re-run after hand-fixing,
since edits can surface new issues — loop until clean.

**Close with one line:** the tool used and the result, e.g. `ruff format + check → clean (6 autofixed, 1 fixed by hand)`.
