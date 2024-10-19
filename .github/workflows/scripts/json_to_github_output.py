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
    github_env = os.getenv("GITHUB_ENV")

    if github_output is None:
        print("GITHUB_OUTPUT is not set. Unable to set output.")
        sys.exit(1)

    # Write all outputs to GITHUB_OUTPUT at once to avoid file locking issues
    with open(github_output, "a") as fh:
        for name, value in outputs.items():
            fh.write(f"{name}={value}\n")
        fh.flush()
        print(f"Debug: Written to GITHUB_OUTPUT -> {outputs}")

    # Additionally write to GITHUB_ENV to make sure they are set as environment variables
    if github_env:
        with open(github_env, "a") as env_file:
            for name, value in outputs.items():
                env_file.write(f"{name}={value}\n")
            env_file.flush()
            print(f"Debug: Written to GITHUB_ENV -> {outputs}")


def parse_json(data: Any, prefix: str = "") -> Dict[str, str]:
    """
    Recursively parse JSON data and collect GitHub Actions outputs.

    :param data: The JSON data to be parsed.
    :param prefix: Prefix to add to the variable names (used for nested dictionaries).
    :return: A dictionary of parsed output variables.
    """
    outputs = {}
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                outputs.update(parse_json(value, prefix + key.upper() + "_"))
            else:
                outputs[f"{prefix}{key.upper()}"] = str(value)
    elif isinstance(data, list):
        list_values = json.dumps(data)
        outputs[prefix[:-1]] = list_values  # Remove trailing underscore
        for index, item in enumerate(data):
            if isinstance(item, dict):
                outputs.update(parse_json(item, prefix + f"{index}_"))
            else:
                outputs[f"{prefix}{index}"] = str(item)

    return outputs


if __name__ == "__main__":
    json_file = sys.argv[1]

    # Load the JSON data from the file
    with open(json_file, "r") as f:
        data = json.load(f)

    # Parse the JSON data and write to GITHUB_OUTPUT and GITHUB_ENV
    collected_outputs = parse_json(data)
    set_github_output(collected_outputs)
