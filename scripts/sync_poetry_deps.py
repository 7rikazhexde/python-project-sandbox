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

    # そのまま返す（既に>=, ==, <=などを使用している場合）
    return version_str


def sync_dependencies() -> None:
    """[tool.poetry.group.dev.dependencies]から[project.optional-dependencies]を生成する"""
    with open("pyproject.toml", "r", encoding="utf-8") as f:
        content = f.read()

    # tomlkitでパース
    pyproject = tomlkit.parse(content)

    # Poetry開発依存関係がある場合
    poetry_deps: Optional[Dict[str, Any]] = (
        pyproject.get("tool", {})
        .get("poetry", {})
        .get("group", {})
        .get("dev", {})
        .get("dependencies")
    )
    if poetry_deps:
        dev_deps = poetry_deps

        # [project]セクションがなければ作成
        if "project" not in pyproject:
            pyproject["project"] = tomlkit.table()

        # [project.optional-dependencies]セクションがなければ作成
        if "optional-dependencies" not in pyproject["project"]:
            pyproject["project"]["optional-dependencies"] = tomlkit.table()

        # 新しいdevセクションを作成（配列形式で一行ずつ追加する）
        pyproject["project"]["optional-dependencies"]["dev"] = tomlkit.array()
        dev_array = pyproject["project"]["optional-dependencies"]["dev"]

        # 各依存関係を配列の要素として追加
        for package, version in dev_deps.items():
            pep621_version = convert_poetry_version_to_pep621(str(version))
            entry = f"{package}{pep621_version}"
            dev_array.append(entry)
            dev_array.multiline(True)  # 複数行フォーマットを有効化

        print("開発依存関係を[project.optional-dependencies]に同期しました。")
    else:
        print("警告: [tool.poetry.group.dev.dependencies]セクションが見つかりません。")

    # 結果を書き込み
    with open("pyproject.toml", "w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(pyproject))


if __name__ == "__main__":
    sync_dependencies()
