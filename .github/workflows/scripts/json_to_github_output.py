import json
import os
import sys
from typing import Any, Dict, Optional, TextIO


def parse_json(
    data: Any,
    prefix: str = "",
    debug: bool = False,
    output_file: Optional[TextIO] = None,
) -> None:
    """
    JSONデータを再帰的に探索し、デバッグモードなら標準出力に表示、
    通常モードならGITHUB_OUTPUTに書き込む。

    :param data: JSON形式の辞書データ
    :param prefix: 環境変数名に付加するプレフィックス（ネストされた辞書対応）
    :param debug: デバッグモードの有無
    :param output_file: GITHUB_OUTPUT用のファイルオブジェクト
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                # ネストされた辞書やリストを再帰的に処理
                parse_json(value, prefix + key.upper() + "_", debug, output_file)
            else:
                # その他の単一の値をそのまま表示または書き込む
                if debug:
                    print(f"{prefix}{key.upper()}={value}")
                elif output_file:
                    print(
                        f"Writing to GITHUB_OUTPUT: {prefix}{key.upper()}={value}"
                    )  # デバッグ用
                    output_file.write(f"{prefix}{key.upper()}={value}\n")
    elif isinstance(data, list):
        # リストはJSON形式で表示または書き込む
        list_values = json.dumps(data)
        if debug:
            print(f"{prefix[:-1]}={list_values}")  # 最後の不要なアンダースコアを削除
        elif output_file:
            print(
                f"Writing to GITHUB_OUTPUT: {prefix[:-1]}={list_values}"
            )  # デバッグ用
            output_file.write(f"{prefix[:-1]}={list_values}\n")
        # リスト内の辞書を個別に処理
        for index, item in enumerate(data):
            if isinstance(item, dict):
                parse_json(item, prefix + f"{index}_", debug, output_file)
            else:
                if debug:
                    print(f"{prefix}{index}={item}")
                elif output_file:
                    print(
                        f"Writing to GITHUB_OUTPUT: {prefix}{index}={item}"
                    )  # デバッグ用
                    output_file.write(f"{prefix}{index}={item}\n")


if __name__ == "__main__":
    # コマンドライン引数からJSONファイルのパスとオプションを取得
    json_file: str = sys.argv[1]
    debug = "--debug" in sys.argv

    # デバッグモードでない場合、GITHUB_OUTPUTを取得
    output_file: Optional[TextIO] = None
    if not debug:
        github_output = os.getenv("GITHUB_OUTPUT")
        if not github_output:
            raise ValueError("GITHUB_OUTPUT environment variable is not set.")
        output_file = open(github_output, "a")

    # JSONファイルの読み込み
    with open(json_file, "r") as f:
        data: Dict[str, Any] = json.load(f)

    # JSONデータの解析とGITHUB_OUTPUTへの書き出し（デバッグモードなら標準出力に表示）
    parse_json(data, debug=debug, output_file=output_file)

    # ファイルが開かれていれば閉じる
    if output_file:
        output_file.close()
