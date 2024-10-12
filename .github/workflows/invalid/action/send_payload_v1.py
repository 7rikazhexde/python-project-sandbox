import os
import subprocess
from typing import Dict, List, Union

# 環境変数やリストをまとめて定義
data: Dict[str, Union[str, List[str]]] = {
    "repository_name": os.getenv(
        "REPOSITORY_NAME", "7rikazhexde/python-project-sandbox"
    ),
    "ghpages_branch": os.getenv("GHPAGES_BRANCH", "gh_pages"),
    "os_list": os.getenv("OS_LIST", "ubuntu-latest macos-13 windows-latest").split(),
    "python_versions": os.getenv("PYTHON_VERSIONS", "3.11 3.12").split(),
}


# ペイロードを作成する関数
def build_payload(data_dict: Dict[str, Union[str, List[str]]]) -> str:
    payload_cmd = []
    payload_cmd.append(f"gh api repos/{data_dict['repository_name']}/dispatches")
    payload_cmd.append("-f event_type=test_pytest-testmon_deploy_multi_os")

    for key, value in data_dict.items():
        if isinstance(value, list):
            for item in value:
                payload_cmd.append(f"-f client_payload[{key}][]={item}")
        elif key != "repository_name":  # repository_nameはすでに使っているためスキップ
            payload_cmd.append(f"-f client_payload[{key}]={value}")

    return " ".join(payload_cmd)


# コマンドを生成
command: str = build_payload(data)

# コマンドの確認と実行
print(f"Executing command: {command}")
subprocess.run(command, shell=True, check=True)
