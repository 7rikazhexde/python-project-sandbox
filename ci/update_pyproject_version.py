#!.venv/bin/python3

import re
import sys

from tomlkit.toml_file import TOMLFile


def update_poetry_project_version(new_tag: str, toml: TOMLFile) -> None:
    toml_data = toml.read()
    try:
        toml_get_data = toml_data.get("tool")
        if toml_get_data is not None and "poetry" in toml_get_data:
            toml_get_data["poetry"]["version"] = new_tag
            toml.write(toml_data)
            print(f"Updated pyproject.toml version to {new_tag}")
        else:
            raise KeyError("Failed to find 'poetry' section in 'tool'")
    except Exception as e:
        print(f"Failed to update pyproject.toml. Error: {str(e)}")
        sys.exit(1)


def get_arg() -> str:
    if len(sys.argv) == 2:
        new_tag = sys.argv[1]
        pattern = r"^[0-9]+\.[0-9]{1,3}\.[0-9]{1,3}$"
        if not re.match(pattern, new_tag):
            print("Invalid tag format. Please enter in [x.x.x].")
            sys.exit(1)
        return new_tag
    else:
        print(
            "Please provide a version number. Usage: ./update_pyproject_version.py [x.x.x]"
        )
        sys.exit(1)


if __name__ == "__main__":
    new_version = get_arg()
    toml = TOMLFile("pyproject.toml")
    update_poetry_project_version(new_version, toml)
