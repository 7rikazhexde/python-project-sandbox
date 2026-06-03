# CI & Coverage

This project leans on GitHub Actions for testing and for **publishing reports to
dedicated branches** — a core idea of this template.

## Workflows

| Workflow | Trigger | Purpose |
| --- | --- | --- |
| `PR Check (Except Dependabot)` | PR to `main` | Multi-OS / multi-Python tests, 90% coverage gate, coverage PR comment |
| `Dependabot PR Check` | Dependabot PR | Same checks for dependency-update PRs |
| `Test Multi-OS` | push to `main` | Tests + publishes the coverage summary to the `coverage` branch |
| `Modern Quality (Preview)` | PR / push | `zizmor` / `ty` / `pip-audit` / `typos` / `validate-pyproject` (preview) |
| `Release Please` | push to `main` | Conventional-Commits release automation (opens a Release PR) |
| `Docs (Zensical)` | push / PR | Build this site and deploy to `ghpages/docs/` |

All test workflows install `just` from a **prebuilt binary**
(`taiki-e/install-action`) and use `concurrency` to cancel superseded runs,
keeping CI fast.

## Branch-managed reports

Rather than committing generated artifacts to `main`, reports live on their own
branches:

- **`coverage`** — a generated `README.md` with the per-OS / per-Python coverage
  summary. See the
  [coverage branch](https://github.com/7rikazhexde/python-project-sandbox/tree/coverage?tab=readme-ov-file#pytest-coverages-summary).
- **`ghpages`** — pytest **HTML** and **coverage** reports published to GitHub
  Pages, driven by [pytest-testmon](https://pypi.org/project/pytest-testmon/)
  incremental runs. See the
  [reports](https://github.com/7rikazhexde/python-project-sandbox/tree/ghpages?tab=readme-ov-file#pytest-report).

This documentation site is published to the **`docs/` subdirectory of the
`ghpages` branch**, so it coexists with the pytest reports served from the root.

## Releases

Releases are automated with
[release-please](https://github.com/googleapis/release-please) using
[Conventional Commits](https://www.conventionalcommits.org/). On every push to
`main`, release-please maintains a **Release PR** that updates `CHANGELOG.md` and
the version in `pyproject.toml`. Merging that PR creates the git tag and GitHub
Release — so nothing is released without an explicit human merge.

## Coverage PR comments

Pull requests receive a coverage comment from
[`pytest-coverage-comment`](https://github.com/marketplace/actions/pytest-coverage-comment).
File links are resolved with `coverage-path-prefix: project_a/` so they point at
real source paths, and a `cleanup_pr_comments` job removes stale comments on
re-runs to avoid broken links.
