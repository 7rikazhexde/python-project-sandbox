# Pytest Coverages Summary
[![](https://github.com/7rikazhexde/python-project-sandbox/actions/workflows/test_multi_os.yml/badge.svg)](https://github.com/7rikazhexde/python-project-sandbox/actions/workflows/test_multi_os.yml)

> [!Note]
> 
> Commit: [1bccd70d](https://github.com/7rikazhexde/python-project-sandbox/tree/1bccd70d)

> [!Important]
> The following file is intentionally excluded from test coverage:
> - [project_a/staking/ton_whales_staking_dashboard.py](https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/staking/ton_whales_staking_dashboard.py)
> 
> This file contains complex external dependencies and is verified through manual and integration testing.
> 
## Coverage Report (os: ubuntu-latest / python-version: 3.11)
<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/README.md"><img alt="coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen.svg" /></a><details><summary>Coverage Report (ubuntu-latest / Python 3.11) </summary><table><tr><th>File</th><th>Stmts</th><th>Miss</th><th>Cover</th><th>Missing</th></tr><tbody><tr><td><a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>account</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation.py">get_latest_ton_amount_calculation.py</a></td><td>71</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation_async_aiohttp.py">get_latest_ton_amount_calculation_async_aiohttp.py</a></td><td>86</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation_sync.py">get_latest_ton_amount_calculation_sync.py</a></td><td>87</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_ton_txns_api.py">get_ton_txns_api.py</a></td><td>55</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>calculator</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/calculator/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/calculator/operations.py">operations.py</a></td><td>9</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>staking</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/staking/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/staking/create_ton_stkrwd_cryptact_custom.py">create_ton_stkrwd_cryptact_custom.py</a></td><td>44</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>utils</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/config_loader.py">config_loader.py</a></td><td>20</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/ton_address_conv.py">ton_address_conv.py</a></td><td>10</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td><b>TOTAL</b></td><td><b>382</b></td><td><b>0</b></td><td><b>100%</b></td><td>&nbsp;</td></tr></tbody></table></details>

## Pytest Result Summary (os: ubuntu-latest / python-version: 3.11)
| Tests | Skipped | Failures | Errors | Time |
| ----- | ------- | -------- | -------- | ------------------ |
| 105 | 0 :zzz: | 0 :x: | 0 :fire: | 6.301s :stopwatch: |


## Coverage Report (os: ubuntu-latest / python-version: 3.12)
<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/README.md"><img alt="coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen.svg" /></a><details><summary>Coverage Report (ubuntu-latest / Python 3.12) </summary><table><tr><th>File</th><th>Stmts</th><th>Miss</th><th>Cover</th><th>Missing</th></tr><tbody><tr><td><a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>account</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation.py">get_latest_ton_amount_calculation.py</a></td><td>71</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation_async_aiohttp.py">get_latest_ton_amount_calculation_async_aiohttp.py</a></td><td>86</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation_sync.py">get_latest_ton_amount_calculation_sync.py</a></td><td>87</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_ton_txns_api.py">get_ton_txns_api.py</a></td><td>55</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>calculator</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/calculator/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/calculator/operations.py">operations.py</a></td><td>9</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>staking</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/staking/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/staking/create_ton_stkrwd_cryptact_custom.py">create_ton_stkrwd_cryptact_custom.py</a></td><td>44</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>utils</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/config_loader.py">config_loader.py</a></td><td>20</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/ton_address_conv.py">ton_address_conv.py</a></td><td>10</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td><b>TOTAL</b></td><td><b>382</b></td><td><b>0</b></td><td><b>100%</b></td><td>&nbsp;</td></tr></tbody></table></details>

## Pytest Result Summary (os: ubuntu-latest / python-version: 3.12)
| Tests | Skipped | Failures | Errors | Time |
| ----- | ------- | -------- | -------- | ------------------ |
| 105 | 0 :zzz: | 0 :x: | 0 :fire: | 7.284s :stopwatch: |


## Coverage Report (os: ubuntu-latest / python-version: 3.13)
<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/README.md"><img alt="coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen.svg" /></a><details><summary>Coverage Report (ubuntu-latest / Python 3.13) </summary><table><tr><th>File</th><th>Stmts</th><th>Miss</th><th>Cover</th><th>Missing</th></tr><tbody><tr><td><a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>account</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation.py">get_latest_ton_amount_calculation.py</a></td><td>71</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation_async_aiohttp.py">get_latest_ton_amount_calculation_async_aiohttp.py</a></td><td>86</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation_sync.py">get_latest_ton_amount_calculation_sync.py</a></td><td>87</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_ton_txns_api.py">get_ton_txns_api.py</a></td><td>55</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>calculator</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/calculator/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/calculator/operations.py">operations.py</a></td><td>9</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>staking</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/staking/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/staking/create_ton_stkrwd_cryptact_custom.py">create_ton_stkrwd_cryptact_custom.py</a></td><td>44</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>utils</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/config_loader.py">config_loader.py</a></td><td>20</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/ton_address_conv.py">ton_address_conv.py</a></td><td>10</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td><b>TOTAL</b></td><td><b>382</b></td><td><b>0</b></td><td><b>100%</b></td><td>&nbsp;</td></tr></tbody></table></details>

## Pytest Result Summary (os: ubuntu-latest / python-version: 3.13)
| Tests | Skipped | Failures | Errors | Time |
| ----- | ------- | -------- | -------- | ------------------ |
| 105 | 0 :zzz: | 0 :x: | 0 :fire: | 7.042s :stopwatch: |


## Coverage Report (os: windows-latest / python-version: 3.11)
<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/README.md"><img alt="coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen.svg" /></a><details><summary>Coverage Report (windows-latest / Python 3.11) </summary><table><tr><th>File</th><th>Stmts</th><th>Miss</th><th>Cover</th><th>Missing</th></tr><tbody><tr><td><a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>account</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation.py">get_latest_ton_amount_calculation.py</a></td><td>71</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation_async_aiohttp.py">get_latest_ton_amount_calculation_async_aiohttp.py</a></td><td>86</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation_sync.py">get_latest_ton_amount_calculation_sync.py</a></td><td>87</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_ton_txns_api.py">get_ton_txns_api.py</a></td><td>55</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>calculator</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/calculator/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/calculator/operations.py">operations.py</a></td><td>9</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>staking</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/staking/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/staking/create_ton_stkrwd_cryptact_custom.py">create_ton_stkrwd_cryptact_custom.py</a></td><td>44</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>utils</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/config_loader.py">config_loader.py</a></td><td>20</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/ton_address_conv.py">ton_address_conv.py</a></td><td>10</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td><b>TOTAL</b></td><td><b>382</b></td><td><b>0</b></td><td><b>100%</b></td><td>&nbsp;</td></tr></tbody></table></details>

## Pytest Result Summary (os: windows-latest / python-version: 3.11)
| Tests | Skipped | Failures | Errors | Time |
| ----- | ------- | -------- | -------- | ------------------ |
| 105 | 0 :zzz: | 0 :x: | 0 :fire: | 9.990s :stopwatch: |


## Coverage Report (os: windows-latest / python-version: 3.12)
<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/README.md"><img alt="coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen.svg" /></a><details><summary>Coverage Report (windows-latest / Python 3.12) </summary><table><tr><th>File</th><th>Stmts</th><th>Miss</th><th>Cover</th><th>Missing</th></tr><tbody><tr><td><a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>account</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation.py">get_latest_ton_amount_calculation.py</a></td><td>71</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation_async_aiohttp.py">get_latest_ton_amount_calculation_async_aiohttp.py</a></td><td>86</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation_sync.py">get_latest_ton_amount_calculation_sync.py</a></td><td>87</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_ton_txns_api.py">get_ton_txns_api.py</a></td><td>55</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>calculator</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/calculator/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/calculator/operations.py">operations.py</a></td><td>9</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>staking</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/staking/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/staking/create_ton_stkrwd_cryptact_custom.py">create_ton_stkrwd_cryptact_custom.py</a></td><td>44</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>utils</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/config_loader.py">config_loader.py</a></td><td>20</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/ton_address_conv.py">ton_address_conv.py</a></td><td>10</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td><b>TOTAL</b></td><td><b>382</b></td><td><b>0</b></td><td><b>100%</b></td><td>&nbsp;</td></tr></tbody></table></details>

## Pytest Result Summary (os: windows-latest / python-version: 3.12)
| Tests | Skipped | Failures | Errors | Time |
| ----- | ------- | -------- | -------- | ------------------ |
| 105 | 0 :zzz: | 0 :x: | 0 :fire: | 10.822s :stopwatch: |


## Coverage Report (os: windows-latest / python-version: 3.13)
<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/README.md"><img alt="coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen.svg" /></a><details><summary>Coverage Report (windows-latest / Python 3.13) </summary><table><tr><th>File</th><th>Stmts</th><th>Miss</th><th>Cover</th><th>Missing</th></tr><tbody><tr><td><a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>account</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation.py">get_latest_ton_amount_calculation.py</a></td><td>71</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation_async_aiohttp.py">get_latest_ton_amount_calculation_async_aiohttp.py</a></td><td>86</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation_sync.py">get_latest_ton_amount_calculation_sync.py</a></td><td>87</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_ton_txns_api.py">get_ton_txns_api.py</a></td><td>55</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>calculator</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/calculator/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/calculator/operations.py">operations.py</a></td><td>9</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>staking</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/staking/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/staking/create_ton_stkrwd_cryptact_custom.py">create_ton_stkrwd_cryptact_custom.py</a></td><td>44</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>utils</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/config_loader.py">config_loader.py</a></td><td>20</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/ton_address_conv.py">ton_address_conv.py</a></td><td>10</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td><b>TOTAL</b></td><td><b>382</b></td><td><b>0</b></td><td><b>100%</b></td><td>&nbsp;</td></tr></tbody></table></details>

## Pytest Result Summary (os: windows-latest / python-version: 3.13)
| Tests | Skipped | Failures | Errors | Time |
| ----- | ------- | -------- | -------- | ------------------ |
| 105 | 0 :zzz: | 0 :x: | 0 :fire: | 14.115s :stopwatch: |


## Coverage Report (os: macos-latest / python-version: 3.11)
<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/README.md"><img alt="coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen.svg" /></a><details><summary>Coverage Report (macos-latest / Python 3.11) </summary><table><tr><th>File</th><th>Stmts</th><th>Miss</th><th>Cover</th><th>Missing</th></tr><tbody><tr><td><a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>account</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation.py">get_latest_ton_amount_calculation.py</a></td><td>71</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation_async_aiohttp.py">get_latest_ton_amount_calculation_async_aiohttp.py</a></td><td>86</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation_sync.py">get_latest_ton_amount_calculation_sync.py</a></td><td>87</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_ton_txns_api.py">get_ton_txns_api.py</a></td><td>55</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>calculator</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/calculator/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/calculator/operations.py">operations.py</a></td><td>9</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>staking</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/staking/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/staking/create_ton_stkrwd_cryptact_custom.py">create_ton_stkrwd_cryptact_custom.py</a></td><td>44</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>utils</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/config_loader.py">config_loader.py</a></td><td>20</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/ton_address_conv.py">ton_address_conv.py</a></td><td>10</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td><b>TOTAL</b></td><td><b>382</b></td><td><b>0</b></td><td><b>100%</b></td><td>&nbsp;</td></tr></tbody></table></details>

## Pytest Result Summary (os: macos-latest / python-version: 3.11)
| Tests | Skipped | Failures | Errors | Time |
| ----- | ------- | -------- | -------- | ------------------ |
| 105 | 0 :zzz: | 0 :x: | 0 :fire: | 5.413s :stopwatch: |


## Coverage Report (os: macos-latest / python-version: 3.12)
<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/README.md"><img alt="coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen.svg" /></a><details><summary>Coverage Report (macos-latest / Python 3.12) </summary><table><tr><th>File</th><th>Stmts</th><th>Miss</th><th>Cover</th><th>Missing</th></tr><tbody><tr><td><a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>account</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation.py">get_latest_ton_amount_calculation.py</a></td><td>71</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation_async_aiohttp.py">get_latest_ton_amount_calculation_async_aiohttp.py</a></td><td>86</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation_sync.py">get_latest_ton_amount_calculation_sync.py</a></td><td>87</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_ton_txns_api.py">get_ton_txns_api.py</a></td><td>55</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>calculator</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/calculator/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/calculator/operations.py">operations.py</a></td><td>9</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>staking</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/staking/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/staking/create_ton_stkrwd_cryptact_custom.py">create_ton_stkrwd_cryptact_custom.py</a></td><td>44</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>utils</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/config_loader.py">config_loader.py</a></td><td>20</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/ton_address_conv.py">ton_address_conv.py</a></td><td>10</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td><b>TOTAL</b></td><td><b>382</b></td><td><b>0</b></td><td><b>100%</b></td><td>&nbsp;</td></tr></tbody></table></details>

## Pytest Result Summary (os: macos-latest / python-version: 3.12)
| Tests | Skipped | Failures | Errors | Time |
| ----- | ------- | -------- | -------- | ------------------ |
| 105 | 0 :zzz: | 0 :x: | 0 :fire: | 6.813s :stopwatch: |


## Coverage Report (os: macos-latest / python-version: 3.13)
<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/README.md"><img alt="coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen.svg" /></a><details><summary>Coverage Report (macos-latest / Python 3.13) </summary><table><tr><th>File</th><th>Stmts</th><th>Miss</th><th>Cover</th><th>Missing</th></tr><tbody><tr><td><a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>account</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation.py">get_latest_ton_amount_calculation.py</a></td><td>71</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation_async_aiohttp.py">get_latest_ton_amount_calculation_async_aiohttp.py</a></td><td>86</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_latest_ton_amount_calculation_sync.py">get_latest_ton_amount_calculation_sync.py</a></td><td>87</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/account/get_ton_txns_api.py">get_ton_txns_api.py</a></td><td>55</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>calculator</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/calculator/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/calculator/operations.py">operations.py</a></td><td>9</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>staking</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/staking/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/staking/create_ton_stkrwd_cryptact_custom.py">create_ton_stkrwd_cryptact_custom.py</a></td><td>44</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>utils</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/__init__.py">\_\_init\_\_.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/config_loader.py">config_loader.py</a></td><td>20</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/7rikazhexde/python-project-sandbox/blob/1bccd70dd3f2fe9a0f775c1bf6d86f392e3a518f/project_a/utils/ton_address_conv.py">ton_address_conv.py</a></td><td>10</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td><b>TOTAL</b></td><td><b>382</b></td><td><b>0</b></td><td><b>100%</b></td><td>&nbsp;</td></tr></tbody></table></details>

## Pytest Result Summary (os: macos-latest / python-version: 3.13)
| Tests | Skipped | Failures | Errors | Time |
| ----- | ------- | -------- | -------- | ------------------ |
| 105 | 0 :zzz: | 0 :x: | 0 :fire: | 5.992s :stopwatch: |


