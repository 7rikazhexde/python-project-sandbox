# python-project-sandbox

A **modern Python project base** for experimenting with tooling — powered by
[uv](https://docs.astral.sh/uv/), [Ruff](https://docs.astral.sh/ruff/),
[mypy](https://mypy-lang.org/) and [pytest](https://docs.pytest.org/), with test
coverage and HTML reports published to dedicated branches via GitHub Actions.

## Highlights

- **Fast tooling** — `uv` for dependency management, `Ruff` for lint/format,
  `mypy` for type checking, `just` as the task runner.
- **Branch-managed reports** — coverage summaries are published to the
  [`coverage`](https://github.com/7rikazhexde/python-project-sandbox/tree/coverage)
  branch and pytest HTML/cov reports to the
  [`ghpages`](https://github.com/7rikazhexde/python-project-sandbox/tree/ghpages)
  branch. See [CI & Coverage](ci.md).
- **Modern tooling, adopted early** — `zizmor` (Actions security), `ty`
  (Astral type checker), `pip-audit`, `typos` and `validate-pyproject` run as a
  preview quality workflow.
- **Multi-OS / multi-Python CI** — every change is tested across
  Ubuntu / macOS / Windows on Python 3.11, 3.12 and 3.13.

## Where to next

- [Getting started](getting-started.md) — install dependencies and run the
  common development tasks.
- [CI & Coverage](ci.md) — how coverage and reports are built and published.

!!! note "Documentation engine"

    This site is built with [Zensical](https://zensical.org), the next-generation
    static site generator from the creators of Material for MkDocs, adopted here
    as an early-access (preview) tool.
