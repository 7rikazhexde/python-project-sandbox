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
