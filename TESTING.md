# テストドキュメント

## 概要

本プロジェクトでは、pytest-testmonによる増分テストを使用して、GitHub Pagesでテストカバレッジレポートを維持しながらCI実行時間を削減しています。

## ワークフロー構成

### メインワークフロー

- **ファイル**: `.github/workflows/test_pytest-testmon_deploy_multi_os.yml`
- **目的**: pytest-testmonによる増分テストと完全なレポート生成
- **トリガー**: mainブランチへのpush

### サポートワークフロー

- **README更新**: `.github/workflows/update_readme_ghpages.yml`
  - ghpagesブランチでテストレポートリンクを自動生成
  - testmonワークフロー完了後にトリガー

### 無効化されたワークフロー

- `test_pytest-html-report_deploy_multi_os.yml` (無効)
- `test_pytest-cov-report_deploy_multi_os.yml` (無効)

これらのワークフローは、タイミング問題を防ぎ一貫性を確保するため、testmonワークフローに統合されました。

## テスト実行動作

### 🎯 初回実行時（testmondataが存在しない場合）

#### ステップ1: testmonの実行

```bash
testmon: new DB, environment: ubuntu-latest-py3.12.9
collected 4 items
tests/calculator/test_operations.py::test_add PASSED
tests/calculator/test_operations.py::test_subtract PASSED
tests/calculator/test_operations.py::test_multiply PASSED
tests/calculator/test_operations.py::test_divide PASSED
✓ tests_executed=true
```

#### ステップ2: 完全なレポート生成

```bash
Generate HTML and Coverage reports
pytest --html=... --cov=project_a ...
collected 4 items
All tests PASSED [100%]
Coverage: 100%
```

#### ステップ3: デプロイ

- `.testmondata` → ghpagesブランチにアップロード
- HTML/Coverageレポート → ghpagesブランチにデプロイ
- レポートリンク付きREADME更新

**結果**: CI時間 約2分、カバレッジ100%のレポート生成 ✅

---

### ✏️ テストケース変更時（追加・削除・修正）

例: test_operations.pyに`test_power`を追加

#### ステップ1: testmonの実行

```bash
testmon: changed files: tests/calculator/test_operations.py
environment: ubuntu-latest-py3.12.9
collected 5 items / 4 deselected / 1 selected
tests/calculator/test_operations.py::test_power PASSED
✓ tests_executed=true (新しいテストが検出された)
```

#### ステップ2: 完全なレポート生成

```bash
pytest --html=... --cov=project_a ...
collected 5 items
All 5 tests PASSED [100%]
Coverage: 100%
```

#### ステップ3: デプロイ

- 更新された`.testmondata` → ghpagesにアップロード
- 新しいHTML/Coverageレポート → ghpagesにデプロイ
- README更新

**結果**: CI時間 約2分、全5テストが実行され、カバレッジ100%のレポート生成 ✅

---

### 🚫 変更なし時（testmondataが最新の場合）

#### ステップ1: testmonの実行

```bash
testmon: changed files: 0, unchanged files: 16
environment: ubuntu-latest-py3.12.9
collected 0 items
no tests ran in 0.02s
✓ tests_executed=false (変更なし)
```

#### ステップ2: レポート生成をスキップ

```bash
Skipping report deployment (no tests executed)
```

#### ステップ3: testmondataのみデプロイ

- `.testmondata` → ghpagesにアップロード（変更なし）
- HTML/Coverageレポート → **スキップ**（既存レポートが残る）
- README更新 → **スキップ**

**結果**: CI時間 約10秒、レポート生成なし（既存レポートが保持される） ✅

---

### 🔧 ソースコード変更時（テストコードは変更なし）

例: project_a/calculator/operations.pyのadd関数を修正

#### ステップ1: testmonの実行

```bash
testmon: changed files: project_a/calculator/operations.py
environment: ubuntu-latest-py3.12.9
collected 4 items / 3 deselected / 1 selected
tests/calculator/test_operations.py::test_add PASSED
✓ tests_executed=true (関連するtest_addのみ実行)
```

#### ステップ2: 完全なレポート生成

```bash
pytest --html=... --cov=project_a ...
collected 4 items
All 4 tests PASSED [100%]
Coverage: 100%
```

#### ステップ3: デプロイ

- 更新された`.testmondata` → ghpagesにアップロード
- 新しいHTML/Coverageレポート → ghpagesにデプロイ
- README更新

**結果**: CI時間 約2分、testmonは1テストのみ実行、レポートは全テストの結果(100%) ✅

---

## 📊 パフォーマンス比較

| シナリオ | testmon実行 | レポート生成 | CI時間 | カバレッジ |
|----------|-------------|-------------|---------|-----------|
| 初回実行 | 全テスト(4件) | 全テスト(4件) | 約2分 | 100% |
| テスト変更 | 増分(1件) | 全テスト(4件) | 約2分 | 100% |
| 変更なし | なし(0件) | **スキップ** | **約10秒** 🚀 | N/A |
| ソース変更 | 増分(1件) | 全テスト(4件) | 約2分 | 100% |

---

## 🎯 メリット

1. **変更がない場合のCI時間が劇的に短縮**（2分 → 10秒）
2. **レポートは常に全テストの結果を表示（カバレッジ100%）**
3. **testmondataが蓄積され、正確な増分テストが可能**
4. **GitHub Pagesのレポートは常に最新かつ完全**

---

## 🔍 ファイル差分検出との比較

### 他のアプローチとの違い

#### 1. GitHub Actions `paths`フィルター

```yaml
on:
  push:
    paths:
      - 'project_a/**'
      - 'tests/**'
```

**動作**:

- ファイル変更があれば**ワークフロー全体を実行**
- 変更がなければ**ワークフロー自体がスキップ**

**問題点**:

- ❌ `project_a/calculator/operations.py`が変更 → **全テスト実行**（無駄）
- ❌ `tests/calculator/test_operations.py`が変更 → **全テスト実行**（無駄）
- ✅ 他のファイル変更 → ワークフロースキップ（OK）

**CI時間**: 変更あり = 2分、変更なし = 0秒

#### 2. dorny/paths-filter アクション

```yaml
- uses: dorny/paths-filter@v2
  id: changes
  with:
    filters: |
      calculator:
        - 'project_a/calculator/**'
        - 'tests/calculator/**'

- name: Test calculator
  if: steps.changes.outputs.calculator == 'true'
  run: pytest tests/calculator/
```

**動作**:

- ファイルパスに基づいて**テストディレクトリを選択**
- 変更されたディレクトリのテストのみ実行

**問題点**:

- ⚠️ `operations.py`の`add`関数変更 → **test_add, test_subtract, test_multiply, test_divide全部実行**（粗い粒度）
- ✅ calculator配下の変更 → calculatorテストのみ実行（OK）
- ❌ `test_operations.py`変更 → **全calculatorテスト実行**（細かい制御不可）

**CI時間**: 変更あり = 1-2分、変更なし = 0秒

#### 3. pytest-testmon（本プロジェクトの採用方式）

```yaml
- run: pytest --testmon --testmon-env "$ENV_ID" -v
```

**動作**:

- **関数レベル**で依存関係を追跡
- 変更された関数に関連する**テストのみ実行**

**詳細な制御**:

- ✅ `operations.py`の`add`関数変更 → **test_addのみ実行**（最適）
- ✅ `test_operations.py`の`test_subtract`変更 → **test_subtractのみ実行**（最適）
- ✅ 無関係なファイル変更 → **テストスキップ**
- ✅ 初回実行 → **全テスト実行してデータベース構築**

**CI時間**: 変更あり = 約2分（testmon実行 + レポート生成）、変更なし = 10秒

### 📊 具体例での比較

#### シナリオ1: operations.pyのadd関数のみ変更

| 方式 | 実行されるテスト | CI時間 |
|------|-----------------|--------|
| **pathsフィルター** | test_add, test_subtract, test_multiply, test_divide（全4件） | 2分 |
| **paths-filter** | test_add, test_subtract, test_multiply, test_divide（全4件） | 2分 |
| **pytest-testmon** | **test_addのみ（1件）** 🎯 | testmon: 5秒 / レポート: 2分 / 合計: 2分 |

#### シナリオ2: test_operations.pyのtest_subtract変更

| 方式 | 実行されるテスト | CI時間 |
|------|-----------------|--------|
| **pathsフィルター** | 全4テスト | 2分 |
| **paths-filter** | 全4テスト | 2分 |
| **pytest-testmon** | **test_subtractのみ（1件）** 🎯 | 2分 |

#### シナリオ3: README.md変更のみ

| 方式 | 実行されるテスト | CI時間 |
|------|-----------------|--------|
| **pathsフィルター** | なし（ワークフロースキップ） | 0秒 |
| **paths-filter** | なし（テストスキップ） | 30秒 |
| **pytest-testmon** | **なし（テストスキップ）** 🎯 | **10秒** |

### 🎯 testmonの独自の利点

#### 1. 関数レベルの依存関係追跡

**pathsフィルター/paths-filter**:

```text
operations.py変更 → tests/calculator/全テスト実行
```

**testmon**:

```python
# operations.pyのadd関数変更
def add(a, b):
    return a + b + 1  # バグ追加

# testmonは依存関係を理解している
testmon: changed files: project_a/calculator/operations.py
→ test_addのみ実行 ✅
→ test_subtract, test_multiply, test_divideはスキップ
```

#### 2. インポートチェーン追跡

```python
# utils/helper.py変更
def format_number(n):
    return str(n)

# calculator/operations.pyでインポート
from utils.helper import format_number

# testmonは追跡する
testmon: changed files: utils/helper.py
→ operations.pyに影響
→ test_add, test_subtract, test_multiply, test_divideを実行
```

pathsフィルターでは、このような間接的な依存関係を検出できません。

#### 3. テストコード自体の変更追跡

```python
# test_operations.pyのtest_add変更
def test_add():
    assert add(1, 2) == 3
    assert add(5, 5) == 10  # 新規追加

# testmon
→ test_addのみ実行
→ 他のテストはスキップ
```

### 🔄 組み合わせた構成（オプション）

**pathsフィルターとtestmonを組み合わせる**ことも可能です：

```yaml
on:
  push:
    paths:
      - 'project_a/**'
      - 'tests/**'
      - '.github/workflows/**'
  # ↑ まずワークフロー起動を制御

jobs:
  test:
    steps:
      - run: pytest --testmon ...
        # ↑ 起動後、testmonで細かく制御
```

**メリット**:

- README.md変更 → ワークフロー起動せず（0秒）
- コード変更 → testmonで最小限のテストのみ実行（2分）

### 📋 比較まとめ

| 特徴 | pathsフィルター | paths-filter | **pytest-testmon** |
|------|----------------|--------------|-------------------|
| **粒度** | ファイルパス | ディレクトリ | **関数レベル** 🎯 |
| **依存関係追跡** | ❌ | ❌ | **✅** |
| **インポート追跡** | ❌ | ❌ | **✅** |
| **テスト変更検出** | ⚠️ | ⚠️ | **✅** |
| **CI時間削減** | 中 | 中 | **大** 🚀 |
| **設定の複雑さ** | 簡単 | 中 | 中（自動追跡） |
| **誤検出リスク** | 高 | 中 | **低** |

**pytest-testmonは最も賢い選択です！**

---

## 技術詳細

### テストマトリックス

ワークフローは複数のOSとPythonバージョンでテストを実行します：

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
    python-version: [3.11.9, 3.12.9, 3.13.2]
```

各組み合わせは独自の`.testmondata`ファイルを保持します：

- `testmon-data/{os}/python/{version}/.testmondata`

### 環境識別

各テスト環境は一意に識別されます：

```bash
ENV_ID="${{ matrix.os }}-py${{ matrix.python-version }}"
# 例: ubuntu-latest-py3.12.9
```

これにより、testmonが環境ごとに変更を正確に追跡できます。

### レポートデプロイ

レポートはGitHub Pages（ghpagesブランチ）にデプロイされます：

- **pytest-html**: `pytest-html-report/{os}/python/{version}/report_page.html`
- **pytest-cov**: `pytest-cov-report/{os}/python/{version}/index.html`
- **testmondata**: `testmon-data/{os}/python/{version}/.testmondata`

### README生成

`update_readme_ghpages.yml`ワークフローは自動的に以下を実行します：

1. デプロイされたレポートをスキャン
2. Pythonバージョンを抽出（正規表現: `^[0-9]+\.[0-9]+(\.[0-9]+)?$`）
3. レポートリンク付きのmarkdownテーブルを生成
4. ghpagesブランチのREADMEを更新

---

## メンテナンス

### testmondataのクリア

大きな変更後に全テストを強制実行する場合：

```bash
# ghpagesブランチに切り替え
git checkout ghpages

# すべてのtestmondataを削除
rm -rf testmon-data/

# コミット＆プッシュ
git add -A
git commit -m "chore: Clear testmondata to force full test execution"
git push origin ghpages

# mainに戻ってワークフローをトリガー
git checkout main
gh workflow run test_pytest-testmon_deploy_multi_os.yml
```

### 手動ワークフロートリガー

```bash
gh workflow run test_pytest-testmon_deploy_multi_os.yml
```

---

## レポートの閲覧

レポートはGitHub Pagesで利用可能です：

- **pytest-html**: `https://{user}.github.io/{repo}/pytest-html-report/{os}/python/{version}/report_page.html`
- **pytest-cov**: `https://{user}.github.io/{repo}/pytest-cov-report/{os}/python/{version}/index.html`

例：

- <https://7rikazhexde.github.io/python-project-sandbox/pytest-html-report/ubuntu-latest/python/3.12.9/report_page.html>
- <https://7rikazhexde.github.io/python-project-sandbox/pytest-cov-report/ubuntu-latest/python/3.12.9/index.html>

---

## トラブルシューティング

### 空のレポート

**症状**: レポートに「No results found」と表示される

**原因**: testmondataが変更を検出せず、テストが実行されなかったため、レポートが生成されなかった。古い空のレポートが残っている。

**解決策**: testmondataをクリアする（上記メンテナンスセクション参照）

### カバレッジが期待より低い

**症状**: カバレッジが100%ではなく2%などと表示される

**原因**: 現在の実装では発生しないはずです。発生した場合は：

1. "Generate HTML and Coverage reports"ステップが`--testmon`フラグなしで実行されているか確認
2. `tests_executed=true`が正しく設定されているか確認
3. ワークフローログでエラーを確認

### READMEに「assets N/A」や「python N/A」が表示される

**症状**: レポートテーブルに無効なエントリが表示される

**原因**: README生成の正規表現が非バージョンディレクトリをフィルタリングしていない

**解決策**: `update_readme_ghpages.yml:95`で既に修正済み：

```bash
grep -E '^[0-9]+\.[0-9]+(\.[0-9]+)?$'
```

---

## 関連ファイル

- `CLAUDE.md` - プロジェクト実装計画と背景
- `TESTMON_ANALYSIS_AND_FIX_PLAN.md` - testmon問題の詳細分析
- `.github/json2vars-setter/matrix.json` - テストマトリックス設定

---

**最終更新**: 2025-11-09
