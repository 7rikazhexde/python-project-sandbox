# trial-test

An experimental project to test out various tools.

## pre-commit

This project is using [pre-commit](https://github.com/pre-commit/pre-commit) via poetry

1. Using [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks)

1. Using Static Analysis Tools

   - [isort](https://pypi.org/project/isort/): automatic organization of import statements
   - [black](https://pypi.org/project/black/): code formatter for Python (PEP8 compliant)
   - [flake8](https://pypi.org/project/flake8/): grammar checking
   - [mypy](https://pypi.org/project/mypy/): type checking with type annotations

1. Run update pyproject.toml version up script

   - [update_pyproject_version.py](ci/update_pyproject_version.py)
