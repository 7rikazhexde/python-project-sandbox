#!/usr/bin/env python3
from typing import Any, Dict, Optional

import tomlkit


def convert_poetry_version_to_pep621(version_str: str) -> str:
    """Poetryのバージョン指定形式をPEP 621形式に変換する"""
    # ^4.2.0 -> >=4.2.0
    if version_str.startswith("^"):
        version = version_str[1:]
        return f">={version}"
    # ~4.2.0 -> >=4.2.0
    elif version_str.startswith("~"):
        version = version_str[1:]
        return f">={version}"
    # バージョン指定子がない場合（例: "0.11.5"）
    elif version_str and not any(
        op in version_str for op in [">=", "<=", "==", ">", "<", "!="]
    ):
        return f"=={version_str}"

    # そのまま返す（既に>=, ==, <=などを使用している場合）
    return version_str


def sync_dependencies() -> None:
    """
    Poetry依存関係からPEP 621依存関係を同期する
    1. [tool.poetry.dependencies] -> [project.dependencies]
    2. [tool.poetry.group.dev.dependencies] -> [project.optional-dependencies.dev]
    """
    with open("pyproject.toml", "r", encoding="utf-8") as f:
        content = f.read()

    # tomlkitでパース
    pyproject = tomlkit.parse(content)

    # [project]セクションがなければ作成
    if "project" not in pyproject:
        pyproject["project"] = tomlkit.table()

    # Python依存関係を最初にチェック
    python_dep = None
    poetry_section = pyproject.get("tool", {}).get("poetry", {})

    # Poetryセクションのpython依存関係をチェック
    poetry_deps = poetry_section.get("dependencies", {})
    if "python" in poetry_deps:
        python_dep = str(poetry_deps["python"])
        # requires-pythonを設定
        if python_dep.startswith("^"):
            # ^3.11 -> >=3.11,<4.0
            pyproject["project"]["requires-python"] = (
                f">={python_dep[1:]},<{int(python_dep[1:].split('.')[0]) + 1}.0"
            )
        else:
            pyproject["project"]["requires-python"] = convert_poetry_version_to_pep621(
                python_dep
            )
        print(
            f"Python依存関係 {python_dep} を[project.requires-python]に同期しました: {pyproject['project']['requires-python']}"
        )

    # 1. メイン依存関係の同期
    main_deps: Optional[Dict[str, Any]] = poetry_deps

    if main_deps:
        # 依存関係セクションがなければ作成
        if "dependencies" not in pyproject["project"]:
            pyproject["project"]["dependencies"] = tomlkit.array()

        # 配列形式を維持するために、複数行フォーマットを有効化
        deps_array = pyproject["project"]["dependencies"]
        # tomlkit.itemsは独自のメソッドを持っているので、型チェックを行う
        if not hasattr(deps_array, "multiline"):
            # 通常のPythonリストの場合、tomlkitの配列に変換
            new_array = tomlkit.array()
            new_array.multiline(True)
            deps_array = new_array
        else:
            deps_array.clear()
            # 明示的に複数行フォーマットを設定
            deps_array.multiline(True)

        # 各依存関係を配列の要素として追加（pythonは除く）
        for package, version in main_deps.items():
            if package != "python":  # pythonはrequires-pythonで処理済み
                pep621_version = convert_poetry_version_to_pep621(str(version))
                entry = f"{package}{pep621_version}"
                deps_array.append(entry)

        # 依存関係を設定
        pyproject["project"]["dependencies"] = deps_array

        print("メイン依存関係を[project.dependencies]に同期しました。")
    else:
        print("警告: [tool.poetry.dependencies]セクションが見つかりません。")

    # 2. 開発依存関係の同期
    dev_deps: Optional[Dict[str, Any]] = (
        pyproject.get("tool", {})
        .get("poetry", {})
        .get("group", {})
        .get("dev", {})
        .get("dependencies")
    )

    if dev_deps:
        # [project.optional-dependencies]セクションがなければ作成
        if "optional-dependencies" not in pyproject["project"]:
            pyproject["project"]["optional-dependencies"] = tomlkit.table()

        # 新しいdevセクションを作成
        dev_array = tomlkit.array()
        dev_array.multiline(True)  # 複数行フォーマットを有効化

        # 各依存関係を配列の要素として追加
        for package, version in dev_deps.items():
            pep621_version = convert_poetry_version_to_pep621(str(version))
            entry = f"{package}{pep621_version}"
            dev_array.append(entry)

        # devセクションを設定
        pyproject["project"]["optional-dependencies"]["dev"] = dev_array

        print("開発依存関係を[project.optional-dependencies.dev]に同期しました。")
    else:
        print("警告: [tool.poetry.group.dev.dependencies]セクションが見つかりません。")

    # 結果を書き込み
    with open("pyproject.toml", "w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(pyproject))


if __name__ == "__main__":
    sync_dependencies()
