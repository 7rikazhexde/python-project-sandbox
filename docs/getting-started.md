# Getting started

## Install

This project uses [uv](https://docs.astral.sh/uv/) for fast Python package
management.

=== "Production"

    ```bash
    # Install uv if not already installed
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Install runtime dependencies
    uv sync
    ```

=== "Development"

    ```bash
    # Install dependencies including development tools
    uv sync --extra dev
    ```

## Task runner (just)

Common tasks are wrapped with [just](https://github.com/casey/just):

```bash
just --list            # List all available commands
just testcov           # Run tests with coverage
just lint              # Lint with Ruff
just format            # Format with Ruff
just type-check        # Type check with mypy
just check             # Lint + type-check + tests
```

### Modern tooling (preview)

Early-adopted quality tools are also available as `just` recipes:

```bash
just type-check-ty     # Type check with ty (Astral, preview)
just spell             # Spell check with typos
just audit-actions     # GitHub Actions security audit (zizmor)
just audit-deps        # Dependency vulnerability scan (pip-audit)
just validate-pyproject # Validate pyproject.toml schema
```

## Pre-commit

```bash
# Install dependencies and the pre-commit hooks
uv sync --extra dev
uv run pre-commit install

# Run all hooks against every file
uv run pre-commit run --all-files
```

## Build these docs locally

The documentation site is built with [Zensical](https://zensical.org):

```bash
uvx zensical serve     # Live preview at http://127.0.0.1:8000
uvx zensical build     # Build static site into ./site
```
