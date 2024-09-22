# trial-test

An experimental project to test out various tools.

## Pytest Coverage Comment

[![Test Multi-OS](https://github.com/7rikazhexde/trial-test/actions/workflows/test_multi_os.yml/badge.svg)](https://github.com/7rikazhexde/trial-test/actions/workflows/test_multi_os.yml) [![Coverage Status](https://img.shields.io/badge/Coverage-check%20here-blue.svg)](https://github.com/7rikazhexde/trial-test/tree/coverage)

## pytest-html

[![pytest-html Report and Deploy Multi-OS](https://github.com/7rikazhexde/trial-test/actions/workflows/test_pytest-cov-report_deploy_multi_os.yml/badge.svg)](https://github.com/7rikazhexde/trial-test/actions/workflows/test_pytest-cov-report_deploy_multi_os.yml)

[![ubuntu_latest](https://img.shields.io/badge/ubuntu_latest-url-brightgreen)](https://7rikazhexde.github.io/trial-test/ubuntu-latest/report_page.html) [![macos-13](https://img.shields.io/badge/macos_13-url-ff69b4)](https://7rikazhexde.github.io/trial-test/macos-13/report_page.html) [![windows-latest](https://img.shields.io/badge/windows_latest-url-blue)](https://7rikazhexde.github.io/trial-test/windows-latest/report_page.html)

## pytest-cov

[![pytest-cov Report and Deploy Multi-OS](https://github.com/7rikazhexde/trial-test/actions/workflows/test_pytest-html-report_deploy_multi_os.yml/badge.svg)](https://github.com/7rikazhexde/trial-test/actions/workflows/test_pytest-html-report_deploy_multi_os.yml)

[![ubuntu_latest](https://img.shields.io/badge/ubuntu_latest-url-brightgreen)](https://7rikazhexde.github.io/trial-test/ubuntu-latest/htmlcov_ubuntu-latest/index.html) [![macos-13](https://img.shields.io/badge/macos_13-url-ff69b4)](https://7rikazhexde.github.io/trial-test/macos-13/htmlcov_macos-13/index.html) [![windows-latest](https://img.shields.io/badge/windows_latest-url-blue)](https://7rikazhexde.github.io/trial-test/windows-latest/htmlcov_windows-latest/index.html)

## Tabale of contents

- [trial-test](#trial-test)
  - [Pytest Coverage Comment](#pytest-coverage-comment)
  - [pytest-html](#pytest-html)
  - [pytest-cov](#pytest-cov)
  - [Tabale of contents](#tabale-of-contents)
  - [pre-commit](#pre-commit)
    - [Overview](#overview)
    - [Usage](#usage)
  - [post-commit](#post-commit)
    - [Overview](#overview-1)
    - [Usage](#usage-1)
    - [pytest-coverage-comment](#pytest-coverage-comment-1)

## pre-commit

This project is using [pre-commit](https://github.com/pre-commit/pre-commit) via poetry.

### Overview

1. Using [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks)

1. Using Static Analysis Tools

   - [ruff](https://pypi.org/project/ruff/): An extremely fast Python linter and code formatter, written in Rust.
   - [mypy](https://pypi.org/project/mypy/): Type checking with type annotations
   - [mdformat](https://pypi.org/project/mdformat/): Opinionated Markdown formatter that can be used to enforce a consistent style in Markdown files.

1. Run update pyproject.toml version up script

   - [update_pyproject_version.py](ci/update_pyproject_version.py)

   - example

     ```toml
     [tool.poetry]
     name = "trial-test"
     version = "0.1.19" # Automatic increase
     description = "An experimental project to test out various tools."
     authors = ["7rikaz_wsl1 <7rikaz.h785.stat2ltas41lcijad@gmail.com>"]
     license = "MIT"
     readme = "README.md"
     ```

### Usage

> **Note**\
> **If you are creating a pre-commit script with reference to this project, please make sure that the .pre-commit-config.yaml and pyproject.toml are set up correctly.**\
> **Also, pre-commit is applied to staged files. Note that if it is not staged, it will be Skipped.**
> **First, please run poetry run pre-commit run --all-files to make sure that the operation is OK.**

Set pre-commit\
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

### Overview

For this project, use .git/hooks/post-commit to reference the version of pyproject.toml and create a git tag. Then push the main branch and tag.
If you are committing to a project for the first time, create a post-commit script.

### Usage

> **Note**\
> **post-commit depends on the version of the pre-commit script and pyproject.toml.**\
> **If you are creating a post-commit script with reference to this project, please make sure that the .pre-commit-config.yaml and pyproject.toml are set up correctly.**\
> **First, please run .git/hooks/post-commit to make sure that the operation is OK.**

1. Set create post-commit

   Execute the following command to create post-commit.

   ```bash
   cd scripts
   chmod +x create_post-commit.sh
   ./create_post-commit.sh
   ```

   > **Note**\
   > **If post-commit does not exist, create a new post-commit and add execute permission (chmod +x).**
   > **If post-commit exists, create it as post-commit.second.**
   > **If you want to use it, merge or rename it to pre-sommit.**
   > **Execution privileges are not attached to post-commit.second, so grant them as necessary.**

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
