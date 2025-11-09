# pytest-testmon GitHub Actions統合プロジェクト

## プロジェクト概要

このプロジェクトは、pytest-testmonをGitHub ActionsのCI環境で効果的に活用するための実装です。`.testmondata`をGitHub Pagesで永続化し、増分テスト実行によりCI時間を短縮することを目指しています。

## 問題の背景

### 現在の課題

pytest-testmonをGitHub Actionsで使用する際、以下の問題が発生しています:

- `.testmondata`が常に新規作成されてしまう（"testmon: new DB"メッセージが表示される）
- GitHub Pagesから取得した`.testmondata`が認識されない
- 結果として全テストが毎回実行され、増分テスト実行の恩恵が得られない

### 関連情報

- **GitHub Issue**: [pytest-testmon #236](https://github.com/tarpas/pytest-testmon/issues/236)
- **詳細分析**: `TESTMON_ANALYSIS_AND_FIX_PLAN.md`を参照

## 根本原因

TESTMON_ANALYSIS_AND_FIX_PLAN.mdの分析により、以下の原因が特定されています:

1. **SQLite WALモードファイルの欠落** (最重要)
   - `.testmondata-wal`と`.testmondata-shm`がアップロード/ダウンロードされていない
   - WALチェックポイントが実行されていないため、データベースの整合性が保証されない

2. **システムパッケージの変更検出**
   - CI環境でのパッケージバージョン変動
   - インストール順序の違い

3. **環境識別子の不一致**
   - OS × Pythonバージョンの組み合わせが適切に識別されていない

4. **条件付きアップロードによるデータ損失**
   - テストが実行されない場合、データがアップロードされない

## プロジェクト構造

### 既存のワークフロー（本番環境）

以下のワークフローは既に本番稼働しており、`ghpages`ブランチにデプロイしています:

```text
.github/workflows/
├── test-pytest-cov-report.yml      # カバレッジレポート生成・デプロイ (ghpagesブランチ)
└── test-pytest-html-report.yml     # HTMLテストレポート生成・デプロイ (ghpagesブランチ)
```

### テスト用ワークフロー（開発環境）

以下のワークフローはテスト・検証用で、`repository_dispatch`イベントで起動されます:

```text
.github/workflows/test_workflow/
├── test_pytest-testmon_deploy_multi_os.yml     # testmonデータ管理
├── test_pytest-html-report_deploy_multi_os.yml # HTMLレポート生成（testmonベース）
└── test_pytest-cov-report_deploy_multi_os.yml  # カバレッジレポート生成（testmonベース）
```

## 実装計画

### 基本方針

1. **既存ワークフローとの区別**
   - 既存の`ghpages`ブランチは使用しない
   - 新しく`ghpages_pytest-testmon`ブランチを作成してテスト

2. **作業用ブランチ**
   - ブランチ名: `test/pytest-testmon-workflow`
   - 既存の本番ワークフローに影響を与えずに開発・テスト

3. **段階的な実装**
   - フェーズ1: デバッグ情報追加による問題の可視化
   - フェーズ2: WALチェックポイント実装
   - フェーズ3: 環境識別子の明示化
   - フェーズ4: 動作確認と最適化

### 修正対象ワークフロー

#### 1. test_pytest-testmon_deploy_multi_os.yml

**現在の処理フロー:**

```text
1. ghpagesブランチから.testmondataを取得
2. pytest --testmonを実行
3. .testmondataをアーティファクトとしてアップロード
4. ghpagesブランチにデプロイ
5. 後続ワークフロー（cov, html）をトリガー
```

**必要な修正:**

- [ ] ghpagesブランチ → ghpages_pytest-testmonブランチに変更
- [ ] SQLite WALチェックポイントの追加（最重要）
- [ ] 環境識別子の明示的設定（`--testmon-env`）
- [ ] デバッグ情報の追加
- [ ] 無条件アップロードへの変更（`if: always()`）

#### 2. test_pytest-html-report_deploy_multi_os.yml

**必要な修正:**

- [ ] ghpagesブランチ → ghpages_pytest-testmonブランチに変更
- [ ] testmonデータ取得元の変更

#### 3. test_pytest-cov-report_deploy_multi_os.yml

**必要な修正:**

- [ ] ghpagesブランチ → ghpages_pytest-testmonブランチに変更
- [ ] testmonデータ取得元の変更

## 実装の詳細

### フェーズ1: デバッグ情報の追加

テスト実行前後で以下の情報を出力:

- データベースファイルの存在確認
- データベースバージョン（`PRAGMA user_version`）
- 環境レコード数
- テスト実行レコード数
- WALファイルの有無

```yaml
- name: Debug - Check testmon data before test
  run: |
    if [ -f .testmondata ]; then
      echo "✓ .testmondata exists"
      ls -lh .testmondata*
      sqlite3 .testmondata "PRAGMA user_version;"
      sqlite3 .testmondata "SELECT COUNT(*) FROM test_execution;"
    fi
```

### フェーズ2: WALチェックポイントの実装

テスト実行後、アップロード前にWALチェックポイントを実行:

```yaml
- name: Checkpoint testmon database
  if: always()
  run: |
    if [ -f .testmondata ]; then
      sqlite3 .testmondata "PRAGMA wal_checkpoint(TRUNCATE);"
      rm -f .testmondata-wal .testmondata-shm
      echo "✓ WAL checkpoint completed"
    fi
```

### フェーズ3: 環境識別子の設定

OS × Pythonバージョンで環境を明確に識別:

```yaml
- name: Run tests with testmon
  run: |
    ENV_ID="${{ matrix.os }}-py${{ matrix.python-version }}"
    poetry run pytest --testmon --testmon-env "$ENV_ID" -v
```

### フェーズ4: ブランチ変更

すべてのワークフローで`ghpages`を`ghpages_pytest-testmon`に変更:

```yaml
# 例: test_pytest-testmon_deploy_multi_os.yml
- name: Fetch previous testmon data
  run: |
    git fetch origin ghpages_pytest-testmon:ghpages_pytest-testmon || true
    git checkout ghpages_pytest-testmon -- "testmon-data/..."
```

## 検証手順

### 1. 作業ブランチの作成

```bash
git checkout -b test/pytest-testmon-workflow
```

### 2. ghpages_pytest-testmonブランチの作成

```bash
git checkout --orphan ghpages_pytest-testmon
git rm -rf .
echo "# pytest-testmon data storage" > README.md
git add README.md
git commit -m "Initialize ghpages_pytest-testmon branch"
git push origin ghpages_pytest-testmon
```

### 3. ワークフローの修正と実行

1. デバッグ情報を追加してプッシュ
2. ワークフロー実行ログを確認
3. WALチェックポイントを実装してプッシュ
4. 2回目の実行で"new DB"が表示されないことを確認
5. 環境識別子を設定してプッシュ
6. 複数回実行して増分テストが機能することを確認

### 4. 確認ポイント

**初回実行:**
```
testmon: new DB, environment: ubuntu-latest-py3.12
```

**2回目以降（変更なし）:**
```
testmon: changed files: 0, unchanged files: X
collected 0 items
```

**変更後:**
```
testmon: changed files: 1, unchanged files: X
collected Y items (deselected Z items)
```

## トラブルシューティング

### "new DB"が継続して表示される場合

1. WALチェックポイントが実行されているか確認
2. `.testmondata`のファイルサイズが0バイトでないか確認
3. データベースバージョンが一致しているか確認（`PRAGMA user_version` = 13）
4. 環境識別子が一致しているか確認

### 全テストが実行される場合

1. "packages changed"メッセージの有無を確認
2. 環境識別子が一致しているか確認
3. Git HEAD SHAが変わっている場合は正常動作

## 追加の最適化案（オプション）

### GitHub Actions キャッシュの活用

7日間保持されるキャッシュを利用することで、より安定したデータ永続化が可能:

```yaml
- name: Restore testmon data from cache
  uses: actions/cache@v4
  with:
    path: .testmondata
    key: testmon-${{ matrix.os }}-py${{ matrix.python-version }}-${{ github.sha }}
    restore-keys: |
      testmon-${{ matrix.os }}-py${{ matrix.python-version }}-
```

### システムパッケージ無視設定

CI環境で変動しやすいパッケージを無視:

```toml
# pyproject.toml
[tool.pytest.ini_options]
testmon_ignore_dependencies = [
    "setuptools",
    "pip",
    "wheel",
    "certifi",
]
```

## 参考資料

### ドキュメント

- [pytest-testmon公式ドキュメント](https://testmon.org)
- [SQLite WALモード](https://www.sqlite.org/wal.html)
- [GitHub Actions キャッシュ](https://docs.github.com/ja/actions/using-workflows/caching-dependencies-to-speed-up-workflows)

### プロジェクト内ドキュメント

- `TESTMON_ANALYSIS_AND_FIX_PLAN.md` - 詳細な問題分析と改善案
- `.github/workflows/test-pytest-cov-report.yml` - 既存カバレッジワークフロー
- `.github/workflows/test-pytest-html-report.yml` - 既存HTMLレポートワークフロー

### 外部リンク

- [GitHub Issue #236](https://github.com/tarpas/pytest-testmon/issues/236) - 同様の問題報告

## マイルストーン

- [ ] 作業ブランチ`test/pytest-testmon-workflow`の作成
- [ ] `ghpages_pytest-testmon`ブランチの作成
- [ ] デバッグ情報の追加と初回実行
- [ ] WALチェックポイントの実装
- [ ] 環境識別子の設定
- [ ] 全ワークフローのブランチ変更
- [ ] 動作確認（複数回実行）
- [ ] 増分テスト機能の検証
- [ ] パフォーマンス測定（CI時間短縮率）
- [ ] 本番環境への統合検討

## 注意事項

1. **既存ワークフローへの影響なし**
   - `ghpages`ブランチは触らない
   - 本番稼働中のワークフローは変更しない

2. **テスト環境での実験**
   - `ghpages_pytest-testmon`ブランチで独立してテスト
   - 問題があれば容易にロールバック可能

3. **段階的な実装**
   - 一度に1つの改善案を実装
   - 各ステップで動作確認

4. **データベース整合性**
   - SQLite WALチェックポイントは必須
   - バージョン不一致に注意

## 次のステップ

1. このドキュメントの内容を確認
2. 作業ブランチ`test/pytest-testmon-workflow`を作成
3. `ghpages_pytest-testmon`ブランチを作成
4. フェーズ1（デバッグ情報追加）から開始
5. 各フェーズの結果をログで確認しながら進める

---

**最終更新**: 2025-11-09
**ステータス**: 実装準備完了
