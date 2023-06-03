# trial-test

An experimental project to test out various tools.

## Tabale of contents

- [trial-test](#trial-test)
  - [Tabale of contents](#tabale-of-contents)
  - [pre-commit](#pre-commit)
    - [Overview](#overview)
    - [Usage](#usage)
  - [post-commit](#post-commit)
    - [Overview](#overview-1)
    - [Usage](#usage-1)

## pre-commit

This project is using [pre-commit](https://github.com/pre-commit/pre-commit) via poetry.

### Overview

1. Using [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks)

1. Using Static Analysis Tools

   - [isort](https://pypi.org/project/isort/): Automatic organization of import statements
   - [black](https://pypi.org/project/black/): Code formatter for Python (PEP8 compliant)
   - [flake8](https://pypi.org/project/flake8/): Grammar checking
   - [mypy](https://pypi.org/project/mypy/): Type checking with type annotations
   - [mdformat](https://pypi.org/project/mdformat/): Opinionated Markdown formatter that can be used to enforce a consistent style in Markdown files.

1. Run update pyproject.toml version up script

   - [update_pyproject_version.py](ci/update_pyproject_version.py)

### Usage

Set pre-commit

```bash
poetry run pre-commit install
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

1. Create post-commit

   If post-commit.sample exists

   ```bash
   cd ./git/hooks
   cp post-commit.sample post-commit
   ```

   If post-commit.sample does not exist

   ```bash
   cd ./git/hooks
   touch post-commit
   ```

1. Scripting

   Copy the following code and write the script.

   ```bash
   #!/usr/bin/env bash

   source $HOME/develop/git/trial-test/.venv/bin/activate
   poetry run python ci/run_git_tag_base_pyproject.py
   if [ $? -ne 0 ]; then
       printf "Error occurred in run_git_tag_base_pyproject.py. Exiting post-commit.\n"
       exit 1
   fi

   git push origin main:main
   git push --tags
   printf ".git/hooks/post-commit end!!!\n"
   ```

1. Grant execute permission.

   ```bash
   chmod +x post-commit
   ```

If you want to test locally

```bash
./git/hooks/post-commit
```
