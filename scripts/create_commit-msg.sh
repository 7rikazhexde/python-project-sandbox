#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

create_commit_msg() {
    cat > "$1" << EOF
#!/usr/bin/env bash

commit_msg_file="\$1"
commit_msg=\$(cat "\$commit_msg_file")

# :bookmark:タグがある場合、バージョンを更新
if [[ \$commit_msg == *":bookmark:"* ]]; then
    source "$SCRIPT_DIR/../.venv/bin/activate"
    poetry run python "$SCRIPT_DIR/../ci/update_pyproject_version.py"
    if [ \$? -eq 0 ]; then
        git add pyproject.toml
    else
        echo "Failed to update version. Please check the error and try again."
        exit 1
    fi
fi

# デフォルトで:bookmark:タグを追加（既に含まれている場合は追加しない）
if [[ \$commit_msg != *":bookmark:"* ]]; then
    echo -e "\n:bookmark:" >> "\$commit_msg_file"
    echo "Default :bookmark: tag added. Remove it if version update is not needed."
fi
EOF

    if [ "$2" == "execute" ]; then
        chmod +x "$1"
        echo "$1 created with execution permission."
    else
        echo "$1 created."
    fi
}

if [ -f "$SCRIPT_DIR/../.git/hooks/commit-msg" ]; then
    read -p "$SCRIPT_DIR/../.git/hooks/commit-msg already exists. Do you want to create $SCRIPT_DIR/../.git/hooks/commit-msg.second instead? (y/N): " choice
    if [[ $choice == "y" || $choice == "Y" ]]; then
        create_commit_msg "$SCRIPT_DIR/../.git/hooks/commit-msg.second"
        exit 0
    else
        create_commit_msg "$SCRIPT_DIR/../.git/hooks/commit-msg" "execute"
        exit 0
    fi
fi

create_commit_msg "$SCRIPT_DIR/../.git/hooks/commit-msg" "execute"
exit 0
