import json
import os
import sys
from typing import Any, Dict


def parse_json_to_github_output(
    data: Dict[str, Any], prefix: str = "", debug: bool = False
) -> None:
    github_output = os.getenv("GITHUB_OUTPUT")
    if not github_output:
        raise ValueError("GITHUB_OUTPUT environment variable is not set.")

    with open(github_output, "a") as f:
        for key, value in data.items():
            if isinstance(value, dict):
                parse_json_to_github_output(value, prefix + key.upper() + "_", debug)
            elif isinstance(value, list):
                list_values = json.dumps(value)
                if debug:
                    print(f"{prefix}{key.upper()}={list_values}")
                else:
                    f.write(f"{prefix}{key.upper()}={list_values}\n")
            else:
                if debug:
                    print(f"{prefix}{key.upper()}={value}")
                else:
                    f.write(f"{prefix}{key.upper()}={value}\n")


if __name__ == "__main__":
    json_file: str = sys.argv[1]
    debug = "--debug" in sys.argv

    with open(json_file, "r") as f:
        data: Dict[str, Any] = json.load(f)

    parse_json_to_github_output(data, debug=debug)
