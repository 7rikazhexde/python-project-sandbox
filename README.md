# python-project-sandbox

An experimental project to test out various tools.

[![Pytest_Coverages_Summary](https://img.shields.io/badge/Pytest_Coverages_Summary-gray?logo=python&logoColor=white)](https://github.com/7rikazhexde/python-project-sandbox/tree/coverage?tab=readme-ov-file#pytest-coverages-summary) [![Pytest_Reports](https://img.shields.io/badge/Pytest_Reports-gray?logo=python&logoColor=white)](https://github.com/7rikazhexde/python-project-sandbox/tree/ghpages?tab=readme-ov-file#pytest-report)

## Table of Contents

- [python-project-sandbox](#python-project-sandbox)
  - [Table of Contents](#table-of-contents)
  - [Pytest Coverages Summary](#pytest-coverages-summary)
  - [Pytest Reports](#pytest-reports)
  - [Install](#install)
    - [Using uv (Recommended)](#using-uv-recommended)
      - [Production Environment](#production-environment)
      - [Development Environment](#development-environment)
    - [Using pip with pyproject.toml](#using-pip-with-pyprojecttoml)
      - [Production Environment](#production-environment-1)
      - [Development Environment](#development-environment-1)
    - [Using requirements.txt](#using-requirementstxt)
      - [Production Environment](#production-environment-2)
      - [Development Environment](#development-environment-2)
  - [Development Tools](#development-tools)
    - [just (Task Runner)](#just-task-runner)
    - [Available Commands](#available-commands)
  - [pre-commit](#pre-commit)
    - [Overview](#overview)
    - [Usage](#usage)
  - [Development Environment Setup](#development-environment-setup)
  - [Testing](#testing)
  - [Code Quality](#code-quality)
  - [CI/CD](#cicd)

## [Pytest Coverages Summary](https://github.com/7rikazhexde/python-project-sandbox/tree/coverage?tab=readme-ov-file#pytest-coverages-summary)

This repository generates test coverage results using [Pytest Coverage Comment](https://github.com/marketplace/actions/pytest-coverage-comment) and outputs them to the [coverage branch](https://github.com/7rikazhexde/python-project-sandbox/tree/coverage).

## [Pytest Reports](https://github.com/7rikazhexde/python-project-sandbox/tree/ghpages?tab=readme-ov-file#pytest-report)

This repository deploys [pytest-html](https://github.com/7rikazhexde/python-project-sandbox/tree/ghpages?tab=readme-ov-file#pytest-html) and [pytest-cov](https://github.com/7rikazhexde/python-project-sandbox/tree/ghpages?tab=readme-ov-file#pytest-cov) reports to GitHub Pages based on the [execution results](https://github.com/7rikazhexde/python-project-sandbox/tree/ghpages/testmon-data) from [pytest-testmon](https://pypi.org/project/pytest-testmon/).

## Install

### Using uv (Recommended)

This project uses [uv](https://docs.astral.sh/uv/) for fast Python package management.

#### Production Environment

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

#### Development Environment

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies including development tools
uv sync --extra dev
```

### Using pip with pyproject.toml

#### Production Environment

```bash
pip install .
```

#### Development Environment

```bash
pip install ".[dev]"
```

### Using requirements.txt

#### Production Environment

```bash
pip install -r requirements.txt
```

#### Development Environment

```bash
pip install -r requirements.txt && pip install -r requirements-dev.txt
```

## Development Tools

### just (Task Runner)

This project uses [just](https://github.com/casey/just) as a task runner for common development tasks.

Install just:

```bash
# On macOS
brew install just

# On Linux
curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to ~/.local/bin

# On Windows
choco install just
```

### Available Commands

```bash
# List all available commands
just --list

# Common development commands
just install          # Install dependencies
just testcov          # Run tests with coverage
just testhtml         # Generate HTML test report
just lint             # Run code linting
just format           # Format code
just type-check       # Run type checking
just check            # Run all quality checks
just clean            # Clean up generated files

# Comprehensive testing
just test-ci-full     # Run comprehensive CI tests
just report-all       # Generate all types of reports
just health-check     # Run complete project health check
```

## pre-commit

This project uses [pre-commit](https://github.com/pre-commit/pre-commit) for automated code quality checks.

### Overview

1. **Static Analysis Tools**

   - [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks): Syntax check of each file
   - [markdownlint-cli](https://github.com/igorshubovych/markdownlint-cli): Syntax checking of markdown files
   - [ruff](https://pypi.org/project/ruff/): Code linting and formatting for Python
   - [mypy](https://pypi.org/project/mypy/): Type checking with type annotations for Python

2. **Automated Version Management**

> [!NOTE]
> Version updates are handled by the [UPDATE workflow (Version Update and Release)](https://github.com/7rikazhexde/python-project-sandbox/blob/main/.github/workflows/update-version-and-release.yml).

### Usage

> [!NOTE]
> If you are creating a pre-commit script with reference to this project, please ensure that the `.pre-commit-config.yaml` and `pyproject.toml` are set up correctly.
>
> Pre-commit is applied to staged files. Note that unstaged files will be skipped.
>
> First, run `uv run pre-commit run --all-files` to verify everything works correctly.

**Set up pre-commit:**

```bash
# Install dependencies
uv sync --extra dev

# Install pre-commit hooks
uv run pre-commit install
```

**Development workflow:**

```bash
# Add changed files
git add -A

# Commit (pre-commit hooks will run automatically)
git commit -m "feat(search): add fuzzy search to search bar

This commit adds fuzzy search functionality to the search bar component.
Fuzzy search allows users to find search results even with spelling mistakes.

Closes #1234"
```

**Test pre-commit locally:**

```bash
uv run pre-commit run --all-files
```

**Alternative using just:**

```bash
just pre-commit
```

## Development Environment Setup

**Quick setup:**

```bash
# Install dependencies and set up pre-commit
just setup
```

**Manual setup:**

```bash
# Install dependencies
uv sync --extra dev

# Install pre-commit hooks
uv run pre-commit install

# Verify setup
just health-check
```

## Testing

**Run tests with coverage:**

```bash
just testcov
```

**Generate comprehensive reports:**

```bash
just report-all
```

**Run tests for specific changes:**

```bash
just testmon
```

## Code Quality

**Run all quality checks:**

```bash
just check
```

**Individual tools:**

```bash
just lint          # Linting with ruff
just format        # Code formatting
just type-check    # Type checking with mypy
just security-check # Security analysis
```

## CI/CD

This project uses GitHub Actions for continuous integration and deployment:

- **PR Check**: Runs tests across multiple OS and Python versions
- **Coverage Reports**: Generates and deploys coverage reports to GitHub Pages
- **HTML Reports**: Generates and deploys test reports to GitHub Pages
- **Automated Releases**: Handles version updates and releases

View workflows in [.github/workflows/](.github/workflows/).
