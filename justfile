# デフォルトレシピを表示
default:
    @just --list

# テスト関連コマンド
test-coverage-verbose:
    uv run pytest -s -vv --cov=. --cov-branch --cov-report term-missing --cov-report html

test-html-report:
    uv run pytest --html=htmlcov/report_page.html

test-ci-xml:
    uv run python scripts/run_tests.py --report xml

test-ci-term:
    uv run python scripts/run_tests.py --report term

test-testmon:
    uv run pytest --testmon

test-coverage:
    uv run pytest --cov=. --cov-branch --cov-report=term-missing --cov-report=html

# 短縮エイリアス
testcov: test-coverage
testcovv: test-coverage-verbose
testhtml: test-html-report
testmon: test-testmon

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

# クリーンアップ
clean:
    rm -rf .pytest_cache
    rm -rf htmlcov
    rm -rf .coverage
    rm -rf .mypy_cache
    rm -rf .ruff_cache
    find . -type d -name __pycache__ -delete
    find . -type f -name "*.pyc" -delete

# 開発環境セットアップ
setup: install
    uv run pre-commit install

# ヘルプ（詳細な説明付き）
help:
    @echo "Available commands:"
    @echo ""
    @echo "Testing:"
    @echo "  test-coverage        - Run tests with coverage report"
    @echo "  test-coverage-verbose - Run tests with verbose coverage report"
    @echo "  test-html-report     - Run tests with HTML report"
    @echo "  test-ci-xml          - Run tests for CI with XML report"
    @echo "  test-ci-term         - Run tests for CI with terminal report"
    @echo "  test-testmon         - Run tests with testmon (changed files only)"
    @echo ""
    @echo "Aliases:"
    @echo "  testcov              - Alias for test-coverage"
    @echo "  testcovv             - Alias for test-coverage-verbose"
    @echo "  testhtml             - Alias for test-html-report"
    @echo "  testmon              - Alias for test-testmon"
    @echo ""
    @echo "Development:"
    @echo "  install              - Install all dependencies"
    @echo "  install-prod         - Install production dependencies only"
    @echo "  update               - Update dependencies"
    @echo "  lint                 - Run linting"
    @echo "  lint-fix             - Run linting with auto-fix"
    @echo "  type-check           - Run type checking"
    @echo "  format               - Format code"
    @echo "  check                - Run all quality checks"
    @echo "  pre-commit           - Run pre-commit hooks"
    @echo "  clean                - Clean up generated files"
    @echo "  setup                - Setup development environment"
