# pytest-testmon ワークフロー動作確認手順

## 事前準備

### 1. ブランチの確認

現在の作業ブランチ: `test/pytest-testmon-workflow`

```bash
git branch
# * test/pytest-testmon-workflow
```

### 2. 必要なブランチの存在確認

```bash
# ghpages ブランチが存在することを確認
git branch -r | grep ghpages
# origin/ghpages
```

## 動作確認手順

### 方法1: 自動トリガー（推奨）

ワークフローファイルを変更してプッシュすると自動的にトリガーされます。

```bash
# 軽微な変更を加える（例: コメント追加）
echo "# Test trigger" >> .github/workflows/send_payload_to_pytest_testmon.yml

# コミット・プッシュ
git add .github/workflows/send_payload_to_pytest_testmon.yml
git commit -m "test: Trigger pytest-testmon workflow"
git push origin test/pytest-testmon-workflow
```

### 方法2: 手動トリガー（GitHub UI）

1. GitHubリポジトリにアクセス
   - <https://github.com/7rikazhexde/python-project-sandbox>

2. "Actions" タブをクリック

3. 左サイドバーから "Use Send Payload Action to Pytest Testmon" を選択

4. 右側の "Run workflow" ボタンをクリック

5. ブランチを `test/pytest-testmon-workflow` に設定

6. "Run workflow" をクリック

### 方法3: GitHub CLI（ローカルから手動実行）

```bash
# GitHub CLIがインストールされている場合
gh workflow run send_payload_to_pytest_testmon.yml --ref test/pytest-testmon-workflow
```

## ワークフロー実行の流れ

### 1. トリガーワークフロー

**ワークフロー名**: `Use Send Payload Action to Pytest Testmon`

実行内容:

- `repository_dispatch` イベントを発行
- ペイロード:
  - `event_type`: `test_pytest-testmon_deploy_multi_os`
  - `ghpages_branch`: `ghpages`
  - `os_list`: `[ubuntu-latest]`
  - `version_list`: `[3.12]`

### 2. メインワークフロー

**ワークフロー名**: `pytest-testmon Deploy Multi-OS`

実行ジョブ:

1. **test-and-deploy-testmon** (ubuntu-latest, Python 3.12)
   - 環境セットアップ
   - 前回の .testmondata 取得
   - デバッグ情報出力（前）
   - pytest-testmon 実行
   - デバッグ情報出力（後）
   - WALチェックポイント実行
   - アーティファクトアップロード

2. **deploy-testmon**
   - アーティファクトダウンロード
   - ghpages ブランチへデプロイ

3. **trigger-other-workflows**
   - pytest-cov ワークフロートリガー
   - pytest-html ワークフロートリガー

### 3. 後続ワークフロー

- **pytest-cov Report and Deploy Multi-OS**
- **pytest-html Report and Deploy Multi-OS**

## ログ確認ポイント

### 初回実行時

#### 1. デバッグ情報（テスト実行前）

```text
=== Before Test Execution ===
⚠ .testmondata does NOT exist
```

#### 2. pytest-testmon 実行

```text
Running tests with testmon...
Environment ID: ubuntu-latest-py3.12
testmon: new DB, environment: ubuntu-latest-py3.12
```

#### 3. デバッグ情報（テスト実行後）

```text
=== After Test Execution ===
✓ .testmondata exists
WAL files:
-rw-r--r-- 1 ... .testmondata-wal
-rw-r--r-- 1 ... .testmondata-shm
```

#### 4. WALチェックポイント

```text
Executing WAL checkpoint...
✓ WAL checkpoint completed
✓ WAL files removed
Final .testmondata size:
-rw-r--r-- 1 ... .testmondata
```

### 2回目実行時（成功の確認）

#### 1. デバッグ情報（テスト実行前）

```text
=== Before Test Execution ===
✓ .testmondata exists
Database version:
13
Environment info:
1|ubuntu-latest-py3.12|3.12.x
Test execution count:
XX
```

#### 2. pytest-testmon 実行（重要！）

```text
Running tests with testmon...
Environment ID: ubuntu-latest-py3.12
testmon: changed files: 0, unchanged files: XX
collected 0 items
```

**✅ 成功の証**: `testmon: changed files: 0` が表示され、`new DB` が表示されない

#### 3. テストが実行されない

```text
No tests executed. Skipping deployment and further workflows.
tests_executed=false
```

これは正常な動作です（変更がないため）。

### 3回目実行時（変更後）

コードを変更してから実行:

```bash
# 例: project_a の任意のファイルを編集
echo "# Test change" >> project_a/calculator/operations.py
git add project_a/calculator/operations.py
git commit -m "test: Trigger testmon with changes"
git push origin test/pytest-testmon-workflow
```

期待されるログ:

```text
testmon: changed files: 1, unchanged files: XX
collected Y items (deselected Z items)
```

影響を受けるテストのみが実行されます。

## トラブルシューティング

### 問題1: まだ "new DB" と表示される

**確認項目:**

1. WALチェックポイントが実行されているか

   ```text
   ログで "✓ WAL checkpoint completed" を確認
   ```

2. .testmondata が正しくアップロードされているか

   ```text
   ログで "File moved successfully" を確認
   ```

3. ghpages ブランチに .testmondata が存在するか

   ```bash
   git fetch origin ghpages:ghpages
   git checkout ghpages
   ls -la testmon-data/ubuntu-latest/python/3.12/
   ```

4. データベースバージョンの確認

   ```bash
   sqlite3 testmon-data/ubuntu-latest/python/3.12/.testmondata "PRAGMA user_version;"
   # 13 と表示されるべき
   ```

### 問題2: ワークフローがトリガーされない

**確認項目:**

1. ブランチが正しいか

   ```bash
   git branch
   # * test/pytest-testmon-workflow
   ```

2. ワークフローファイルの配置

   ```bash
   ls -la .github/workflows/send_payload_to_pytest_testmon.yml
   ls -la .github/workflows/test_pytest-testmon_deploy_multi_os.yml
   ```

3. パーミッション確認
   - Settings > Actions > General > Workflow permissions
   - "Read and write permissions" が有効か確認

### 問題3: "packages changed" が表示される

**確認:**

```text
The packages installed in your Python environment have been changed.
All tests have to be re-executed.
```

**対処法:**

poetry.lock が変更されていないか確認:

```bash
git diff origin/main poetry.lock
```

必要に応じて `pyproject.toml` で依存パッケージを無視:

```toml
[tool.pytest.ini_options]
testmon_ignore_dependencies = [
    "setuptools",
    "pip",
    "wheel",
]
```

## 成功の確認チェックリスト

### ✅ 初回実行

- [ ] ワークフローが正常に完了
- [ ] "new DB" メッセージが表示される（正常）
- [ ] WALチェックポイントが実行される
- [ ] .testmondata がアップロードされる
- [ ] ghpages にデプロイされる

### ✅ 2回目実行（変更なし）

- [ ] ワークフローが正常に完了
- [ ] "changed files: 0" と表示される
- [ ] "new DB" が表示されない ⭐重要
- [ ] "collected 0 items" と表示される
- [ ] tests_executed=false になる

### ✅ 3回目実行（変更あり）

- [ ] ワークフローが正常に完了
- [ ] "changed files: 1" (または変更数) と表示される
- [ ] 影響を受けるテストのみが実行される
- [ ] tests_executed=true になる
- [ ] 後続ワークフローがトリガーされる

## 次のステップ

### 成功後の展開

1. **複数OS・Pythonバージョンでテスト**

   `send_payload_to_pytest_testmon.yml` を編集:

   ```yaml
   os_list: '[ubuntu-latest,macos-13,windows-latest]'
   version_list: '[3.12,3.13]'
   ```

2. **mainブランチへの適用**

   テストが成功したら、mainブランチでも動作するように設定:

   ```yaml
   on:
     push:
       branches:
         - 'main'  # test/pytest-testmon-workflow から変更
   ```

3. **既存ワークフローとの統合**

   動作が安定したら、既存のワークフローと統合を検討。

## 関連ドキュメント

- `CLAUDE.md` - プロジェクト概要と実装詳細
- `TESTMON_ANALYSIS_AND_FIX_PLAN.md` - 問題分析と改善案
- [pytest-testmon 公式ドキュメント](https://testmon.org)

---

**最終更新**: 2025-11-09
**担当**: pytest-testmon 統合チーム
