#!.venv/bin/python3

import re
import subprocess
import sys
from typing import Tuple

from tomlkit.toml_file import TOMLFile


def update_poetry_project_version(new_tag: str, toml: TOMLFile) -> None:
    """Update [poetry].[version] in pyproject.toml

    Args:
        new_tag (str): [major].[minor].[patch]
        toml (TOMLFile): TOMLFile("pyproject.toml")

    Raises:
        KeyError: Failed to update pyproject.toml
    """
    toml_data = toml.read()
    try:
        # Update version
        toml_get_data = toml_data.get("tool")
        if toml_get_data is not None and "poetry" in toml_get_data:
            toml_get_data["poetry"]["version"] = new_tag
            # Writing the pyproject.toml file
            toml.write(toml_data)
            print(f"Updated pyproject.toml version to {new_tag}")
        else:
            raise KeyError("Failed to find 'poetry' section in 'tool'")

    except Exception as e:
        error_message = f"Failed to update pyproject.toml. Error: {str(e)}"
        sys.exit(error_message)


def get_arg() -> str:
    """Version specified by command line arguments

    Raises:
        SystemExit: Invalid tag format([major].[minor].[patch]) or no argument provided

    Returns:
        str: [major].[minor].[patch]
    """
    if len(sys.argv) == 2:
        new_tag = sys.argv[1]
        pattern = r"^[0-9]+\.[0-9]{1,3}\.[0-9]{1,3}$"
        if not re.match(pattern, new_tag):
            error_message = (
                "Invalid tag format. Please enter in [x.x.x]. Exit the program."
            )
            sys.exit(error_message)
        return new_tag
    else:
        error_message = "Please provide a version number. Usage: ./update_pyproject_version.py [x.x.x]"
        sys.exit(error_message)


def create_ver(input_ver: str) -> Tuple[bool, str, TOMLFile]:
    """Create information of [poetry].[version] in pyproject.toml

    Args:
        input_ver (str): [major].[minor].[patch]

    Returns:
        Tuple[bool, str, TOMLFile]: Information of [poetry].[version] in pyproject.toml
    """
    # Load the pyproject.toml file
    toml = TOMLFile("pyproject.toml")
    toml_data = toml.read()
    toml_get_data = toml_data.get("tool")
    # Get current version
    if toml_get_data is not None and "poetry" in toml_get_data:
        current_data = toml_get_data["poetry"].get("version")
    else:
        current_data = "0.0.0"

    # Check if input version is greater than current version
    if input_ver <= current_data:
        error_message = f"The specified version '{input_ver}' must be greater than the current version '{current_data}'. Exit the program."
        sys.exit(error_message)
    return True, input_ver, toml


if __name__ == "__main__":  # pragma: no cover
    # Check for correct data format and get version
    input_ver = get_arg()
    # Update if version is greater than version of pyproject.toml
    create_tag_flag, new_ver, toml = create_ver(input_ver)
    if create_tag_flag:
        update_poetry_project_version(new_ver, toml)
        subprocess.run(["git", "add", "pyproject.toml"])
    else:
        print("No version update needed.")
