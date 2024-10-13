import json
import os
import sys


def main() -> None:
    # GitHub Actionsの環境変数からデータを取得
    updated_testmon_json_str = os.getenv("UPDATED_TESTMON_JSON")

    # Noneのチェック。Noneならワークフローを中止する。
    if not updated_testmon_json_str:
        print("updated_testmon_json is empty. Stopping workflow.")
        sys.exit(1)

    current_os = os.getenv("CURRENT_OS")
    current_python_version = os.getenv("CURRENT_PYTHON_VERSION")

    # JSONのパース
    try:
        updated_testmon_json = json.loads(updated_testmon_json_str)
    except json.JSONDecodeError:
        print("Invalid JSON format. Stopping workflow.")
        sys.exit(1)

    # updated_testmon_jsonが空の場合、ワークフローを中止
    if not updated_testmon_json:
        print("No test targets found in updated_testmon_json. Stopping workflow.")
        sys.exit(1)

    # テストを実行するかどうか判定
    skip_tests = True
    for entry in updated_testmon_json:
        if (
            entry["os"] == current_os
            and entry["python_version"] == current_python_version
        ):
            skip_tests = False
            break

    # GitHub Actionsの出力に反映
    if skip_tests:
        print(
            f"This combination is not in the test target list: OS={current_os}, Python={current_python_version}. Skipping tests."
        )
        set_github_output("skip_tests", "true")
    else:
        print(
            f"This combination is in the test target list: OS={current_os}, Python={current_python_version}. Running tests."
        )
        set_github_output("skip_tests", "false")


def set_github_output(name: str, value: str) -> None:
    """GitHub Actionsの環境ファイルを使って出力を設定"""
    github_output = os.getenv("GITHUB_OUTPUT")
    if github_output is None:
        print("GITHUB_OUTPUT is not set. Unable to set output.")
        sys.exit(1)

    with open(github_output, "a") as fh:
        print(f"{name}={value}", file=fh)


if __name__ == "__main__":
    main()
