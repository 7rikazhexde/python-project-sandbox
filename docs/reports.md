# Reports & coverage

This project keeps **report generation independent** (each report is produced by
a different tool across an OS / Python matrix) but uses this documentation site
as the **hub** that links them together. Nothing is coupled at build time — the
docs simply point at the published artifacts.

## What is published, and where

| Report | Tool | Location |
| --- | --- | --- |
| Coverage summary | `pytest-coverage-comment` | [`coverage` branch README](https://github.com/7rikazhexde/python-project-sandbox/tree/coverage?tab=readme-ov-file#pytest-coverages-summary) |
| Coverage HTML | `pytest-cov` | `ghpages` → `pytest-cov-report/<os>/python/<version>/` |
| Test report HTML | `pytest-html` | `ghpages` → `pytest-html-report/<os>/python/<version>/` |

The HTML reports are driven by [pytest-testmon](https://pypi.org/project/pytest-testmon/)
incremental runs and deployed per OS / Python version. The canonical index — kept
up to date with the current matrix — lives in the
[`ghpages` branch README](https://github.com/7rikazhexde/python-project-sandbox/tree/ghpages?tab=readme-ov-file#pytest-report).

### Live links

- **Indexes (recommended entry points):**
    - Coverage summary → <https://github.com/7rikazhexde/python-project-sandbox/tree/coverage?tab=readme-ov-file#pytest-coverages-summary>
    - HTML / cov reports → <https://github.com/7rikazhexde/python-project-sandbox/tree/ghpages?tab=readme-ov-file#pytest-report>
- **Direct URL pattern** (replace `<os>` / `<version>`):
    - Test report: `…/python-project-sandbox/pytest-html-report/<os>/python/<version>/report_page.html`
    - Coverage:    `…/python-project-sandbox/pytest-cov-report/<os>/python/<version>/index.html`
- **Concrete example** (ubuntu-latest / Python 3.11.9):
    - [Test report](https://7rikazhexde.github.io/python-project-sandbox/pytest-html-report/ubuntu-latest/python/3.11.9/report_page.html)
    - [Coverage](https://7rikazhexde.github.io/python-project-sandbox/pytest-cov-report/ubuntu-latest/python/3.11.9/index.html)

!!! note "Why not serve reports from this site?"

    The reports are large, self-contained HTML generated independently for each
    of `ubuntu` / `macos` / `windows` × Python `3.12` / `3.13` (and more), using
    `pytest-testmon` incremental state. Keeping generation separate avoids
    coupling two pipelines and bloating the docs build — this page is the hub,
    the reports stay independent.

## pytest-html styling (custom CSS)

The HTML test report is themed with a custom stylesheet at
[`css/style.css`](https://github.com/7rikazhexde/python-project-sandbox/blob/main/css/style.css).
It is applied with pytest-html's `--css` option, and `--self-contained-html`
inlines the CSS so the published `report_page.html` is a single portable file:

```bash
uv run pytest \
  --html=htmlcov/report_page.html \
  --self-contained-html \
  --css=css/style.css \
  --capture=no \
  project_a tests/
```

Or via the task runner:

```bash
just testhtml          # -> htmlcov/report_page.html (styled)
```

In CI, the same `--css=css/style.css` is passed in
`test_pytest-html-report_deploy_multi_os.yml` before the report is published to
`ghpages`.

!!! tip "Reproduce this setup in your own project"

    1. Add a stylesheet (e.g. `css/style.css`).
    2. Generate the report with `--html=… --self-contained-html --css=css/style.css`.
    3. Publish the per-matrix output to a `ghpages` subdirectory (this project
       uses `pytest-<html|cov>-report/<os>/python/<version>/`), keeping existing
       files so the reports and these docs coexist.
    4. Link everything from a single hub page — like this one.
