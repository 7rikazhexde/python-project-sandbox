from pathlib import Path
from typing import Any, Union


def pytest_ignore_collect(path: Union[str, Path], config: Any) -> bool:
    """
    特定のファイルをテスト収集から除外するための pytest フック関数。

    この関数は、pytest がテストを収集する際に各ファイルに対して呼び出されます。
    'project_a/staking/ton_whales_staking_dashboard.py' ファイルを
    テスト対象から除外するために使用されます。

    注意: このファイルはカバレッジレポートからも除外されています（pyproject.toml の設定による）。

    Args:
        path (Union[str, Path]): チェック対象のファイルパス
        config (Any): pytest の設定オブジェクト（この関数では使用しない）

    Returns:
        bool: 指定されたパスが除外対象の場合は True、そうでない場合は False
    """
    excluded_file = Path("project_a/staking/ton_whales_staking_dashboard.py")
    return excluded_file.parts[-3:] == Path(path).parts[-3:]