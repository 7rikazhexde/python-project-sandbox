#!../../.venv/bin/python3

import re
import sys

from tomlkit.toml_file import TOMLFile


def update_pyproject_toml(new_tag):
    # print('update_pyproject_toml()')
    try:
        # pyproject.tomlファイルの読み込み
        toml = TOMLFile("../../pyproject.toml")
        toml_data = toml.read()
        toml_get_data = toml_data.get('tool')

        # バージョンの更新
        toml_get_data['poetry']['version'] = new_tag

        # pyproject.tomlファイルの書き込み
        toml.write(toml_data)
    except Exception as e:
        error_message = f"Failed to update pyproject.toml. Error: {str(e)}"
        sys.exit(error_message)


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


if __name__ == "__main__":
    new_tag = get_arg()
    if new_tag is None:
        error_message = (
            "Invalid tag format. Please enter in [vx.x.x]. Exit the program."
        )
        sys.exit(error_message)
    update_pyproject_toml(new_tag.replace("v", ""))
