# pytest-testmon 問題分析と修正計画

## 目次

- [ユーザーの要望と現状](#ユーザーの要望と現状)
- [pytest-testmon の仕組み解析](#pytest-testmon-の仕組み解析)
- [問題の根本原因分析](#問題の根本原因分析)
- [改善案と実装計画](#改善案と実装計画)
- [推奨実装順序](#推奨実装順序)

---

## ユーザーの要望と現状

### 要望

- pytest-testmon を CI 環境（GitHub Actions）で活用したい
- `.testmondata` をアーティファクトまたは GitHub Pages でアップロード/ダウンロードして再利用したい
- 増分テスト実行により CI 時間を短縮したい

### 現在の問題

**`.testmondata` が常に新規作成されてしまう**

ワークフロー構成：

```yaml
# 1. GitHub Pages から .testmondata を取得
git checkout gh-pages -- "testmon-data/{os}/python/{version}/.testmondata"

# 2. テスト実行
pytest --testmon

# 3. アーティファクトとしてアップロード
upload-artifact@v4

# 4. GitHub Pages へデプロイ
git push origin gh-pages
```

しかし、毎回「new DB」として扱われ、全テストが実行されてしまう。

### 対象ワークフロー

- リポジトリ: `https://github.com/7rikazhexde/python-project-sandbox`
- パス: `.github/workflows/test_workflow/test_pytest-testmon_deploy_multi_os.yml`

---

## pytest-testmon の仕組み解析

### 概要

pytest-testmon は、コード変更の影響を受けるテストのみを自動選択して実行する pytest プラグインです。

### コアアーキテクチャ

#### 主要モジュール構成

| モジュール | 役割 | 重要な機能 |
|-----------|------|-----------|
| `pytest_testmon.py` | pytest プラグインのエントリポイント | フック登録、テスト選択/収集の統括 |
| `testmon_core.py` | コア機能 | カバレッジ追跡、TestmonData、TestmonCollector |
| `process_code.py` | コード解析 | AST解析、フィンガープリント生成 |
| `db.py` | データベース層 | SQLite操作、依存関係保存 |
| `configure.py` | 設定管理 | 収集/選択の有効化判定 |
| `common.py` | ユーティリティ | システムパッケージ検出、Git操作 |

#### 動作フロー

```text
1. pytest_configure()
   ↓
2. init_testmon_data() - TestmonData初期化
   ↓
3. TestmonData.__init__()
   ├─ DB接続（.testmondata）
   ├─ initiate_execution() - 実行環境を登録
   └─ determine_stable() - 変更検出
   ↓
4. TestmonSelect.pytest_collection_modifyitems()
   ├─ 安定したテストをdeselect
   └─ 不安定なテストを優先実行
   ↓
5. TestmonCollect.pytest_runtest_protocol()
   ├─ TestmonCollector.start_testmon()
   ├─ Coverage追跡開始
   └─ カバレッジデータ収集
   ↓
6. TestmonData.get_tests_fingerprints()
   ├─ カバレッジからフィンガープリント生成
   └─ 依存関係を構築
   ↓
7. DB.insert_test_file_fps()
   └─ .testmondataに保存
```

### データ構造

#### `.testmondata` (SQLite データベース)

主要テーブル：

- `environment` - 実行環境（OS、Pythonバージョン、パッケージ情報）
- `execution` - 実行履歴
- `test_execution` - テスト実行記録
- `file_fp` - ファイルフィンガープリント
- `test_execution_file_fp` - テストとファイルの依存関係

**重要**: データベースバージョン = `DATA_VERSION = 13` (`db.py:13`)

#### フィンガープリント（Fingerprint）

3段階の変更検出：

1. **mtime** (modification time)
   - ファイルの最終更新時刻
   - 最速のチェック

2. **fsha** (file SHA)
   - Gitブロブ形式のファイルハッシュ
   - `process_code.py:88-99` の `bytes_to_string_and_fsha()`

   ```python
   git_header = b"blob %u\0" % len(byte_string)
   hsh = hashlib.sha1()
   hsh.update(git_header)
   hsh.update(byte_stream)
   ```

3. **method_checksums** (メソッドチェックサム)
   - 各関数/メソッドのCRC32チェックサム
   - `process_code.py:34-39` の `methods_to_checksums()`

   ```python
   def methods_to_checksums(blocks) -> [int]:
       checksums = []
       for block in blocks:
           checksums.append(to_signed(zlib.crc32(block.encode("UTF-8"))))
       return checksums
   ```

### 実行環境の識別

`testmon_core.py:186-194` の `initiate_execution()`:

```python
result = self.db.initiate_execution(
    self.environment,          # --testmon-env または ini設定
    system_packages,           # インストール済みパッケージ一覧
    python_version,            # 例: "3.12.0"
    {
        "tm_client_version": TM_CLIENT_VERSION,  # testmonのバージョン
        "git_head_sha": git_current_head(),      # Git HEAD SHA
        "ci": os.environ.get("CI"),              # CI環境フラグ
    },
)
```

**これらのいずれかが異なると、別の実行環境として扱われます。**

### システムパッケージの追跡

`common.py:76-87` の `get_system_packages()`:

```python
def get_system_packages(ignore=None):
    if not ignore:
        ignore = set(("pytest-testmon", "pytest-testmon"))
    return ", ".join(
        sorted(
            {
                f"{package} {version}"
                for (package, version) in get_system_packages_raw()
                if package not in ignore and package != "UNKNOWN" and version != "0.0.0"
            }
        )
    )
```

`common.py:90-95` の `drop_patch_version()`:

```python
def drop_patch_version(system_packages):
    return re.sub(
        r"\b([\w_-]+\s\d+\.\d+)\.\w+\b",  # (Package M.N).P
        r"\1",                              # Package M.N
        system_packages,
    )
```

例：

- `pytest 8.3.4` → `pytest 8.3`
- `coverage 7.6.1` → `coverage 7.6`

**パッチバージョンは無視されるが、マイナーバージョンは比較される。**

### 新規DBの判定

`testmon_core.py:223-224`:

```python
@property
def new_db(self):
    return self.db.file_created
```

`db.py:63-77`:

```python
def __init__(self, datafile, readonly=False):
    self._readonly = readonly
    file_exists = os.path.exists(datafile)

    connection = connect(datafile, readonly)
    connection, old_format = check_data_version(
        connection, datafile, self.version_compatibility()
    )
    self.con = connection_options(connection)

    if (not file_exists) or old_format:
        self.init_tables()
        self.file_created = True  # ← 新規DBフラグ
    else:
        self.file_created = False
```

`db.py:49-59` の `check_data_version()`:

```python
def check_data_version(connection, datafile, data_version):
    stored_data_version = connection.execute("PRAGMA user_version").fetchone()[0]

    if int(stored_data_version) == data_version:
        return connection, False

    # バージョン不一致 → DBを削除して再作成
    connection.close()
    os.remove(datafile)
    connection = connect(datafile)
    connection = connection_options(connection)
    return connection, True
```

**新規DBになる条件：**

1. ファイルが存在しない
2. データベースバージョンが `DATA_VERSION` と一致しない

---

## 問題の根本原因分析

### 原因1: SQLite WALモードファイルの欠落 ⭐⭐⭐ 最重要

`db.py:30-36` の `connection_options()`:

```python
def connection_options(connection):
    connection.execute("PRAGMA journal_mode = WAL")  # ← WALモード有効化
    connection.execute("PRAGMA synchronous = OFF")
    connection.execute("PRAGMA foreign_keys = TRUE ")
    connection.execute("PRAGMA recursive_triggers = TRUE ")
    connection.row_factory = sqlite3.Row
    return connection
```

**問題点：**

SQLite の WAL (Write-Ahead Logging) モードでは、以下の3つのファイルが作成されます：

```text
.testmondata       # メインデータベースファイル
.testmondata-wal   # Write-Ahead Logファイル
.testmondata-shm   # 共有メモリファイル
```

現在のワークフローでは `.testmondata` のみをアップロード/ダウンロードしています。

**影響：**

- WAL ファイルなしで `.testmondata` を開くと、最新のトランザクションが失われる可能性
- データベースの整合性が保証されない
- 場合によっては破損と判断され、新規作成される

**検証方法：**

```bash
# ワークフロー実行後
ls -la .testmondata*
# .testmondata-wal と .testmondata-shm が存在するか確認
```

### 原因2: システムパッケージの変更検出

`testmon_core.py:186-209`:

```python
system_packages = get_system_packages(ignore=ignore_dependencies)

result = self.db.initiate_execution(
    self.environment,
    system_packages,  # ← この文字列が完全一致する必要がある
    python_version,
    {...}
)
```

**問題点：**

CI 環境では以下の理由でパッケージ情報が変動する可能性：

1. **インストール順序の違い**
   - `sorted()` で並び替えているが、環境再構築時に微妙に異なる可能性

2. **依存パッケージのバージョン変動**
   - Poetry/pip がロックファイルの範囲内でバージョンを選択
   - 例: `certifi 2024.2.2` → `certifi 2024.7.4`

3. **CI提供パッケージの更新**
   - GitHub Actions ランナーにプリインストールされているパッケージの更新

**影響：**

```python
self.system_packages_change = result["packages_changed"]
```

`pytest_testmon.py:306-312`:

```python
message += (
    "The packages installed in your Python environment have been changed. "
    "All tests have to be re-executed. "
    if packages_change
    else f"changed files: {changed_files_msg}, ..."
)
```

パッケージ変更と判断されると、**すべてのテストが実行される**。

### 原因3: 環境識別子の不一致

`testmon_core.py:142-144`:

```python
environment = config.getoption("environment_expression") or eval_environment(
    config.getini("environment_expression")
)
```

デフォルトは `"default"` (`testmon_core.py:170`)。

**問題点：**

異なるマトリックス実行（OS × Python バージョン）で同じ `environment = "default"` を使用すると：

- Ubuntu Python 3.12 のデータ
- macOS Python 3.13 のデータ

が同じ環境として扱われてしまう可能性があります。

逆に、環境識別子を設定していない場合、同じ OS × Python バージョンでも、他の要因（Git SHA など）で別環境と判断される可能性もあります。

### 原因4: 条件付きアップロードによるデータ損失

ワークフローの条件：

```yaml
if: steps.pytest-testmon.outputs.tests_executed == 'true'
```

**問題点：**

- テストが1つも実行されなかった場合、アップロードされない
- 次回実行時にデータが失われる
- 選択的テスト実行の恩恵を受けられない

### 原因5: データベースバージョンの不一致（可能性は低い）

`db.py:13`:

```python
DATA_VERSION = 13
```

**問題点：**

- アップロードした環境とダウンロードした環境で `pytest-testmon` のバージョンが異なる
- データベーススキーマが変更されている

**可能性は低いですが、確認が必要です。**

---

## 改善案と実装計画

### 改善案1: SQLite WALチェックポイントの実行 ⭐⭐⭐ 最重要

**目的:** WAL ファイルの内容をメインファイルに統合し、単一ファイルで完全なデータベースを保持

**実装箇所:** `test_pytest-testmon_deploy_multi_os.yml`

#### ステップ1: テスト実行後にチェックポイント実行

```yaml
- name: Run pytest with testmon
  id: pytest-testmon
  run: |
    poetry run pytest --testmon -v
  continue-on-error: true

- name: Checkpoint testmon database
  if: always()  # テスト成功/失敗に関わらず実行
  run: |
    # WALファイルの内容をメインファイルに書き込む
    if [ -f .testmondata ]; then
      sqlite3 .testmondata "PRAGMA wal_checkpoint(TRUNCATE);"
      echo "✓ WAL checkpoint completed"

      # WALファイルを削除（既にメインファイルに統合済み）
      rm -f .testmondata-wal .testmondata-shm
      echo "✓ WAL files removed"

      # ファイルサイズ確認
      ls -lh .testmondata
    else
      echo "⚠ .testmondata not found"
    fi
  continue-on-error: true
```

**WAL チェックポイントの種類:**

- `PASSIVE`: デフォルト、他の接続に影響しない
- `FULL`: 可能な限りWALをメインファイルに書き込む
- `RESTART`: FULLの後、WALをリセット
- `TRUNCATE`: RESTARTの後、WALファイルを0バイトに切り詰め（推奨）

#### ステップ2: アーティファクトパスの調整

```yaml
- name: Copy testmon data to organized path
  if: always()
  run: |
    mkdir -p testmon-data/${{ matrix.os }}/python/${{ matrix.python-version }}
    if [ -f .testmondata ]; then
      cp .testmondata testmon-data/${{ matrix.os }}/python/${{ matrix.python-version }}/
      echo "✓ Copied .testmondata"
    fi

- name: Upload testmon data
  uses: actions/upload-artifact@v4.4.3
  if: always()  # 条件を削除
  with:
    name: testmon-data_${{ matrix.os }}_python_${{ matrix.python-version }}
    path: testmon-data/${{ matrix.os }}/python/${{ matrix.python-version }}/.testmondata
    if-no-files-found: warn
    retention-days: 1
```

### 改善案2: 環境識別子の明示的設定 ⭐⭐ 強く推奨

**目的:** OS × Python バージョンごとに独立した環境として管理

**実装箇所:** `test_pytest-testmon_deploy_multi_os.yml`

```yaml
- name: Run pytest with testmon
  id: pytest-testmon
  run: |
    # 環境識別子を明示的に設定
    ENV_ID="${{ matrix.os }}-py${{ matrix.python-version }}"
    echo "Environment ID: $ENV_ID"

    poetry run pytest --testmon \
      --testmon-env "$ENV_ID" \
      -v
  continue-on-error: true
```

**効果:**

- `environment` が `"ubuntu-latest-py3.12"` のように明確に識別される
- 異なる環境のデータが混在しない
- 同じ環境では常に同じデータベースを参照

### 改善案3: システムパッケージ変更の無視設定 ⭐

**目的:** CI 環境で変動しやすいパッケージを無視して、コード変更のみに焦点を当てる

#### オプション3-1: pyproject.toml で設定

`pyproject.toml` に追加:

```toml
[tool.pytest.ini_options]
testmon_ignore_dependencies = [
    "setuptools",
    "pip",
    "wheel",
    "certifi",
    "charset-normalizer",
    "urllib3",
    "idna",
    "requests",
    # CI環境で頻繁に更新されるパッケージ
]
```

#### オプション3-2: pytest.ini で設定

`pytest.ini` を作成:

```ini
[pytest]
testmon_ignore_dependencies =
    setuptools
    pip
    wheel
    certifi
    charset-normalizer
```

#### オプション3-3: すべてのパッケージを無視（非推奨だが検証用）

一時的に、パッケージ変更を完全に無視する場合：

```yaml
- name: Run pytest with testmon (ignore all packages)
  run: |
    # 環境変数で全パッケージを無視
    # 注意: これは検証用のみ、本番では使用しない
    poetry run pytest --testmon -v
  env:
    TESTMON_IGNORE_ALL_PACKAGES: "1"  # カスタム実装が必要
```

**注意:** この機能は現在の pytest-testmon には存在しないため、実装が必要です。

### 改善案4: GitHub Actions キャッシュの活用 ⭐⭐

**目的:** アーティファクトの1日保持制限を回避し、より永続的なキャッシュを利用

**実装箇所:** `test_pytest-testmon_deploy_multi_os.yml`

```yaml
- name: Restore testmon data from cache
  id: cache-testmon
  uses: actions/cache@v4
  with:
    path: .testmondata
    # キャッシュキー: OS + Pythonバージョン + Git SHA
    key: testmon-${{ matrix.os }}-py${{ matrix.python-version }}-${{ github.sha }}
    restore-keys: |
      testmon-${{ matrix.os }}-py${{ matrix.python-version }}-
      testmon-${{ matrix.os }}-

- name: Fallback to GitHub Pages
  if: steps.cache-testmon.outputs.cache-hit != 'true'
  run: |
    echo "Cache miss, fetching from GitHub Pages..."
    git fetch origin gh-pages:gh-pages || true
    git checkout gh-pages -- "testmon-data/${{ matrix.os }}/python/${{ matrix.python-version }}/.testmondata" || echo "No data in GitHub Pages"

    if [ -f "testmon-data/${{ matrix.os }}/python/${{ matrix.python-version }}/.testmondata" ]; then
      cp "testmon-data/${{ matrix.os }}/python/${{ matrix.python-version }}/.testmondata" .testmondata
      echo "✓ Restored from GitHub Pages"
    fi

# ... pytest実行 ...

- name: Save testmon data to cache
  if: always()
  uses: actions/cache/save@v4
  with:
    path: .testmondata
    key: testmon-${{ matrix.os }}-py${{ matrix.python-version }}-${{ github.sha }}
```

**メリット:**

- キャッシュは7日間保持（アーティファクトの1日より長い）
- 復元が高速
- `restore-keys` により部分一致でも復元可能

**デメリット:**

- キャッシュサイズ制限（10GB/リポジトリ）
- 古いキャッシュは自動削除される

### 改善案5: デバッグ情報の追加 ⭐

**目的:** 問題の根本原因を特定するための詳細なログ出力

**実装箇所:** `test_pytest-testmon_deploy_multi_os.yml`

```yaml
- name: Debug - Check testmon data before test
  run: |
    echo "=== Before Test Execution ==="
    if [ -f .testmondata ]; then
      echo "✓ .testmondata exists"
      ls -lh .testmondata*

      echo ""
      echo "Database version:"
      sqlite3 .testmondata "PRAGMA user_version;" || echo "Failed to read version"

      echo ""
      echo "Environment info:"
      sqlite3 .testmondata "SELECT id, name, python_version FROM environment LIMIT 5;" || true

      echo ""
      echo "Test execution count:"
      sqlite3 .testmondata "SELECT COUNT(*) FROM test_execution;" || true

      echo ""
      echo "File fingerprint count:"
      sqlite3 .testmondata "SELECT COUNT(*) FROM file_fp;" || true
    else
      echo "⚠ .testmondata does NOT exist"
    fi
  continue-on-error: true

- name: Run pytest with testmon (verbose)
  id: pytest-testmon
  run: |
    poetry run pytest --testmon -vv  # -vv で詳細出力
  continue-on-error: true

- name: Debug - Check testmon data after test
  if: always()
  run: |
    echo "=== After Test Execution ==="
    if [ -f .testmondata ]; then
      echo "✓ .testmondata exists"
      ls -lh .testmondata*

      echo ""
      echo "WAL files:"
      ls -lh .testmondata-wal .testmondata-shm 2>/dev/null || echo "No WAL files"

      echo ""
      echo "Latest execution:"
      sqlite3 .testmondata "SELECT * FROM execution ORDER BY id DESC LIMIT 1;" || true
    else
      echo "⚠ .testmondata does NOT exist after test"
    fi
  continue-on-error: true
```

**出力される情報:**

- データベースファイルの存在確認
- ファイルサイズ
- データベースバージョン（DATA_VERSION）
- 環境レコード数
- テスト実行レコード数
- ファイルフィンガープリント数
- WAL ファイルの有無

### 改善案6: pytest-testmon のバージョン固定 ⭐

**目的:** データベーススキーマの予期しない変更を防ぐ

**実装箇所:** `pyproject.toml`

```toml
[tool.poetry.dependencies]
python = "^3.12"
pytest = "^8.0"
pytest-testmon = "2.1.4"  # バージョンを固定
# または
pytest-testmon = "~2.1.0"  # パッチバージョンのみ更新許可
```

**理由:**

- `DATA_VERSION` が変更されると既存データベースが使えなくなる
- マイナーバージョンアップでスキーマ変更の可能性
- CI 環境でバージョンを統一

### 改善案7: カスタムパッケージフィルタリング（高度）

**目的:** CI 環境で変動するパッケージを自動的に除外

**実装方法:** pytest プラグインを作成

`conftest.py` に追加:

```python
import pytest
from testmon.common import get_system_packages_raw

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # CI環境でのみ適用
    if os.environ.get("CI"):
        # 変動しやすいパッケージを無視
        volatile_packages = {
            "setuptools", "pip", "wheel",
            "certifi", "charset-normalizer",
            "urllib3", "idna", "requests",
        }

        # testmon_ignore_dependencies を動的に設定
        existing = set(config.getini("testmon_ignore_dependencies"))
        config.option.testmon_ignore_dependencies = list(
            existing | volatile_packages
        )
```

**注意:** これは高度な方法で、テストが必要です。

---

## 推奨実装順序

### フェーズ1: 問題の特定（デバッグ）

1. **改善案5を実装** - デバッグ情報の追加
   - 現状の問題を可視化
   - どの原因が実際に発生しているか確認

2. **ブランチ作成**

   ```bash
   git checkout -b feature/fix-testmondata-persistence
   ```

3. **デバッグワークフロー実行**
   - `.github/workflows/test_workflow/test_pytest-testmon_deploy_multi_os.yml` を編集
   - プッシュして実行
   - ログを確認

### フェーズ2: 基本修正

4. **改善案1を実装** - WAL チェックポイント

   - 最も可能性が高い原因に対処
   - チェックポイント処理を追加
   - アップロード前にWALファイル削除

5. **改善案2を実装** - 環境識別子の設定
   - OS × Python バージョンで環境を明確化
   - `--testmon-env` を追加

6. **ワークフロー実行で検証**
   - 2回目の実行で増分テストが動作するか確認
   - ログで "new DB" が表示されないことを確認

### フェーズ3: 追加の安定化

7. **改善案6を実装** - バージョン固定
   - `pyproject.toml` で pytest-testmon バージョン固定

8. **改善案3を検討** - パッケージ無視設定
   - ログでパッケージ変更が頻繁に発生する場合のみ
   - `pyproject.toml` に設定追加

### フェーズ4: 最適化（オプション）

9. **改善案4を検討** - GitHub Actions キャッシュ
   - より高速なリストアを実現
   - GitHub Pages との二重保存

10. **長期運用での監視**
    - CI 実行時間の短縮を測定
    - テスト選択率を監視

---

## 実装時の注意点

### テスト戦略

1. **小さな変更から開始**
   - 一度に1つの改善案を実装
   - ワークフロー実行で効果を確認

2. **ロールバック計画**
   - ブランチで作業
   - 問題があれば元に戻せるようにする

3. **検証方法**

   ```bash
   # ローカルでテスト
   pytest --testmon -vv

   # 2回目の実行（変更なし）
   pytest --testmon -vv
   # → "changed files: 0" と表示されるはず

   # ファイル変更後
   echo "# comment" >> project_a/some_file.py
   pytest --testmon -vv
   # → 影響を受けるテストのみ実行されるはず
   ```

### ログ確認ポイント

ワークフロー実行時に確認すべきログ：

1. **pytest 出力の先頭**

   ```text
   testmon: changed files: X, unchanged files: Y
   ```

   または

   ```text
   testmon: new DB
   ```

2. **デバッグ出力**
   - データベースバージョン = 13
   - テスト実行レコード数 > 0（2回目以降）
   - WAL ファイルの有無

3. **テスト実行数**
   - 初回: 全テスト実行
   - 2回目（変更なし）: 0個のテスト実行、または失敗したテストのみ
   - 変更後: 影響を受けるテストのみ

### トラブルシューティング

#### 問題: まだ "new DB" と表示される

**確認項目:**

1. WAL チェックポイントが実行されているか
2. `.testmondata` が正しくアップロード/ダウンロードされているか
3. ファイルサイズが 0 バイトでないか
4. SQLite バージョンの互換性

#### 問題: 全テストが実行される

**確認項目:**

1. "packages changed" メッセージが表示されているか
   → 改善案3を実装
2. 環境識別子が一致しているか
   → 改善案2を確認
3. Git HEAD SHA が変わっている場合は正常動作

#### 問題: データベースエラーが発生

**確認項目:**

1. SQLite のバージョン
2. ファイル権限
3. ディスク容量

---

## 補足情報

### pytest-testmon コマンドオプション

```bash
# 基本
pytest --testmon

# 選択のみ無効化（すべてのテストを実行するが優先順位付け）
pytest --testmon-noselect

# 収集のみ無効化（データ更新しない）
pytest --testmon-nocollect

# 強制選択（-k などと併用）
pytest --testmon-forceselect -k "test_name"

# 環境識別子を指定
pytest --testmon --testmon-env "staging"

# 無効化
pytest --no-testmon

# 詳細出力
pytest --testmon -vv
```

### .testmondata の手動確認

```bash
# データベースに接続
sqlite3 .testmondata

# テーブル一覧
.tables

# 環境一覧
SELECT * FROM environment;

# テスト実行数
SELECT COUNT(*) FROM test_execution;

# データベースバージョン
PRAGMA user_version;

# WAL モード確認
PRAGMA journal_mode;

# WAL チェックポイント実行（手動）
PRAGMA wal_checkpoint(TRUNCATE);

# 終了
.quit
```

### 参考リンク

- pytest-testmon GitHub: <https://github.com/tarpas/pytest-testmon>
- pytest-testmon ドキュメント: <https://testmon.org>
- SQLite WAL モード: <https://www.sqlite.org/wal.html>
- GitHub Actions キャッシュ: <https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows>

---

## まとめ

**最も可能性の高い原因:**

1. WAL ファイルの欠落（改善案1で対処）
2. 環境識別子の不統一（改善案2で対処）

**推奨アクション:**

1. デバッグ情報を追加して現状確認
2. WAL チェックポイントを実装
3. 環境識別子を明示的に設定
4. ワークフロー実行で検証

この手順により、`.testmondata` が適切に保持され、CI 環境でも増分テストの恩恵を受けられるようになります。
