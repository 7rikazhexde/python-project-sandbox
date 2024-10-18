import json
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
            try:
                current_data = current_data[key]
            except IndexError:
                print(
                    f"Error extracting value at path {path}: index {key} out of range"
                )
                sys.exit(1)
        elif isinstance(current_data, dict) and isinstance(key, str):
            try:
                current_data = current_data[key]
            except KeyError:
                print(f"Error extracting value at path {path}: key '{key}' not found")
                sys.exit(1)
        else:
            print(
                f"Error extracting value at path {path}: incompatible type or key/index"
            )
            sys.exit(1)
    return current_data


def parse_path(path: str) -> List[Union[str, int]]:
    """
    パス文字列をリストに変換する。
    例: "['COMPLEX_LIST'][0]['name']" -> ['COMPLEX_LIST', 0, 'name']
    """
    path = (
        path.strip("[]")
        .replace("][", ".")
        .replace("[", ".")
        .replace("]", "")
        .replace("'", "")
        .replace('"', "")
    )
    elements = path.split(".")
    result: List[Union[str, int]] = []
    for element in elements:
        if element.isdigit():
            result.append(int(element))
        else:
            result.append(element)
    return result


def main() -> None:
    # ローカルテスト用にJSONを直接定義
    json_str = """
    [
        {"name": "task1", "status": "complete", "details": {"time": "5m", "result": "success"}},
        {"name": "task2", "status": "incomplete", "details": {"time": "10m", "result": "failed"}}
    ]
    """

    # JSONのパース
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        print("Invalid JSON format.")
        sys.exit(1)

    # コマンドライン引数からパスを取得し、それぞれの値を取得して表示
    for json_path in sys.argv[1:]:
        path_list = parse_path(json_path)
        try:
            value = get_value_by_path(data, path_list)
            print(f"Value at path {json_path}: {value}")
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
