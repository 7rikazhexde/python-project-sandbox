import json
import os
import sys
from typing import Any, Dict


def set_github_output(name: str, value: str) -> None:
    """GitHub Actionsの環境ファイルを使って出力を設定"""
    github_output = os.getenv("GITHUB_OUTPUT")
    if github_output is None:
        print("GITHUB_OUTPUT is not set. Unable to set output.")
        sys.exit(1)

    # ファイルの存在を確認し、存在しない場合はエラーメッセージを表示
    if not os.path.exists(github_output):
        print(f"Error: The GITHUB_OUTPUT file at {github_output} does not exist.")
        sys.exit(1)

    with open(github_output, "a") as fh:
        fh.write(f"{name}={value}\n")
        fh.flush()  # デバッグのため、書き込み後にフラッシュ
        print(
            f"Debug: Written to GITHUB_OUTPUT -> {name}={value}"
        )  # デバッグ情報の追加

    # GITHUB_ENVを利用して環境変数としても設定
    github_env = os.getenv("GITHUB_ENV")
    if github_env:
        with open(github_env, "a") as env_file:
            env_file.write(f"{name}={value}\n")
            print(
                f"Debug: Written to GITHUB_ENV -> {name}={value}"
            )  # デバッグ情報の追加


def parse_json(
    data: Any,
    prefix: str = "",
    debug: bool = False,
) -> None:
    """
    JSONデータを再帰的に探索し、デバッグモードなら標準出力に表示、
    通常モードならGITHUB_OUTPUTに書き込む。

    :param data: JSON形式の辞書データ
    :param prefix: 環境変数名に付加するプレフィックス（ネストされた辞書対応）
    :param debug: デバッグモードの有無
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                # ネストされた辞書やリストを再帰的に処理
                parse_json(value, prefix + key.upper() + "_", debug)
            else:
                # その他の単一の値をそのまま表示または書き込む
                output = f"{prefix}{key.upper()}={value}"
                if debug:
                    print(output)
                else:
                    print(
                        f"Debug: Processing key={prefix + key.upper()} value={value}"
                    )  # デバッグ情報の追加
                    set_github_output(prefix + key.upper(), str(value))
    elif isinstance(data, list):
        # リストはJSON形式で表示または書き込む
        list_values = json.dumps(data)
        output = f"{prefix[:-1]}={list_values}"  # 最後の不要なアンダースコアを削除
        if debug:
            print(output)
        else:
            print(
                f"Debug: Processing list prefix={prefix[:-1]} value={list_values}"
            )  # デバッグ情報の追加
            set_github_output(prefix[:-1], list_values)
        # リスト内の辞書を個別に処理
        for index, item in enumerate(data):
            if isinstance(item, dict):
                parse_json(item, prefix + f"{index}_", debug)
            else:
                output = f"{prefix}{index}={item}"
                if debug:
                    print(output)
                else:
                    print(
                        f"Debug: Processing list item prefix={prefix + str(index)} value={item}"
                    )  # デバッグ情報の追加
                    set_github_output(prefix + str(index), str(item))


if __name__ == "__main__":
    # コマンドライン引数からJSONファイルのパスとオプションを取得
    json_file: str = sys.argv[1]
    debug = "--debug" in sys.argv

    # JSONファイルの読み込み
    with open(json_file, "r") as f:
        data: Dict[str, Any] = json.load(f)

    # JSONデータの解析とGITHUB_OUTPUTへの書き出し（デバッグモードなら標準出力に表示）
    parse_json(data, debug=debug)
