# Stack tooling

How to detect a stack and the commands to format, lint, and test it. **Always prefer what the
project already configures** — a script in `package.json`, a `Makefile` target, a `tox`/`nox`
env, a CI workflow step — over the generic command here. These defaults are the fallback for
when nothing is configured, and the standard choice when you're starting a project from
scratch.

Order of preference when deciding what to run:

1. An explicit project script or task (`package.json` `scripts`, `Makefile`, `justfile`,
   `tox.ini`, `noxfile.py`, `pyproject.toml` `[tool.*]`).
2. The tool the repo has configured (a config file for it exists — see "detect" below).
3. The language default listed here.

If a formatter/linter/test runner truly isn't present and you're hardening existing code, say
so in the report rather than importing a new tool into someone's project unannounced. When
starting fresh, wire up the standard tool early.

---

## Python

- **Detect:** `pyproject.toml`, `setup.cfg`, `setup.py`, `requirements*.txt`, `tox.ini`,
  `ruff.toml`, `.flake8`. Test dirs `tests/`, files `test_*.py` / `*_test.py`.
- **Format:** `ruff format .` (or `black .`).
- **Lint:** `ruff check .` (or `flake8` / `pylint`). Type-check with `mypy` or `pyright` if the
  project uses it (config present).
- **Test:** `pytest` (or `python -m pytest`); `python -m unittest` if that's the setup.
- **From scratch default:** `ruff` (format + lint) + `pytest`, layout `src/<pkg>/` and
  `tests/`.

## JavaScript / TypeScript

- **Detect:** `package.json` (read its `scripts` first), `tsconfig.json`, `.eslintrc*` /
  `eslint.config.*`, `.prettierrc*`, `biome.json`. Lockfile picks the runner: `package-lock.json`
  → npm, `yarn.lock` → yarn, `pnpm-lock.yaml` → pnpm, `bun.lockb` → bun.
- **Format:** `prettier --write .` (or `biome format --write .`).
- **Lint:** `eslint .` (or `biome check .`); prefer the `lint` script if defined. Typecheck with
  `tsc --noEmit` on TS projects.
- **Test:** the `test` script; underlying runner is usually `vitest run`, `jest`, or `node
  --test`. Playwright/Cypress for e2e if present.
- **From scratch default:** TypeScript + Prettier + ESLint + Vitest.

## Go

- **Detect:** `go.mod`, `go.sum`, `*_test.go`.
- **Format:** `gofmt -w .` (or `goimports -w .`).
- **Lint:** `go vet ./...`; `golangci-lint run` if configured.
- **Test:** `go test ./...` (add `-race` for concurrent code).
- **From scratch default:** standard `go` toolchain; add `golangci-lint`.

## Rust

- **Detect:** `Cargo.toml`, `Cargo.lock`.
- **Format:** `cargo fmt`.
- **Lint:** `cargo clippy --all-targets -- -D warnings`.
- **Test:** `cargo test`.

## Java / Kotlin (JVM)

- **Detect:** `pom.xml` (Maven), `build.gradle` / `build.gradle.kts` (Gradle).
- **Format/Lint:** Spotless, Checkstyle, or ktlint if the build configures them (run via the
  build tool). Maven `mvn verify`; Gradle `./gradlew check`.
- **Test:** `mvn test` or `./gradlew test` (JUnit).

## Ruby

- **Detect:** `Gemfile`, `.rubocop.yml`, `spec/` or `test/`.
- **Format/Lint:** `rubocop -A` (autofix) then `rubocop`.
- **Test:** `rspec` or `rake test` (Minitest).

## C# / .NET

- **Detect:** `*.csproj`, `*.sln`, `.editorconfig`.
- **Format:** `dotnet format`.
- **Test:** `dotnet test`.

## PHP

- **Detect:** `composer.json`, `phpunit.xml`, `.php-cs-fixer.php`.
- **Format:** `php-cs-fixer fix` or `phpcbf`.
- **Lint:** `phpstan analyse` or `psalm` if configured.
- **Test:** `phpunit` (or `vendor/bin/phpunit`).

---

## Shared notes

- **Run against the changed files** where the tool supports it, so the pass stays fast and the
  diff stays focused — but a repo-wide format/lint/test is fine when that's how the project's
  scripts are wired.
- **Re-run after fixing.** Format and lint can surface new issues after you edit; tests can
  regress. Loop until a clean run with no new changes.
- **Respect config, don't fight it.** If the project sets a line length, quote style, or lint
  rule you'd personally choose differently, follow the project. Consistency is the point.
- **Monorepos:** detect per-package — the stack and tooling can differ between
  `packages/*` / `services/*`. Scope to the package your change touches.
