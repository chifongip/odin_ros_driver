"""Offline checks; missing config exits before device SDK initialization."""

import os
from pathlib import Path
import subprocess

from ament_index_python.packages import get_package_prefix


def test_missing_custom_config_exits_before_connecting(tmp_path):
    executable = Path(get_package_prefix("odin_ros_driver")) / "lib/odin_ros_driver/host_sdk_sample"
    missing = tmp_path / "does_not_exist.yaml"
    environment = dict(os.environ, ROS_DOMAIN_ID="96", ROS_LOG_DIR=str(tmp_path / "logs"))
    environment.pop("FASTRTPS_DEFAULT_PROFILES_FILE", None)
    result = subprocess.run(
        [str(executable), "--ros-args", "-p", f"config_file:={missing}", "-r", "/tf:=/test/odin/tf"],
        capture_output=True, text=True, timeout=15, env=environment,
    )
    assert result.returncode == 255
    assert f"Failed to load config file: {missing}" in result.stdout + result.stderr
