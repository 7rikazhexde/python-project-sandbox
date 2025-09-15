# デフォルトレシピを表示
default:
    @just --list

# テスト関連コマンド
test-coverage-verbose:
    uv run pytest -s -vv --cov=. --cov-branch --cov-report term-missing --cov-report html

test-html-report:
    uv run pytest --html=htmlcov/report_page.html --self-contained-html --css=css/style.css --capture=no project_a tests/

test-html-report-custom htmldir="htmlcov":
    uv run pytest --html={{htmldir}}/report_page.html --self-contained-html --css=css/style.css --capture=no project_a tests/

test-ci-xml:
    uv run python scripts/run_tests.py --report xml

test-ci-term:
    uv run python scripts/run_tests.py --report term

test-testmon:
    uv run pytest --testmon

test-coverage:
    uv run python -m pytest --cov=project_a --cov-branch --cov-report=term-missing --cov-report=html --cov-report=xml project_a tests/

# カスタムHTMLディレクトリを指定可能なカバレッジテスト
test-coverage-custom htmldir="htmlcov":
    uv run pytest --cov=project_a --cov-branch --cov-report=term-missing --cov-report="html:{{htmldir}}" --cov-report=xml project_a tests/

# CI/CD用の包括的なテストコマンド
test-ci-full:
    @echo "🧪 Running comprehensive CI tests..."
    uv run pytest --junitxml=pytest.xml --cov=project_a --cov-report=xml:coverage.xml --cov-report=term-missing project_a tests/ | tee pytest-coverage.txt
    @echo "✅ CI tests completed successfully"

# 短縮エイリアス
testcov: test-coverage
testcovv: test-coverage-verbose
testhtml: test-html-report
testmon: test-testmon

# カスタムHTMLディレクトリ用のエイリアス
testcov-custom htmldir="htmlcov": (test-coverage-custom htmldir)
testhtml-custom htmldir="htmlcov": (test-html-report-custom htmldir)

# 開発関連コマンド
install:
    uv sync --extra dev

install-prod:
    uv sync

update:
    uv lock --upgrade && uv sync --extra dev

lint:
    uv run ruff check

lint-fix:
    uv run ruff check --fix

type-check:
    uv run mypy project_a tests ci scripts

format:
    uv run ruff format

# 総合的な品質チェック
check: lint type-check test-coverage

# プリコミットフック実行
pre-commit:
    uv run pre-commit run --all-files

# GitHub Actions ワークフローのlint
lint-workflows:
    @echo "🔍 Linting GitHub Actions workflows..."
    @if command -v actionlint >/dev/null 2>&1; then \
        if find .github/workflows -name "*.yml" -o -name "*.yaml" 2>/dev/null | grep -q .; then \
            actionlint .github/workflows/*.yml .github/workflows/*.yaml 2>/dev/null || find .github/workflows -name "*.yml" -o -name "*.yaml" -exec actionlint {} \; ; \
            echo "✅ Workflow linting completed"; \
        else \
            echo "ℹ️ No workflow files found in .github/workflows/"; \
        fi; \
    else \
        echo "❌ actionlint not found. Install it with:"; \
        echo "   go install github.com/rhysd/actionlint/cmd/actionlint@latest"; \
        echo "   Or download from: https://github.com/rhysd/actionlint/releases"; \
        exit 1; \
    fi

# Shellcheck でシェルスクリプトをチェック
lint-shell:
    @echo "🐚 Checking shell scripts..."
    @if command -v shellcheck >/dev/null 2>&1; then \
        shell_files=$(find . -name "*.sh" -o -name "*.bash" 2>/dev/null || true); \
        if [ -n "$shell_files" ]; then \
            echo "$shell_files" | xargs shellcheck; \
            echo "✅ Shell script linting completed"; \
        else \
            echo "ℹ️ No shell script files found"; \
        fi; \
    else \
        echo "❌ shellcheck not found. Install it with:"; \
        echo "   Ubuntu/Debian: apt-get install shellcheck"; \
        echo "   macOS: brew install shellcheck"; \
        echo "   Or download from: https://github.com/koalaman/shellcheck/releases"; \
        exit 1; \
    fi

# Markdown ファイルのlint
lint-markdown:
    @echo "📝 Linting Markdown files..."
    @if command -v markdownlint >/dev/null 2>&1; then \
        if [ -f ".markdownlint.json" ]; then \
            markdownlint --config .markdownlint.json README.md; \
        else \
            markdownlint README.md; \
        fi; \
        echo "✅ Markdown linting completed"; \
    else \
        echo "❌ markdownlint not found. Install it with:"; \
        echo "   npm install -g markdownlint-cli"; \
        exit 1; \
    fi

# 全てのlintを実行
lint-all: lint lint-workflows lint-shell lint-markdown
    @echo "🎉 All linting completed successfully!"

# 詳細なレポート生成（開発用）
report-all:
    @echo "📊 Generating comprehensive test reports..."
    rm -rf htmlcov/ pytest.xml coverage.xml pytest-coverage.txt || true
    uv run pytest --cov=project_a --cov-branch --cov-report=html --cov-report=xml --cov-report=term-missing --html=htmlcov/test_report.html --self-contained-html --css=css/style.css --junitxml=pytest.xml project_a tests/ | tee pytest-coverage.txt
    @echo ""
    @echo "📁 Reports generated:"
    @echo "  📈 Coverage HTML: htmlcov/index.html"
    @echo "  📊 Test HTML: htmlcov/test_report.html"
    @echo "  📄 Coverage XML: coverage.xml"
    @echo "  📋 JUnit XML: pytest.xml"
    @echo "  📝 Coverage Text: pytest-coverage.txt"
    @echo ""
    @echo "🌐 Open reports in browser:"
    @echo "  Coverage: file://$(pwd)/htmlcov/index.html"
    @echo "  Test Results: file://$(pwd)/htmlcov/test_report.html"

# パフォーマンステスト（オプション）
test-performance:
    @echo "⚡ Running performance tests..."
    @if uv pip list | grep -q pytest-benchmark; then \
        uv run pytest --benchmark-only project_a tests/; \
    else \
        echo "ℹ️ pytest-benchmark not installed. Skipping performance tests."; \
        echo "   Install with: uv add --dev pytest-benchmark"; \
    fi

# セキュリティチェック
security-check:
    @echo "🔒 Running security checks..."
    @if command -v bandit >/dev/null 2>&1; then \
        bandit -r project_a/; \
        echo "✅ Security check completed"; \
    else \
        echo "ℹ️ bandit not installed. Skipping security checks."; \
        echo "   Install with: uv add --dev bandit"; \
    fi

# 依存関係の脆弱性チェック
check-vulnerabilities:
    @echo "🛡️ Checking for known vulnerabilities..."
    @if command -v safety >/dev/null 2>&1; then \
        safety check; \
        echo "✅ Vulnerability check completed"; \
    else \
        echo "ℹ️ safety not installed. Skipping vulnerability checks."; \
        echo "   Install with: uv add --dev safety"; \
    fi

# プロジェクトの健全性チェック
health-check: lint-all type-check test-coverage security-check check-vulnerabilities
    @echo "🏥 Project health check completed!"

# クリーンアップ
clean:
    @echo "🧹 Cleaning up generated files..."
    rm -rf .pytest_cache htmlcov .coverage coverage.xml pytest.xml pytest-coverage.txt .mypy_cache .ruff_cache || true
    find . -type d -name __pycache__ -delete 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    @echo "✅ Cleanup completed"

# 完全なクリーンアップ（仮想環境も削除）
clean-all: clean
    @echo "🧹 Deep cleaning (including virtual environment)..."
    rm -rf .venv || true
    @echo "✅ Deep cleanup completed"

# 開発環境セットアップ
setup: install
    @echo "🚀 Setting up development environment..."
    uv run pre-commit install
    @if [ -f ".git/hooks/pre-commit" ]; then \
        echo "✅ Pre-commit hooks installed"; \
    else \
        echo "⚠️ Pre-commit hooks not installed"; \
    fi
    @echo "🎉 Development environment setup completed!"

# 本番環境用ビルド
build:
    @echo "🏗️ Building for production..."
    uv sync --no-dev
    just test-ci-full
    just type-check
    just security-check
    @echo "✅ Production build completed!"

# リリース準備
prepare-release version:
    @echo "🚀 Preparing release {{version}}..."
    just health-check
    @echo "📝 Please update version to {{version}} in pyproject.toml"
    @echo "🏷️ After updating, create a git tag: git tag v{{version}}"
    @echo "✅ Release preparation checklist completed!"

# 開発サーバー起動（Dashアプリがある場合）
serve:
    @echo "🌐 Starting development server..."
    @dash_files=$(find project_a -name "*dashboard*.py" -o -name "*app*.py" 2>/dev/null || true); \
    if [ -n "$dash_files" ]; then \
        echo "📊 Found Dash application files:"; \
        echo "$dash_files"; \
        echo "🚀 Starting Dash server..."; \
        uv run python -c "import project_a.staking.ton_whales_staking_dashboard; project_a.staking.ton_whales_staking_dashboard.app.run_server(debug=True)" 2>/dev/null || \
        echo "⚠️ Could not start Dash server automatically. Please run your application manually."; \
    else \
        echo "ℹ️ No Dash application files found"; \
    fi

# デバッグ情報の表示
debug-info:
    @echo "🔍 Debug Information"
    @echo "===================="
    @echo ""
    @echo "📦 Environment:"
    @echo "  Python: $(uv run python --version)"
    @echo "  uv: $(uv --version)"
    @echo "  Current directory: $(pwd)"
    @echo ""
    @echo "📋 Installed packages:"
    @uv pip list | head -20
    @echo "  ... (showing first 20 packages)"
    @echo ""
    @echo "🔧 Tool availability:"
    @for tool in just actionlint shellcheck markdownlint bandit safety; do \
        if command -v "$tool" >/dev/null 2>&1; then \
            echo "  ✅ $tool: $(command -v "$tool")"; \
        else \
            echo "  ❌ $tool: not found"; \
        fi; \
    done
    @echo ""
    @echo "📁 Project structure:"
    @find . -maxdepth 2 -type f -name "*.py" | head -10
    @echo "  ... (showing first 10 Python files)"

# ヘルプ（詳細な説明付き）
help:
    @echo "Available commands:"
    @echo ""
    @echo "🧪 Testing:"
    @echo "  test-coverage        - Run tests with coverage report"
    @echo "  test-coverage-verbose - Run tests with verbose coverage report"
    @echo "  test-coverage-custom - Run tests with custom HTML directory"
    @echo "  test-html-report     - Run tests with HTML report (pytest-html)"
    @echo "  test-html-report-custom - Run tests with custom HTML report location"
    @echo "  test-ci-xml          - Run tests for CI with XML report"
    @echo "  test-ci-term         - Run tests for CI with terminal report"
    @echo "  test-ci-full         - Run comprehensive CI tests"
    @echo "  test-testmon         - Run tests with testmon (changed files only)"
    @echo "  test-performance     - Run performance benchmarks"
    @echo "  report-all           - Generate all types of reports"
    @echo ""
    @echo "🔍 Code Quality:"
    @echo "  lint                 - Run Python linting (ruff)"
    @echo "  lint-fix             - Run Python linting with auto-fix"
    @echo "  lint-workflows       - Lint GitHub Actions workflows"
    @echo "  lint-shell           - Lint shell scripts"
    @echo "  lint-markdown        - Lint Markdown files"
    @echo "  lint-all             - Run all linting checks"
    @echo "  type-check           - Run type checking (mypy)"
    @echo "  format               - Format code (ruff format)"
    @echo "  check                - Run all quality checks"
    @echo "  health-check         - Comprehensive project health check"
    @echo ""
    @echo "🔒 Security:"
    @echo "  security-check       - Run security analysis (bandit)"
    @echo "  check-vulnerabilities - Check for known vulnerabilities (safety)"
    @echo ""
    @echo "📦 Environment:"
    @echo "  install              - Install all dependencies"
    @echo "  install-prod         - Install production dependencies only"
    @echo "  update               - Update dependencies"
    @echo "  setup                - Setup development environment"
    @echo "  clean                - Clean up generated files"
    @echo "  clean-all            - Deep clean (including virtual environment)"
    @echo ""
    @echo "🚀 Development:"
    @echo "  pre-commit           - Run pre-commit hooks"
    @echo "  serve                - Start development server"
    @echo "  debug-info           - Show debug information"
    @echo ""
    @echo "🏗️ Build & Release:"
    @echo "  build                - Build for production"
    @echo "  prepare-release      - Prepare for release (requires version)"
    @echo ""
    @echo "📚 Aliases:"
    @echo "  testcov              - Alias for test-coverage"
    @echo "  testcovv             - Alias for test-coverage-verbose"
    @echo "  testcov-custom       - Alias for test-coverage-custom"
    @echo "  testhtml             - Alias for test-html-report"
    @echo "  testhtml-custom      - Alias for test-html-report-custom"
    @echo "  testmon              - Alias for test-testmon"
    @echo ""
    @echo "💡 Examples:"
    @echo "  just setup                    # Set up development environment"
    @echo "  just testcov                  # Run tests with coverage"
    @echo "  just lint-all                 # Run all linting"
    @echo "  just health-check             # Full project health check"
    @echo "  just prepare-release 1.2.3    # Prepare version 1.2.3 for release"
