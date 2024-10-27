#!/bin/bash

# matrix.jsonファイルから直接読み込む場合
# os_list=$(jq -r '.os[]' matrix.json | tr '\n' ' ' | sed 's/ $//')

# あるいは、GitHub Actionsの出力形式の文字列から読み込む場合（Show matrixステップの出力形式に基づく）
os='["ubuntu-latest","windows-latest","macos-latest"]'  # GitHub Actionsから渡される形式

# JSON形式の文字列から配列を作成
os_list=$(echo "$os" | jq -r '.[]' | tr '\n' ' ' | sed 's/ $//')

# 結果を確認
echo "Original JSON string: $os"
echo "Transformed os_list: $os_list"
echo -e "\nTesting in for loop:"

for os in $os_list; do
    echo "Current OS: $os"
done
