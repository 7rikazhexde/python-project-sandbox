import json

# JSONデータをファイルから読み込む
with open("updated_testmon_json.txt", "r") as f:
    updated_testmon_json = f.read()

with open("updated_exclude_testmon_json.txt", "r") as f:
    updated_exclude_testmon_json = f.read()

# JSONデータをパース
try:
    updated_testmon_data = json.loads(updated_testmon_json)
    updated_exclude_testmon_data = json.loads(updated_exclude_testmon_json)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    exit(1)

# OSリストとPythonバージョンを取得
os_list = list({entry["os"] for entry in updated_testmon_data})
python_versions = list({entry["python_version"] for entry in updated_testmon_data})

# ファイルに出力
with open("os_list.txt", "w") as f:
    f.write(",".join(os_list))

with open("python_versions.txt", "w") as f:
    f.write(",".join(python_versions))
