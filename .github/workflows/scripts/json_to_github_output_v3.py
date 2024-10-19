import json
import os
import sys
from typing import Any, Dict


def set_github_output(name: str, value: str) -> None:
    """GitHub Actionsの環境ファイルを使って出力を設定"""
    github_output = os.getenv("GITHUB_OUTPUT")
    if github_output is None:
        print("GITHUB_OUTPUT is not set. Unable to set output.")
        sys.exit(1)

    if not os.path.exists(github_output):
        print(f"Error: The GITHUB_OUTPUT file at {github_output} does not exist.")
        sys.exit(1)

    with open(github_output, "a") as fh:
        fh.write(f"{name}={value}\n")
        fh.flush()
        print(f"Debug: Written to GITHUB_OUTPUT -> {name}={value}")

    # GITHUB_ENVを利用して環境変数としても設定
    github_env = os.getenv("GITHUB_ENV")
    if github_env:
        with open(github_env, "a") as env_file:
            env_file.write(f"{name}={value}\n")
            env_file.flush()
            print(f"Debug: Written to GITHUB_ENV -> {name}={value}")


def parse_json(
    data: Any,
    prefix: str = "",
    debug: bool = False,
) -> None:
    """
    JSONデータを再帰的に探索し、デバッグモードなら標準出力に表示、
    通常モードならGITHUB_OUTPUTに書き込む。

    :param data: JSON形式の辞書データ
    :param prefix: 環境変数名に付加するプレフィックス（ネストされた辞書対応）
    :param debug: デバッグモードの有無
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                parse_json(value, prefix + key.upper() + "_", debug)
            else:
                set_variable_output(prefix + key.upper(), value, debug)
    elif isinstance(data, list):
        list_values = json.dumps(data)
        set_variable_output(prefix[:-1], list_values, debug)
        for index, item in enumerate(data):
            if isinstance(item, dict):
                parse_json(item, prefix + f"{index}_", debug)
            else:
                set_variable_output(prefix + str(index), item, debug)


def set_variable_output(key: str, value: Any, debug: bool) -> None:
    """
    環境変数やGITHUB_OUTPUTに出力する共通関数
    :param key: 環境変数のキー
    :param value: 環境変数の値
    :param debug: デバッグモードの有無
    """
    output = f"{key}={value}"
    if debug:
        print(output)
    else:
        print(f"Debug: Processing key={key} value={value}")
        set_github_output(key, str(value))


if __name__ == "__main__":
    json_file: str = sys.argv[1]
    debug = "--debug" in sys.argv

    with open(json_file, "r") as f:
        data: Dict[str, Any] = json.load(f)

    parse_json(data, debug=debug)
