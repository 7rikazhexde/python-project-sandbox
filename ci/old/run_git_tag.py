#!../../.venv/bin/python3

import re
import subprocess
import sys

from tomlkit.toml_file import TOMLFile


def remote_tag_checker(remote, tag=None):
    # print('call remote_tag_checker()')
    try:
        # リモートブランチのタグを取得
        tags = subprocess.run(
            ["git", "ls-remote", "--tags", remote], capture_output=True, text=True
        ).stdout.splitlines()
        latest_tag = ""
        for remote_tag in tags:
            if tag in remote_tag:
                latest_tag = remote_tag.split("refs/tags/")[-1]
                break
        if latest_tag == tag:
            error_message = (
                f"Tag '{tag}' already exists in the remote branch. Exit the program."
            )
            sys.exit(error_message)
    except subprocess.CalledProcessError as e:
        error_code = e.returncode
        error_output = e.stderr
        print(f"error_code:{error_code}")
        print(f"error_output:{error_output}")
        latest_tag = ""
        error_message = "Failed to fetch remote tags. Exit the program."
        sys.exit(error_message)
    return latest_tag


def local_tag_checker(tag=None):
    # print('call local_tag_checker()')
    try:
        # タグを降順(n,n-1,n-2)にソートして取得
        tags = subprocess.run(
            ["git", "tag", "--sort", "-v:refname"], capture_output=True, text=True
        ).stdout.splitlines()
        latest_tag = tags[0] if tags else ""
        if latest_tag == tag:
            error_message = f"Tag '{tag}' already exists. Exit the program."
            sys.exit(error_message)
    except subprocess.CalledProcessError as e:
        error_code = e.returncode
        error_output = e.stderr
        print(f"error_code:{error_code}")
        print(f"error_output:{error_output}")
        latest_tag = ""
        error_message = "No tags found. Exit the program."
        sys.exit(error_message)
    return latest_tag


def poetry_project_version_checker(new_tag):
    # print('update_pyproject_toml()')
    new_ver = new_tag.replace("v", "")
    try:
        # pyproject.tomlファイルの読み込み
        toml = TOMLFile("../pyproject.toml")
        toml_data = toml.read()
        toml_get_data = toml_data.get('tool')
        # バージョンの更新
        curent_ver = toml_get_data['poetry']['version']
        if curent_ver <= new_ver:
            toml_get_data['poetry']['version'] = new_ver
        else:
            error_message = f"The specified tag '{new_ver}' must be greater than the latest tag 'v{curent_ver}'. Exit the program."
            sys.exit(error_message)
    except Exception as e:
        error_message = f"Failed to update pyproject.toml. Error: {str(e)}"
        sys.exit(error_message)
    return toml_data


def get_arg():
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
        new_tag = None
    return new_tag


def create_tag(new_tag, latest_tag):
    create_tag_flag = False
    # print('create_tag()')
    if not latest_tag:
        print("not latest_tag. set v0.1.0.")
        # タグが存在しない場合、初期バージョンを設定する
        if not new_tag:
            new_tag = "v0.1.0"
        create_tag_flag = True
    else:
        # タグのバージョンを分割する
        tag_version = latest_tag[1:] if latest_tag.startswith("v") else latest_tag
        major, minor, patch = map(int, tag_version.split("."))

        # 引数が指定された場合、引数のバージョンを使用する
        if len(sys.argv) > 1:
            new_tag = sys.argv[1]
            create_tag_flag = True
            if new_tag.replace("v", "") < tag_version:
                create_tag_flag = False
                error_message = f"The specified tag '{new_tag}' must be greater than the latest tag 'v{tag_version}'. Exit the program."
                sys.exit(error_message)
        else:
            # タグのバージョンをインクリメント
            if patch < 999:
                patch += 1
            elif minor < 999:
                minor += 1
                patch = 0
            else:
                major += 1
                minor = 0
                patch = 0
            new_tag = f"v{major}.{minor}.{patch}"
            create_tag_flag = True
    return create_tag_flag, new_tag


if __name__ == "__main__":  # pragma: no cover
    remote_to_check = "origin"
    new_tag = get_arg()
    latest_tag_remote = remote_tag_checker(remote_to_check, new_tag)
    latest_tag_local = local_tag_checker(new_tag)
    create_tag_flag, new_tag = create_tag(new_tag, latest_tag_local)
    # 新しいタグを作成する
    if create_tag_flag:
        subprocess.run(["git", "tag", new_tag])
