# Language standards & tooling

The canonical, widely-accepted standard for each language — its community style, the standard
format/lint/test tooling to run, and what a publisher expects for packaging. These standards
*are* "the widespread practice any publisher would accept"; apply them regardless of the
codebase's local habits.

If the project already configures a tool, run that (it encodes the project's intended standard);
otherwise apply the canonical default below. If the project's configured standard is *stricter*
than the default, keep the stricter one — never regress. Detect languages from source
extensions and manifest files, and validate each present language against its section.

---

## Python
- **Style:** PEP 8, enforced by `ruff`/`black`; type hints per PEP 484 on public APIs; docstrings
  (PEP 257) on public modules/functions.
- **Format/lint:** `ruff format .` and `ruff check .` (or `black` + `flake8`); `mypy`/`pyright` if
  types are used seriously.
- **Test:** `pytest` (or the configured runner).
- **Packaging:** PEP 621 `pyproject.toml` with name, version, description, authors, license,
  `requires-python`, dependencies, and entry points; `src/` layout preferred; build with `python
  -m build` and confirm a clean install (`pip install .`) in a fresh venv. Version follows semver.

## JavaScript / TypeScript
- **Style:** the standard ESLint recommended rules + Prettier formatting (or the project's
  StandardJS/Airbnb config); `tsc --noEmit` clean for TS; no `var`, `===` over `==`.
- **Format/lint:** `prettier --check .` and `eslint .` (or `biome check .`).
- **Test:** the `test` script (`vitest`, `jest`, or `node --test`).
- **Packaging:** `package.json` with name, version (semver), description, `main`/`exports`, `type`,
  `license`, `files`, and correctly split `dependencies` vs `devDependencies`; `.npmignore` or
  `files` so only the built artifact ships; `npm pack` and confirm the tarball contents; builds
  from a clean `npm ci`.

## Go
- **Style:** `gofmt`-clean, Effective Go idioms, exported identifiers documented with `//`
  comments, errors wrapped with context (`fmt.Errorf("...: %w", err)`).
- **Format/lint:** `gofmt -l .` (must be empty) and `go vet ./...`; `golangci-lint run` if present.
- **Test:** `go test ./...` (`-race` for concurrent code).
- **Packaging:** a correct `go.mod` (module path matches the repo), tidy deps (`go mod tidy`
  leaves no diff), and `go build ./...` clean. Tag releases with semver (`vX.Y.Z`).

## Rust
- **Style:** `rustfmt`-clean, Rust API Guidelines, no `clippy` warnings, documented public items.
- **Format/lint:** `cargo fmt --check` and `cargo clippy --all-targets -- -D warnings`.
- **Test:** `cargo test`.
- **Packaging:** `Cargo.toml` with name, version (semver), description, license, repository, and
  categories/keywords for crates.io; `cargo publish --dry-run` clean; `cargo build --release` ok.

## Java / Kotlin (JVM)
- **Style:** Google Java Style or the project's Checkstyle/Spotless/ktlint config; documented
  public API (Javadoc/KDoc).
- **Format/lint:** the build's Spotless/Checkstyle/ktlint task; `mvn verify` or `./gradlew check`.
- **Test:** `mvn test` or `./gradlew test` (JUnit).
- **Packaging:** complete POM/Gradle metadata (groupId, artifactId, version, license, developers)
  for Maven Central; sources+javadoc jars; a clean build from scratch.

## Ruby
- **Style:** the Ruby Style Guide via `rubocop`; documented public API.
- **Format/lint:** `rubocop` (clean).
- **Test:** `rspec` or `rake test`.
- **Packaging:** a complete `.gemspec` (name, version, summary, authors, license, files); `gem
  build` clean and installable.

## C# / .NET
- **Style:** .NET conventions via `.editorconfig`; XML doc comments on public API.
- **Format/lint:** `dotnet format --verify-no-changes`.
- **Test:** `dotnet test`.
- **Packaging:** `.csproj` with PackageId, Version (semver), Authors, Description,
  PackageLicenseExpression; `dotnet pack` clean.

---

## For any language not listed
Apply the same shape: find the ecosystem's **canonical style guide** and its standard formatter,
linter, and test runner; require a clean format/lint/test pass and a from-scratch build/install;
and confirm the manifest carries name, version (semver), license, description, and correctly
declared dependencies. When unsure of the canonical standard, prefer the most widely-cited
community guide over any local convention.
