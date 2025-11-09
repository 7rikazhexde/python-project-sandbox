# Testing Documentation

## Overview

This project uses pytest-testmon for incremental testing to reduce CI execution time while maintaining comprehensive test coverage reports on GitHub Pages.

## Workflow Architecture

### Main Workflow

- **File**: `.github/workflows/test_pytest-testmon_deploy_multi_os.yml`
- **Purpose**: Incremental testing with pytest-testmon and full report generation
- **Trigger**: Push to main branch

### Supporting Workflows

- **README Update**: `.github/workflows/update_readme_ghpages.yml`
  - Automatically generates test report links on ghpages branch
  - Triggers after testmon workflow completes

### Disabled Workflows

- `test_pytest-html-report_deploy_multi_os.yml` (DISABLED)
- `test_pytest-cov-report_deploy_multi_os.yml` (DISABLED)

These workflows were consolidated into the testmon workflow to prevent timing issues and ensure consistency.

## Test Execution Behavior

### 🎯 Initial Execution (No testmondata exists)

#### Step 1: Run testmon

```bash
testmon: new DB, environment: ubuntu-latest-py3.12.9
collected 4 items
tests/calculator/test_operations.py::test_add PASSED
tests/calculator/test_operations.py::test_subtract PASSED
tests/calculator/test_operations.py::test_multiply PASSED
tests/calculator/test_operations.py::test_divide PASSED
✓ tests_executed=true
```

#### Step 2: Generate full reports

```bash
Generate HTML and Coverage reports
pytest --html=... --cov=project_a ...
collected 4 items
All tests PASSED [100%]
Coverage: 100%
```

#### Step 3: Deploy

- `.testmondata` → uploaded to ghpages branch
- HTML/Coverage reports → deployed to ghpages branch
- README updated with report links

**Result**: CI time ~2 minutes, 100% coverage reports generated ✅

---

### ✏️ Test Case Changes (Add/Delete/Modify)

Example: Adding `test_power` to test_operations.py

#### Step 1: Run testmon

```bash
testmon: changed files: tests/calculator/test_operations.py
environment: ubuntu-latest-py3.12.9
collected 5 items / 4 deselected / 1 selected
tests/calculator/test_operations.py::test_power PASSED
✓ tests_executed=true (new test detected)
```

#### Step 2: Generate full reports

```bash
pytest --html=... --cov=project_a ...
collected 5 items
All 5 tests PASSED [100%]
Coverage: 100%
```

#### Step 3: Deploy

- Updated `.testmondata` → uploaded to ghpages
- New HTML/Coverage reports → deployed to ghpages
- README updated

**Result**: CI time ~2 minutes, all 5 tests executed, 100% coverage reports ✅

---

### 🚫 No Changes (testmondata is up-to-date)

#### Step 1: Run testmon

```bash
testmon: changed files: 0, unchanged files: 16
environment: ubuntu-latest-py3.12.9
collected 0 items
no tests ran in 0.02s
✓ tests_executed=false (no changes)
```

#### Step 2: Skip report generation

```bash
Skipping report deployment (no tests executed)
```

#### Step 3: Deploy testmondata only

- `.testmondata` → uploaded to ghpages (unchanged)
- HTML/Coverage reports → **SKIPPED** (existing reports remain)
- README update → **SKIPPED**

**Result**: CI time ~10 seconds, no report generation (existing reports preserved) ✅

---

### 🔧 Source Code Changes (Test code unchanged)

Example: Modifying add function in project_a/calculator/operations.py

#### Step 1: Run testmon

```bash
testmon: changed files: project_a/calculator/operations.py
environment: ubuntu-latest-py3.12.9
collected 4 items / 3 deselected / 1 selected
tests/calculator/test_operations.py::test_add PASSED
✓ tests_executed=true (only related test_add executed)
```

#### Step 2: Generate full reports

```bash
pytest --html=... --cov=project_a ...
collected 4 items
All 4 tests PASSED [100%]
Coverage: 100%
```

#### Step 3: Deploy

- Updated `.testmondata` → uploaded to ghpages
- New HTML/Coverage reports → deployed to ghpages
- README updated

**Result**: CI time ~2 minutes, testmon runs 1 test, reports show all tests (100%) ✅

---

## 📊 Performance Comparison

| Scenario | Testmon Execution | Report Generation | CI Time | Coverage |
|----------|------------------|-------------------|---------|----------|
| Initial run | All tests (4) | All tests (4) | ~2 min | 100% |
| Test changes | Incremental (1) | All tests (4) | ~2 min | 100% |
| No changes | None (0) | **SKIPPED** | **~10 sec** 🚀 | N/A |
| Source changes | Incremental (1) | All tests (4) | ~2 min | 100% |

---

## 🎯 Benefits

1. **Dramatic CI time reduction when no changes** (2 min → 10 sec)
2. **Reports always show full test results (100% coverage)**
3. **testmondata accumulates for accurate incremental testing**
4. **GitHub Pages reports are always current and complete**

---

## Technical Details

### Test Matrix

The workflow runs tests across multiple OS and Python versions:

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
    python-version: [3.11.9, 3.12.9, 3.13.2]
```

Each combination maintains its own `.testmondata` file:

- `testmon-data/{os}/python/{version}/.testmondata`

### Environment Identification

Each test environment is uniquely identified:

```bash
ENV_ID="${{ matrix.os }}-py${{ matrix.python-version }}"
# Example: ubuntu-latest-py3.12.9
```

This ensures testmon correctly tracks changes per environment.

### Report Deployment

Reports are deployed to GitHub Pages (ghpages branch):

- **pytest-html**: `pytest-html-report/{os}/python/{version}/report_page.html`
- **pytest-cov**: `pytest-cov-report/{os}/python/{version}/index.html`
- **testmondata**: `testmon-data/{os}/python/{version}/.testmondata`

### README Generation

The `update_readme_ghpages.yml` workflow automatically:

1. Scans deployed reports
2. Extracts Python versions (regex: `^[0-9]+\.[0-9]+(\.[0-9]+)?$`)
3. Generates markdown tables with report links
4. Updates ghpages branch README

---

## Maintenance

### Clearing testmondata

To force a full test run (e.g., after major changes):

```bash
# Switch to ghpages branch
git checkout ghpages

# Remove all testmondata
rm -rf testmon-data/

# Commit and push
git add -A
git commit -m "chore: Clear testmondata to force full test execution"
git push origin ghpages

# Return to main and trigger workflow
git checkout main
gh workflow run test_pytest-testmon_deploy_multi_os.yml
```

### Manual Workflow Trigger

```bash
gh workflow run test_pytest-testmon_deploy_multi_os.yml
```

---

## Viewing Reports

Reports are available on GitHub Pages:

- **pytest-html**: `https://{user}.github.io/{repo}/pytest-html-report/{os}/python/{version}/report_page.html`
- **pytest-cov**: `https://{user}.github.io/{repo}/pytest-cov-report/{os}/python/{version}/index.html`

Example:

- <https://7rikazhexde.github.io/python-project-sandbox/pytest-html-report/ubuntu-latest/python/3.12.9/report_page.html>
- <https://7rikazhexde.github.io/python-project-sandbox/pytest-cov-report/ubuntu-latest/python/3.12.9/index.html>

---

## Troubleshooting

### Empty Reports

**Symptom**: Report shows "No results found"

**Cause**: testmondata detected no changes, so no tests ran and no reports were generated. The old empty report remains.

**Solution**: Clear testmondata (see Maintenance section above)

### Coverage Lower Than Expected

**Symptom**: Coverage shows 2% instead of 100%

**Cause**: This should not happen with the current implementation. If it does:

1. Check that "Generate HTML and Coverage reports" step runs without `--testmon` flag
2. Verify `tests_executed=true` was set correctly
3. Check workflow logs for errors

### "assets N/A" or "python N/A" in README

**Symptom**: Invalid entries in report table

**Cause**: README generation regex not filtering non-version directories

**Solution**: Already fixed in `update_readme_ghpages.yml:95` with regex filter:

```bash
grep -E '^[0-9]+\.[0-9]+(\.[0-9]+)?$'
```

---

## Related Files

- `CLAUDE.md` - Project implementation plan and background
- `TESTMON_ANALYSIS_AND_FIX_PLAN.md` - Detailed analysis of testmon issues
- `.github/json2vars-setter/matrix.json` - Test matrix configuration

---

**Last Updated**: 2025-11-09
