import os
import subprocess
from typing import Dict, List, Mapping, Union

# サポートされるキー一覧
SUPPORTED_KEYS = {
    "repository_name",
    "event_type",
    "ghpages_branch",
    "os_list",
    "python_versions",
    "custom_param",
}

# スペース区切りの値を持つキーを定数として管理
SPLIT_REQUIRED_KEYS = {"os_list", "python_versions"}

# デフォルト値を持つ変数を個別に定義
DEFAULT_VALUES = {
    "custom_param": "default_value",
    "ghpages_branch": "gh_pages",
}

# 環境変数やリストをまとめて定義
data: Dict[str, Union[str, List[str]]] = {}

# SUPPORTED_KEYS から環境変数を動的に取得
env_vars: Dict[str, Union[str, List[str]]] = {}
for key in SUPPORTED_KEYS:
    # 大文字に変換して環境変数から取得 (例: REPOSITORY_NAME)
    env_var_name = key.upper()
    value = os.getenv(env_var_name)

    # 値が設定されている場合のみ追加
    if value:
        # SPLIT_REQUIRED_KEYS に含まれるキーはスペースで分割してリストに変換
        if key in SPLIT_REQUIRED_KEYS:
            env_vars[key] = value.split()
        # デフォルト値と同じであれば省略
        elif key in DEFAULT_VALUES and value == DEFAULT_VALUES[key]:
            continue  # デフォルト値なら無視
        else:
            env_vars[key] = value


# ペイロードを作成する関数
def build_payload(data_dict: Mapping[str, Union[str, List[str]]]) -> str:
    payload_cmd = []
    payload_cmd.append(f"gh api repos/{data_dict['repository_name']}/dispatches")
    payload_cmd.append(f"-f event_type={data_dict['event_type']}")

    for key, value in data_dict.items():
        if isinstance(value, list):
            for item in value:
                payload_cmd.append(f"-f client_payload[{key}][]={item}")
        # client_payloadで指定する変数ではない場合は、以下で明示的に対象外にすること。
        elif (
            isinstance(value, str) and key != "repository_name" and key != "event_type"
        ):
            payload_cmd.append(f"-f client_payload[{key}]={value}")

    return " ".join(payload_cmd)


# コマンドを生成
try:
    command: str = build_payload(env_vars)
    # コマンドの確認と実行
    print(f"Executing command: {command}")
    subprocess.run(command, shell=True, check=True)
except ValueError as e:
    print(f"Error: {e}")
    exit(1)
