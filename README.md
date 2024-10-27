# python-project-sandbox

An experimental project to test out various tools.

## Tabale of contents

- [python-project-sandbox](#python-project-sandbox)
  - [Tabale of contents](#tabale-of-contents)
  - [Pytest Coverages](#pytest-coverages)
  - [Pytest Reports](#pytest-reports)
  - [pre-commit](#pre-commit)
    - [Overview](#overview)
    - [Usage](#usage)
  - [post-commit](#post-commit)
    - [Overview](#overview-1)
    - [Usage](#usage-1)
    - [pytest-coverage-comment](#pytest-coverage-comment)

## Pytest Coverages

[![Coverage Status](https://img.shields.io/badge/Coverage_Data-check%20here-blue.svg)](https://github.com/7rikazhexde/python-project-sandbox/tree/coverage)

This repository generates test coverage results using [Pytest Coverage Comment](https://github.com/marketplace/actions/pytest-coverage-comment) and outputs them to the [coverage branch](https://github.com/7rikazhexde/python-project-sandbox/tree/coverage).

## Pytest Reports

[![Pytest Status](https://img.shields.io/badge/Pytest_Report-check%20here-blue.svg)](https://github.com/7rikazhexde/python-project-sandbox/tree/coverage)

This repository deploys [pytest-html](https://pypi.org/project/pytest-html/) and [pytest-cov](https://pypi.org/project/pytest-cov/) reports to GitHub Pages based on the [execution results](https://github.com/7rikazhexde/python-project-sandbox/tree/ghpages/testmon-data) from [pytest-testmon](https://pypi.org/project/pytest-testmon/).

## pre-commit

This project is using [pre-commit](https://github.com/pre-commit/pre-commit) via poetry.

### Overview

1. Using Static Analysis Tools

   - [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks): Syntax check of each file.
   - [poetry](https://python-poetry.org/docs/pre-commit-hooks/#usage): Syntax checking and generation of dependency files for Poetry configuration information.
   - [markdownlint-cli](https://github.com/igorshubovych/markdownlint-cli): Syntax checking of markdown files.
   - [ruff](https://pypi.org/project/ruff/): Code lint and format for Python.
   - [mypy](https://pypi.org/project/mypy/): Type checking with type annotations for Python.

2. Run update pyproject.toml version up script

> [!NOTE]
> This hook is available, but has been superseded by the [UPDATE workflow (Version Update and Release)](https://github.com/7rikazhexde/python-project-sandbox/blob/main/.github/workflows/update-version-and-release.yml).\
> Please check the workflow for details.

- [update_pyproject_version.py](ci/update_pyproject_version.py)

- example

  ```toml
  [tool.poetry]
  name = "python-project-sandbox"
  version = "0.1.19" # Automatic increase
  description = "An experimental project to test out various tools."
  authors = ["7rikaz"]
  license = "MIT"
  readme = "README.md"
  ```

### Usage

> [!NOTE]
> If you are creating a pre-commit script with reference to this project, please make sure that the .pre-commit-config.yaml and pyproject.toml are set up correctly.\
> Also, pre-commit is applied to staged files. Note that if it is not staged, it will be Skipped.
> First, please run poetry run pre-commit run --all-files to make sure that the operation is OK.

Set pre-commit

The following command will create `.git/hooks/pre-commit`.

```bash
poetry run pre-commit install
```

Add all files that have changed

```bash
git add -A
```

git commit

example:

```bash
git commit -m "feat(search): add fuzzy search to search bar

This commit adds fuzzy search functionality to the search bar component. Fuzzy search allows users to find search results even if they make spelling mistakes or typos. This feature will enhance the user experience and make it easier to find what they are looking for.

Closes #1234"
```

If you want to test locally

```bash
poetry run pre-commit run --all-files
```

## post-commit

> [!NOTE]
> This hook is available, but has been superseded by the [UPDATE workflow (Version Update and Release)](https://github.com/7rikazhexde/python-project-sandbox/blob/main/.github/workflows/update-version-and-release.yml). Please check the workflow for details.

### Overview

For this project, use .git/hooks/post-commit to reference the version of pyproject.toml and create a git tag. Then push the main branch and tag.
If you are committing to a project for the first time, create a post-commit script.

### Usage

> [!NOTE]
> post-commit depends on the version of the pre-commit script and pyproject.toml.\
> If you are creating a post-commit script with reference to this project, please make sure that the .pre-commit-config.yaml and pyproject.toml are set up correctly.\
> First, please run .git/hooks/post-commit to make sure that the operation is OK.

1. Set create post-commit

   Execute the following command to create post-commit.

   ```bash
   cd scripts
   chmod +x create_post-commit.sh
   ./create_post-commit.sh
   ```

   > [!NOTE]
   > If post-commit does not exist, create a new post-commit and add execute permission (chmod +x).
   > If post-commit exists, create it as post-commit.second.
   > If you want to use it, merge or rename it to pre-sommit.
   > Execution privileges are not attached to post-commit.second, so grant them as necessary.

1. After the entire commit process

   After the entire commit process is complete, refer to [update_pyproject_version.py](ci/update_pyproject_version.py) to update and push the git tag.

   ```bash
   $ git tag
   v0.1.8
   v0.1.9 # git add from ["poetry"]["version"]
   ```

   If you want to test locally

   ```bash
   .git/hooks/post-commit
   ```

### pytest-coverage-comment

Use the following actions.
[pytest-coverage-comment](https://github.com/MishaKav/pytest-coverage-comment#example-usage)
