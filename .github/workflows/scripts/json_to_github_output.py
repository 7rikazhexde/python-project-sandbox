import json
import os
import sys
from typing import Any, Dict


def set_github_output(outputs: Dict[str, str]) -> None:
    """
    Set multiple GitHub Actions output variables by appending them to the GITHUB_OUTPUT file at once.

    :param outputs: Dictionary of output variables to set.
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
        for name, value in outputs.items():
            fh.write(f"{name}={value}\n")
        fh.flush()  # Flush after writing for debugging purposes
        print(f"Debug: Written to GITHUB_OUTPUT -> {outputs}")


def parse_json(data: Any, prefix: str = "", debug: bool = False) -> Dict[str, str]:
    """
    Recursively parse JSON data and collect GitHub Actions outputs.

    :param data: The JSON data to be parsed.
    :param prefix: Prefix to add to the variable names (used for nested dictionaries).
    :param debug: If True, print debug information to standard output.
    :return: A dictionary of parsed output variables.
    """
    outputs = {}
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                outputs.update(parse_json(value, prefix + key.upper() + "_", debug))
            else:
                output_key = f"{prefix}{key.upper()}"
                output_value = str(value)
                if debug:
                    print(f"{output_key}={output_value}")
                else:
                    outputs[output_key] = output_value
    elif isinstance(data, list):
        list_values = json.dumps(data)
        if debug:
            print(f"{prefix[:-1]}={list_values}")
        else:
            outputs[prefix[:-1]] = list_values
        for index, item in enumerate(data):
            if isinstance(item, dict):
                outputs.update(parse_json(item, prefix + f"{index}_", debug))
            else:
                outputs[f"{prefix}{index}"] = str(item)

    return outputs


if __name__ == "__main__":
    # Retrieve the JSON file path and optional debug flag from command line arguments
    json_file: str = sys.argv[1]
    debug = "--debug" in sys.argv

    # Load the JSON data from the file
    with open(json_file, "r") as f:
        data: Dict[str, Any] = json.load(f)

    # Parse the JSON data and collect outputs
    collected_outputs = parse_json(data, debug=debug)

    # Write all collected outputs to GITHUB_OUTPUT at once
    if not debug:
        set_github_output(collected_outputs)
