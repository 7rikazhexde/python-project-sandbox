#!../../.venv/bin/python3

import re
import subprocess
import sys

from run_git_tag import create_tag, local_tag_checker, remote_tag_checker
from update_pyproject_version_with_git_tag import update_pyproject_toml


def get_arg():
    # print('get_arg()')
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


if __name__ == "__main__":  # pragma: no cover
    remote_to_check = "origin"
    new_tag = get_arg()
    latest_tag_remote = remote_tag_checker(remote_to_check, new_tag)
    latest_tag_local = local_tag_checker(new_tag)
    create_tag_flag, new_tag = create_tag(new_tag, latest_tag_local)

    if create_tag_flag:
        # 新しいタグを作成する
        subprocess.run(["git", "tag", new_tag])

        # pyproject.tomlのバージョンを更新する
        update_pyproject_toml(new_tag.replace("v", ""))
