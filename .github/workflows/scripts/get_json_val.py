import json
import os
import sys
from typing import Any


def get_value_by_path(data: Any, path: str) -> Any:
    """
    指定されたパスに従ってJSONデータから値を取得する。
    :param data: JSON形式のデータ
    :param path: キーやインデックスを表すパス（例: "['COMPLEX_LIST'][0]['name']"）
    :return: 指定されたパスの値
    """
    try:
        # パスに従って値を取得
        value = eval(f"data{path}")
        return value
    except (KeyError, IndexError, TypeError) as e:
        print(f"Error extracting value at {path}: {e}")
        sys.exit(1)


def set_github_env(name: str, value: str) -> None:
    """GitHub Actionsの環境ファイルを使って環境変数を設定"""
    github_env = os.getenv("GITHUB_ENV")
    if github_env is None:
        print("GITHUB_ENV is not set. Unable to set environment variable.")
        sys.exit(1)

    with open(github_env, "a") as fh:
        print(f"{name}={value}", file=fh)


def main() -> None:
    # 環境変数からJSONデータを取得
    json_str = os.getenv("COMPLEX_LIST")
    if not json_str:
        print("COMPLEX_LIST is empty. Stopping workflow.")
        sys.exit(1)

    # JSONのパース
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        print("Invalid JSON format. Stopping workflow.")
        sys.exit(1)

    # コマンドライン引数からパスを取得し、それぞれの値を取得して環境変数に設定
    for json_path in sys.argv[1:]:
        value = get_value_by_path(data, json_path)
        env_var_name = f"VALUE_{json_path.replace('[', '_').replace(']', '').replace('\'', '').replace('\"', '').replace('.', '_')}"
        set_github_env(env_var_name, str(value))


if __name__ == "__main__":
    main()
