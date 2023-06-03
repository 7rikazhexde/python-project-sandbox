#!.venv/bin/python3

import argparse
import os
import re
import subprocess
import sys
from typing import Optional, Tuple

from tomlkit.toml_file import TOMLFile


def update_poetry_project_version(new_tag: str, toml: TOMLFile) -> None:
    toml_data = toml.read()
    try:
        # バージョンの更新
        toml_get_data = toml_data.get("tool")
        if toml_get_data is not None and "poetry" in toml_get_data:
            toml_get_data["poetry"]["version"] = new_tag
            # pyproject.tomlファイルの書き込み
            toml.write(toml_data)
        else:
            raise KeyError("Failed to find 'poetry' section in 'tool'")

    except Exception as e:
        error_message = f"Failed to update pyproject.toml. Error: {str(e)}"
        sys.exit(error_message)


def get_arg() -> Optional[str]:
    if len(sys.argv) == 2:
        new_tag = sys.argv[1]
        pattern = r"^[0-9]+\.[0-9]{1,3}\.[0-9]{1,3}$"
        if not re.match(pattern, new_tag):
            # 引数の指定に誤りがある場合
            error_message = (
                "Invalid tag format. Please enter in [x.x.x]. Exit the program."
            )
            sys.exit(error_message)
    elif len(sys.argv) > 2:
        error_message = "Please enter ./create_tag_data.py [x.x.x] Exit the program."
        sys.exit(error_message)
    else:
        new_tag = None
    return new_tag


def get_user_input() -> Optional[str]:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tag",
        required=False,
        nargs="?",
        const=None,
        help="Enter the tag in the format [x.x.x]",
    )
    args = parser.parse_args()

    user_input = args.tag
    pattern = r"^[0-9]+\.[0-9]{1,3}\.[0-9]{1,3}$"

    if user_input is None and not os.isatty(sys.stdin.fileno()):
        # 標準入力からデータが渡された場合
        user_input = sys.stdin.read().strip()
    elif user_input is None:
        user_input = input("Enter the tag in the format [x.x.x]: ")

    if user_input == "":
        # 入力が空の場合は処理を適用
        user_input = None
    elif not re.match(pattern, user_input):
        # 入力の形式が正しくない場合
        error_message = (
            "Invalid tag format. Please enter in [x.x.x]. Exiting the program."
        )
        sys.exit(error_message)

    return user_input


def create_ver(input_ver: Optional[str]) -> Tuple[bool, str, TOMLFile]:
    # pyproject.tomlファイルの読み込み
    toml = TOMLFile("pyproject.toml")
    toml_data = toml.read()
    toml_get_data = toml_data.get("tool")
    # バージョンの更新
    if toml_get_data is not None and "poetry" in toml_get_data:
        current_data = toml_get_data["poetry"].get("version")
    else:
        current_data = "0.0.0"
    major, minor, patch = map(int, current_data.split("."))
    create_tag_flag = False
    # 引数指定のデータあり
    if input_ver is not None:
        new_ver = input_ver
        create_tag_flag = True
        # pyproject.tomlのversion以下の場合はエラー
        if input_ver <= current_data:
            create_tag_flag = False
            error_message = f"The specified tag '{input_ver}' must be greater than the latest tag 'v{current_data}'. Exit the program."
            sys.exit(error_message)
    # 引数指定のデータなし
    else:
        # pyproject.tomlのversionをインクリメント
        if patch < 999:
            patch += 1
        elif minor < 999:
            minor += 1
            patch = 0
        else:
            major += 1
            minor = 0
            patch = 0
        new_ver = f"{major}.{minor}.{patch}"
        create_tag_flag = True
    return create_tag_flag, new_ver, toml


if __name__ == "__main__":  # pragma: no cover
    # 正しいデータ形式かチェック
    input_ver = get_arg()
    # 引数なし：pyproject.tomlのversionをインクリメント
    # 引数あり：pyproject.tomlのversion以上なら更新
    create_tag_flag, new_ver, toml = create_ver(input_ver)
    if create_tag_flag:
        update_poetry_project_version(new_ver, toml)
        subprocess.run(["git", "add", "pyproject.toml"])
