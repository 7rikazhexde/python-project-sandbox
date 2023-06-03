#!.venv/bin/python3

import re
import subprocess
import sys
from typing import Optional, Tuple

from tomlkit.toml_file import TOMLFile


def remote_tag_checker(remote: str, tag: Optional[str]) -> bool:
    checker = False
    try:
        # リモートブランチのタグを取得
        tags = subprocess.run(
            ["git", "ls-remote", "--tags", remote], capture_output=True, text=True
        ).stdout.splitlines()

        pattern = r"v(\d+\.\d+\.\d+)"
        match = re.search(pattern, tags[-1])
        if match:
            highest_tag = "v" + match.group(1)
            print(f"highest_tag: {highest_tag}")

        if tag is not None and tag <= highest_tag:
            print("Invalid tag version")
            error_message = f"Remote tag '{tag}' is an invalid tag version. Exiting the program. Please check pyproject.toml / version."
            sys.exit(error_message)
        checker = True

    except subprocess.CalledProcessError as e:
        error_code = e.returncode
        error_output = e.stderr
        print(f"error_code:{error_code}")
        print(f"error_output:{error_output}")
        error_message = "Failed to fetch remote tags. Exiting the program."
        sys.exit(error_message)
    return checker


def local_tag_checker(tag: Optional[str]) -> bool:
    checker = False
    try:
        # タグを降順(n,n-1,n-2)にソートして取得
        tags = subprocess.run(
            ["git", "tag", "--sort", "-v:refname"], capture_output=True, text=True
        ).stdout.splitlines()
        print(f"tags:{tags}")

        if tag is not None and tag <= tags[0]:
            print("Invalid tag version")
            error_message = f"Local tag '{tag}' is an invalid tag version. Exiting the program. Please check pyproject.toml / version."
            sys.exit(error_message)
        checker = True
    except subprocess.CalledProcessError as e:
        error_code = e.returncode
        error_output = e.stderr
        print(f"error_code:{error_code}")
        print(f"error_output:{error_output}")
        error_message = "No tags found. Exiting the program."
        sys.exit(error_message)
    return checker


def read_poetry_project_version() -> Tuple[bool, Optional[str]]:
    read_success_flag = False
    curent_ver = ""
    try:
        # pyproject.tomlファイルの読み込み
        toml = TOMLFile("pyproject.toml")
        toml_data = toml.read()
        toml_get_data = toml_data.get("tool", {})
        if "poetry" in toml_get_data:
            curent_ver = toml_get_data["poetry"].get("version", "")
            read_success_flag = True
        else:
            error_message = (
                "Failed to find 'poetry' section in pyproject.toml. Exit the program."
            )
            sys.exit(error_message)
    except Exception as e:
        error_message = f"Failed to update pyproject.toml. Error: {str(e)}"
        sys.exit(error_message)
    return read_success_flag, curent_ver


def get_arg(tag: str) -> str:
    if len(sys.argv) == 2:
        new_tag = sys.argv[1]
        pattern = r"^v[0-9]+\.[0-9]{1,3}\.[0-9]{1,3}$"
        if not re.match(pattern, new_tag):
            # 引数の指定に誤りがある場合
            error_message = (
                "Invalid tag format. Please enter in [vx.x.x]. Exit the program."
            )
            sys.exit(error_message)
    elif len(sys.argv) > 2:
        error_message = "Please enter ./create_tag_data.py [vx.x.x] Exit the program."
        sys.exit(error_message)
    else:
        new_tag = tag
    print(f"get_arg() return new_tag:{new_tag}")
    return new_tag


if __name__ == "__main__":  # pragma: no cover
    remote_to_check = "origin"
    remote_tag_checker_flag = False
    local_tag_checker_flag = False
    read_success_flag, new_tag = read_poetry_project_version()
    new_tag = f"v{new_tag or ''}"
    new_tag = get_arg(new_tag)
    remote_tag_checker_flag = remote_tag_checker(remote_to_check, new_tag)
    local_tag_checker_flag = local_tag_checker(new_tag)
    # 新しいタグを作成する
    if remote_tag_checker_flag is True and local_tag_checker_flag is True:
        subprocess.run(["git", "tag", new_tag])
    subprocess.run(["git", "tag"])
