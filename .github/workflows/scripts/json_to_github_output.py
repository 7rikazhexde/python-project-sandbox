import json
import os
import sys
from typing import Any, Dict


def parse_json_to_github_output(data: Dict[str, Any], prefix: str = "") -> None:
    """
    JSONデータを再帰的に探索し、各キーと値をGITHUB_OUTPUTに書き込む。

    :param data: JSON形式の辞書データ
    :param prefix: 環境変数名に付加するプレフィックス（ネストされた辞書対応）
    """
    # GITHUB_OUTPUT 環境変数に出力先が指定されているかを確認
    github_output = os.getenv("GITHUB_OUTPUT")
    if not github_output:
        raise ValueError("GITHUB_OUTPUT environment variable is not set.")

    with open(github_output, "a") as f:
        for key, value in data.items():
            if isinstance(value, dict):
                # ネストされた辞書は再帰的に処理
                parse_json_to_github_output(value, prefix + key.upper() + "_")
            elif isinstance(value, list):
                # リストはカンマ区切りの文字列に変換
                list_values = ",".join(map(str, value))
                f.write(f"{prefix}{key.upper()}={list_values}\n")
            else:
                # その他の単一の値はそのまま書き込む
                f.write(f"{prefix}{key.upper()}={value}\n")


if __name__ == "__main__":
    # コマンドライン引数からJSONファイルのパスを取得
    json_file: str = sys.argv[1]

    # JSONファイルの読み込み
    with open(json_file, "r") as f:
        data: Dict[str, Any] = json.load(f)

    # JSONの解析とGITHUB_OUTPUTへの書き出し
    parse_json_to_github_output(data)
