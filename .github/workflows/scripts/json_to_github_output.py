import json
import os
import sys
from typing import Any, Dict


def set_github_output(name: str, value: str) -> None:
    """GitHub Actionsの新しい方法で出力を設定"""
    with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
        print(f"{name}<<EOF", file=fh)
        print(value, file=fh)
        print("EOF", file=fh)


def parse_json(
    data: Any,
    prefix: str = "",
    debug: bool = False,
) -> None:
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
        output = f"{prefix[:-1]}={list_values}"
        if debug:
            print(output)
        else:
            set_github_output(prefix[:-1], list_values)
        for index, item in enumerate(data):
            if isinstance(item, dict):
                parse_json(item, prefix + f"{index}_", debug)
            else:
                output = f"{prefix}{index}={item}"
                if debug:
                    print(output)
                else:
                    set_github_output(prefix + str(index), str(item))


if __name__ == "__main__":
    json_file: str = sys.argv[1]
    debug = "--debug" in sys.argv

    with open(json_file, "r") as f:
        data: Dict[str, Any] = json.load(f)

    parse_json(data, debug=debug)
