import json
import os
import sys
from typing import Any, List, Union


def get_value_by_path(data: Any, path: List[Union[str, int]]) -> Any:
    """
    指定されたパスに従ってJSONデータから値を取得する。
    :param data: JSON形式のデータ
    :param path: パスのリスト（例: ['COMPLEX_LIST', 0, 'name']）
    :return: 指定されたパスの値
    """
    current_data = data
    for key in path:
        if isinstance(current_data, list) and isinstance(key, int):
            # リストの場合、インデックスとしてアクセス
            try:
                current_data = current_data[key]
            except IndexError:
                print(
                    f"Error extracting value at {'.'.join(map(str, path))}: index {key} out of range"
                )
                sys.exit(1)
        elif isinstance(current_data, dict) and isinstance(key, str):
            # 辞書の場合、キーとしてアクセス
            try:
                current_data = current_data[key]
            except KeyError:
                print(
                    f"Error extracting value at {'.'.join(map(str, path))}: key '{key}' not found"
                )
                sys.exit(1)
        else:
            print(
                f"Error extracting value at {'.'.join(map(str, path))}: incompatible type or key/index"
            )
            sys.exit(1)
    return current_data


def set_github_env(name: str, value: str) -> None:
    """GitHub Actionsの環境ファイルを使って環境変数を設定"""
    github_env = os.getenv("GITHUB_ENV")
    if github_env is None:
        print("GITHUB_ENV is not set. Unable to set environment variable.")
        sys.exit(1)

    with open(github_env, "a") as fh:
        print(f"{name}={value}", file=fh)


def parse_path(path: str) -> List[Union[str, int]]:
    """
    パス文字列をリストに変換する。
    例: "['COMPLEX_LIST'][0]['name']" -> ['COMPLEX_LIST', 0, 'name']
    """
    path = (
        path.replace("][", ".")
        .replace("[", ".")
        .replace("]", "")
        .replace("'", "")
        .replace('"', "")
    )
    elements = path.split(".")
    result: List[Union[str, int]] = []
    for element in elements:
        if element.isdigit():
            result.append(int(element))  # インデックスとして整数に変換
        else:
            result.append(element)
    return result


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
        path_list = parse_path(json_path)
        value = get_value_by_path(data, path_list)
        env_var_name = f"VALUE_{'_'.join(map(str, path_list)).upper()}"
        set_github_env(env_var_name, str(value))


if __name__ == "__main__":
    main()
