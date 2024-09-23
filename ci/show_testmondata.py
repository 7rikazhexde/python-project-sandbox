import sqlite3
import sys
from pathlib import Path
from typing import Any, List, Tuple

# プロジェクトのルートディレクトリを取得
project_root: Path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

# .testmondataファイルのパスを設定
testmondata_path: Path = project_root / ".testmondata"

# ファイルが存在するか確認
if not testmondata_path.exists():
    print(f"Error: {testmondata_path} does not exist.")
    sys.exit(1)

conn: sqlite3.Connection | None = None
try:
    conn = sqlite3.connect(str(testmondata_path))
    cursor: sqlite3.Cursor = conn.cursor()

    # テーブルの一覧を取得
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables: List[Tuple[str]] = cursor.fetchall()
    print("Tables:", tables)

    # 各テーブルの内容を表示
    for table in tables:
        print(f"\nContents of {table[0]}:")
        cursor.execute(f"SELECT * FROM {table[0]}")
        rows: List[Tuple[Any, ...]] = cursor.fetchall()
        for row in rows:
            print(row)

except sqlite3.Error as e:
    print(f"An error occurred: {e}")

finally:
    if conn:
        conn.close()
