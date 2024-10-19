import json
import os
import sys
from typing import Any, Dict


def set_github_output(name: str, value: str) -> None:
    """
    Set a GitHub Actions output variable by appending it to the GITHUB_OUTPUT file.

    :param name: The name of the output variable to set.
    :param value: The value of the output variable to set.
    """
    github_output = os.getenv("GITHUB_OUTPUT")
    if github_output is None:
        print("GITHUB_OUTPUT is not set. Unable to set output.")
        sys.exit(1)

    # Check if the GITHUB_OUTPUT file exists; if not, exit with an error message.
    if not os.path.exists(github_output):
        print(f"Error: The GITHUB_OUTPUT file at {github_output} does not exist.")
        sys.exit(1)

    with open(github_output, "a") as fh:
        fh.write(f"{name}={value}\n")
        fh.flush()  # Flush after writing for debugging purposes
        print(
            f"Debug: Written to GITHUB_OUTPUT -> {name}={value}"
        )  # Additional debug information


def set_github_env(name: str, value: str) -> None:
    """
    Set an environment variable for GitHub Actions by appending it to the GITHUB_ENV file.

    :param name: The name of the environment variable to set.
    :param value: The value of the environment variable to set.
    """
    github_env = os.getenv("GITHUB_ENV")
    if github_env is None:
        print("GITHUB_ENV is not set. Unable to set environment variable.")
        sys.exit(1)

    # Check if the GITHUB_ENV file exists; if not, exit with an error message.
    if not os.path.exists(github_env):
        print(f"Error: The GITHUB_ENV file at {github_env} does not exist.")
        sys.exit(1)

    with open(github_env, "a") as env_file:
        env_file.write(f"{name}={value}\n")
        env_file.flush()  # Flush after writing to ensure changes are saved
        print(
            f"Debug: Written to GITHUB_ENV -> {name}={value}"
        )  # Additional debug information


def parse_json(
    data: Any,
    prefix: str = "",
    debug: bool = False,
) -> None:
    """
    Recursively parse JSON data and set GitHub Actions outputs and environment variables.

    :param data: The JSON data to be parsed.
    :param prefix: Prefix to add to the variable names (used for nested dictionaries).
    :param debug: If True, print debug information to standard output.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                # Recursively handle nested dictionaries and lists
                parse_json(value, prefix + key.upper() + "_", debug)
            else:
                # Handle single values
                output = f"{prefix}{key.upper()}={value}"
                if debug:
                    print(output)
                else:
                    print(
                        f"Debug: Processing key={prefix + key.upper()} value={value}"
                    )  # Debug information
                    set_github_output(prefix + key.upper(), str(value))
                    set_github_env(prefix + key.upper(), str(value))
    elif isinstance(data, list):
        # Write the entire list as a JSON string
        list_values = json.dumps(data)
        output = (
            f"{prefix[:-1]}={list_values}"  # Remove the trailing underscore from prefix
        )
        if debug:
            print(output)
        else:
            print(
                f"Debug: Processing list prefix={prefix[:-1]} value={list_values}"
            )  # Debug information
            set_github_output(prefix[:-1], list_values)
            set_github_env(prefix[:-1], list_values)
        # Process each item in the list individually
        for index, item in enumerate(data):
            if isinstance(item, dict):
                parse_json(item, prefix + f"{index}_", debug)
            else:
                output = f"{prefix}{index}={item}"
                if debug:
                    print(output)
                else:
                    print(
                        f"Debug: Processing list item prefix={prefix + str(index)} value={item}"
                    )  # Debug information
                    set_github_output(prefix + str(index), str(item))
                    set_github_env(prefix + str(index), str(item))


if __name__ == "__main__":
    # Retrieve the JSON file path and optional debug flag from command line arguments
    json_file: str = sys.argv[1]
    debug = "--debug" in sys.argv

    # Load the JSON data from the file
    with open(json_file, "r") as f:
        data: Dict[str, Any] = json.load(f)

    # Parse the JSON data and write to GITHUB_OUTPUT and GITHUB_ENV (or print if in debug mode)
    parse_json(data, debug=debug)
