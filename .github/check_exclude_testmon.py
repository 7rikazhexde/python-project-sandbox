import json
import os


def main() -> None:
    # GitHub Actionsの環境変数からデータを取得
    exclude_testmon_json_str = os.getenv("EXCLUDE_TESTMON_JSON")

    # Noneのチェック。Noneなら空のリストとして扱う。
    if exclude_testmon_json_str is None:
        exclude_testmon_json_str = "[]"

    current_os = os.getenv("CURRENT_OS")
    current_python_version = os.getenv("CURRENT_PYTHON_VERSION")

    # JSONのパース
    try:
        exclude_testmon_json = json.loads(exclude_testmon_json_str)
    except json.JSONDecodeError:
        print("Invalid JSON format. Skipping tests.")
        print("::set-output name=skip_tests::false")
        return

    # テストをスキップするかどうか判定
    skip_tests = False
    for entry in exclude_testmon_json:
        if (
            entry["os"] == current_os
            and entry["python_version"] == current_python_version
        ):
            skip_tests = True
            break

    # GitHub Actionsの出力に反映
    if skip_tests:
        print(
            f"This combination is in the exclude list: OS={current_os}, Python={current_python_version}. Skipping tests."
        )
        print("::set-output name=skip_tests::true")
    else:
        print(
            f"This combination is not in the exclude list: OS={current_os}, Python={current_python_version}. Running tests."
        )
        print("::set-output name=skip_tests::false")


if __name__ == "__main__":
    main()
