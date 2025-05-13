import enum
import os
import subprocess
from datetime import timedelta

import pytest
from dagster import AssetKey, DagsterInstance
from dagster._time import get_current_datetime
from dbt_example.dagster_defs.utils import get_airflow_instance

from dbt_example_tests.integration_tests.conftest import makefile_dir


class DagsterDevCmd(enum.Enum):
    PEER = "PEER"
    OBSERVE = "OBSERVE"
    MIGRATE = "MIGRATE"
    OBSERVE_WITH_CHECK = "OBSERVE_WITH_CHECK"

    @property
    def as_cmd(self) -> list[str]:
        if self == DagsterDevCmd.PEER:
            cmd = ["make", "run_peer"]
        elif self == DagsterDevCmd.OBSERVE:
            cmd = ["make", "run_observe"]
        else:
            cmd = ["make", "run_migrate"]
        return cmd + ["-C", str(makefile_dir())]

    @property
    def test_id(self) -> str:
        return self.value.lower()


def make_unmigrated() -> None:
    subprocess.check_output(["make", "not_proxied", "-C", str(makefile_dir())])


@pytest.fixture(name="dagster_home")
def dagster_home_fixture(local_env: None) -> str:
    return os.environ["DAGSTER_HOME"]


@pytest.fixture(name="stage")
def stage_fixture(request) -> DagsterDevCmd:
    return request.param


@pytest.fixture(name="dagster_dev_cmd")
def dagster_dev_cmd_fixture(stage: DagsterDevCmd) -> list[str]:
    return stage.as_cmd


@pytest.mark.parametrize(
    "stage",
    [stage for stage in DagsterDevCmd],
    ids=[stage.test_id for stage in DagsterDevCmd],
    indirect=True,
)
def test_dagster_materializes(
    airflow_instance: None,
    dagster_dev: None,
    dagster_home: str,
    stage: DagsterDevCmd,
) -> None:
    """Test that assets can load properly, and that materializations register."""
    if stage == DagsterDevCmd.PEER:
        make_unmigrated()
    af_instance = get_airflow_instance()
    for dag_id, expected_asset_key in [("rebuild_iris_models", AssetKey(["lakehouse", "iris"]))]:
        run_id = af_instance.trigger_dag(dag_id=dag_id)
        af_instance.wait_for_run_completion(dag_id=dag_id, run_id=run_id, timeout=60)
        dagster_instance = DagsterInstance.get()
        start_time = get_current_datetime()
        while get_current_datetime() - start_time < timedelta(seconds=30):
            asset_materialization = dagster_instance.get_latest_materialization_event(
                asset_key=AssetKey(["my_airflow_instance", "dag", dag_id])
            )
            if asset_materialization:
                break

        assert asset_materialization  # pyright: ignore[reportPossiblyUnboundVariable]

        if stage == DagsterDevCmd.OBSERVE or stage == DagsterDevCmd.MIGRATE:
            asset_materialization = dagster_instance.get_latest_materialization_event(
                asset_key=expected_asset_key
            )
            assert asset_materialization
