---
name: ship-ready-code
description: >-
  Turns freshly-written code into reviewer-ready, production-grade code. Use this
  whenever a coding task is wrapping up or the user asks to clean up, review, harden,
  finalize, polish, or "get this ready for review / for production," or says they want
  code that will pass review or get approved. Auto-detects the repo's stack and
  conventions, then runs a full format+lint → test → self code-review → security+performance
  pass, fixing issues in place and returning a Ship-Ready Report. Also use it when starting a
  new project or component from scratch and the user wants it built to a professional standard
  from the first line. Reach for it proactively at the end of any multi-file coding change,
  even if the user doesn't name it explicitly.
---

# Ship-Ready Code

Fresh code is rarely reviewer-ready. It compiles and mostly works, but it carries the
residue of getting-it-working: inconsistent style, thin error handling, untested edge cases,
a helper that duplicates one three files over, a name that made sense an hour ago. A good
reviewer catches these and sends it back. This skill does that reviewer's pass *before* the
code leaves your hands, and fixes what it finds, so what you hand over gets approved instead
of bounced.

The goal is not to satisfy a checklist. It's to make the change look like it was written
carefully the first time, in the style of the codebase it lives in.

## Two modes

**While coding** — write it well the first time so there's less to fix later. Two situations:

- *Extending an existing codebase:* hold to the conventions the project already uses and to
  ordinary engineering discipline — small functions that do one thing, honest names, errors
  handled where they happen, no copy-paste when a shared helper exists.
- *Starting from scratch (no code yet):* there's no house style to match, so set a good one
  from the first line. Lay out a sensible project structure, pick the stack's standard tooling
  (formatter, linter, test runner) and wire it up early, write tests alongside the code rather
  than bolting them on at the end, keep modules cohesive and dependencies pointing one way, and
  handle errors and inputs honestly instead of leaving `TODO`s. `references/stack-tooling.md`
  names the standard tools per stack, and `references/review-checklist.md` describes what
  "good" looks like — use them as you write, not only when reviewing.

Either way you don't need a ceremony for this; just don't accumulate debt you'll have to pay
down later.

**End-of-session hardening pass** — the main event, described below. Run it when a unit of
work is done: a feature finished, a bug fixed, a refactor settled, or a from-scratch component
first working. This is what the user is asking for when they say "get this ready for review."
Greenfield code needs it just as much — arguably more, since nothing was there to keep it
honest.

## The core principle: detect, don't assume

"Best practice" in the abstract loses to *the practice of this repo*. A change that's
technically cleaner but stylistically foreign still reads as wrong to the reviewer who owns
the code. So before improving anything, learn how this codebase does things, and match it.
Impose generic preferences only where the repo has expressed none.

## Step 0 — Scope and conventions

Do this first; it aims the whole pass.

**Scope to what changed.** Review the code from *this* session, not the entire repository.
Find it with `git status` and `git diff` (and `git diff --staged`); if the work isn't in git
yet, use the set of files you just created or edited. Reviewing untouched code wastes effort
and invites unrelated churn that itself gets a change bounced.

**Detect the stack and its tools.** Look for the config that reveals how this project builds,
formats, lints, and tests — e.g. `pyproject.toml` / `setup.cfg` / `ruff.toml`, `package.json`
/ `.eslintrc*` / `.prettierrc*` / `biome.json`, `go.mod`, `Cargo.toml`, `pom.xml` /
`build.gradle`, plus `.editorconfig`, `Makefile`, and CI workflow files. Read `CLAUDE.md` /
`AGENTS.md` and any `CONTRIBUTING` doc — teams often write their rules there. When a tool or
convention isn't configured, fall back to the language's community default.
`references/stack-tooling.md` maps common stacks to their detect signals and commands; read
the section for the stack you're in.

**Read a couple of neighbors.** Open one or two existing files near your change and match what
you see: naming, error style, import ordering, test layout, how public APIs are shaped.
Consistency with these beats any rule in this skill. If you're starting a project from scratch
and there are no neighbors, the reverse applies: the conventions you set here become the ones
the rest of the code will follow, so choose the stack's standard idioms deliberately.

## The pass

Run these in order. Each fix can surface work for another step, so after making changes,
**re-run the earlier automated checks** (format, lint, tests) to confirm you didn't regress —
loop until everything is green and settled. Work through the changed files, not the whole
tree.

### A. Format + lint

Run the project's formatter and linter (or the language defaults). Apply autofixes, then fix
the rest by hand. The point isn't cosmetic — a clean lint pass is table stakes for review;
warnings buried in a diff read as carelessness. Do **not** silence a linter with an
inline-ignore just to make it quiet; either fix the underlying issue or, if a suppression is
genuinely warranted, add it with a one-line reason so the reviewer sees the judgment, not a
dodge.

### B. Tests + fill the gaps

Run the existing suite and get it green. When a test fails, assume the *code* is wrong until
you've proven otherwise — fixing the test to match a bug just hides the bug. Never weaken,
skip, or delete a test to make the bar go green; that's the one move guaranteed to erode a
reviewer's trust.

Then add the tests the change is missing. Cover the new behavior and — more importantly — its
edges: the empty input, the boundary value, the error path, the concurrent case if it's
concurrent code. Match the project's existing test framework and structure so the new tests
look native. If the project has no test setup at all, add a minimal, idiomatic one rather than
inventing something elaborate, and note that you did.

### C. Self code-review

Now read the diff the way a careful reviewer would, using `references/review-checklist.md` as
your lens. Fix what you find, in place. The high-value passes:

- **Correctness & edge cases** — off-by-ones, null/None, empty collections, unhandled error
  paths, resource cleanup, assumptions that only hold on the happy path.
- **Clarity** — names that say what they mean; functions short enough to hold in your head;
  early returns over nesting; comments only where the code can't explain itself.
- **Structure & altitude** — the change sits at the right layer, duplicates nothing that
  already exists (search before adding a helper), and doesn't leak abstractions. Reuse the
  codebase's existing utilities instead of re-implementing them.
- **Consistency** — it matches the neighbors you read in Step 0.

### D. Security + performance

Scan the changed code for the failure modes that get flagged in real reviews:

- **Security** — injection (SQL/shell/HTML), hardcoded secrets or credentials, unvalidated
  input crossing a trust boundary, unsafe deserialization, missing authz checks, secrets or
  PII in logs. Fix these; they block merges.
- **Performance** — the obvious ones that matter: N+1 queries, unnecessary work inside hot
  loops, needless O(n²) over large inputs, unbounded memory growth. Don't micro-optimize cold
  paths or trade readability for speed that doesn't matter — that's its own review smell.

## Fix policy: fix in place, but surface the judgment calls

Default to fixing what you find rather than handing back a to-do list — "reviewer-ready" means
the work is done, not diagnosed.

But not all fixes are equal, and honesty about that is what keeps a reviewer trusting the
change. A formatting fix or a clearer name needs no announcement. A fix that **changes
behavior**, **alters a public interface**, or **reshapes the architecture** does — apply it
when you're confident it's right, but call it out prominently in the report so the reviewer
(and the user) can see and weigh it, not discover it later. When a genuine judgment call is
too close to make on your own — two defensible designs, or a change that ripples wider than
the session's scope — make the safe choice, implement it, and flag the alternative rather than
stalling. The report is where these live so nothing significant is buried in a large diff.

## Output: the Ship-Ready Report

End every hardening pass with this report. It's the artifact that tells the user — and stands
in for you to the next reviewer — exactly what was checked, what changed, and what still needs
a human's eye. Keep it tight; link findings to files.

```
## Ship-Ready Report

**Scope:** <files / roughly how many lines reviewed>
**Status:** ✅ Reviewer-ready  |  ⚠️ Needs your call on <N> item(s)

### Checks
- Format + lint: <tool used — clean / N fixed>
- Tests: <N passed; M added; coverage of the new code in a phrase>
- Self-review: <the substantive fixes, not the trivia>
- Security + performance: <what was scanned; findings or "no issues found">

### Fixed in place
- <notable changes, grouped; skip pure formatting noise>

### Needs your attention
- <behavior/interface/architecture changes you made and want seen, and any
   judgment calls — with the file and the reasoning. Omit this section if there are none.>

### Verification
- <exact commands run and their final result, e.g. `ruff check .` → clean,
   `pytest` → 34 passed>
```

If a step genuinely doesn't apply — no tests possible for a pure-config change, say — write
one line saying so rather than forcing it. The report should read as true, not complete for
its own sake.

## Bundled references

- `references/review-checklist.md` — the review dimensions in depth, each with a good-vs-smell
  contrast. Use it as the lens for step C.
- `references/stack-tooling.md` — per-stack detection signals and the format/lint/test commands
  to run, plus what to default to when nothing is configured.
