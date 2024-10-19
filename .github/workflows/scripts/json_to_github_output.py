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
        print(f"Debug: Written to GITHUB_OUTPUT -> {name}={value}")


def parse_json(data: Any, prefix: str = "", debug: bool = False) -> None:
    """
    Recursively parse JSON data and set GitHub Actions outputs.

    :param data: The JSON data to be parsed.
    :param prefix: Prefix to add to the variable names (used for nested dictionaries).
    :param debug: If True, print debug information to standard output.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                parse_json(value, prefix + key.upper() + "_", debug)
            else:
                output = f"{prefix}{key.upper()}={value}"
                if debug:
                    print(output)
                else:
                    set_github_output(prefix + key.upper(), str(value))
    elif isinstance(data, list):
        list_values = json.dumps(data)
        if debug:
            print(f"{prefix[:-1]}={list_values}")
        else:
            set_github_output(prefix[:-1], list_values)
        for index, item in enumerate(data):
            if isinstance(item, dict):
                parse_json(item, prefix + f"{index}_", debug)
            else:
                set_github_output(prefix + str(index), str(item))


if __name__ == "__main__":
    json_file: str = sys.argv[1]
    debug = "--debug" in sys.argv

    with open(json_file, "r") as f:
        data: Dict[str, Any] = json.load(f)

    parse_json(data, debug=debug)
