"""Unit tests for the report-only boundary checker (no repository import)."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

import check_boundaries as cb


def make_repo(tmp_path: Path, name: str, files: dict[str, str], manifest: dict | None = None) -> cb.Repo:
    path = tmp_path / name
    path.mkdir()
    if manifest is not None:
        (path / "capability.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
    for rel, text in files.items():
        target = path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    repo = cb.Repo(name, path, cb.LAYERS.get(name, "?"), None)
    cb.load_manifest(repo)
    return repo


def v1_manifest(**overrides):
    data = {
        "schema_version": 1,
        "name": "jcheng-example",
        "version": "0.1.0",
        "contract": {
            "interfaces": ">=0.2,<0.3",
            "contract_hash": "sha256:" + "a" * 64,
            "system_api": ">=0.2,<0.4",
        },
        "safety": {
            "class": "offline",
            "scopes": [],
            "requires_lease": True,
            "max_rate_hz": 1,
            "deadman_ms": 500,
        },
        "hardware_access": "none",
        "runtime": {"ros_domains": [], "publishes": [], "subscribes": []},
    }
    data.update(overrides)
    return data


def test_allowed_edges():
    assert cb.allowed_edge("L4", "L2")
    assert cb.allowed_edge("L4", "L1")
    assert cb.allowed_edge("L3", "L2")
    assert cb.allowed_edge("L2", "L1")
    assert not cb.allowed_edge("L4", "L3")
    assert not cb.allowed_edge("L2", "L3")
    assert not cb.allowed_edge("SCEN", "L3")


def test_b2_flags_device_token_when_access_none(tmp_path):
    repo = make_repo(tmp_path, "jcheng-scenarios", {"src/x.py": "port = serial.Serial('/dev/ttyUSB0')\n"}, v1_manifest())
    findings = cb.rule_b2(repo)
    assert findings and {f.rule for f in findings} == {"B2"}
    assert all(f.severity == "Critical" for f in findings)


def test_b2_ignores_readonly_camera_declaration(tmp_path):
    manifest = v1_manifest()
    manifest["hardware_access"] = "camera_readonly"
    repo = make_repo(tmp_path, "jcheng-perception", {"src/x.py": "import cv2\n"}, manifest)
    assert cb.rule_b2(repo) == []


def test_b4_flags_execution_token_outside_system(tmp_path):
    repo = make_repo(
        tmp_path,
        "jcheng-studio",
        {"backend/app/adapters/hardware.py": "URL = '/motion/dispatch'\n"},
        v1_manifest(),
    )
    findings = cb.rule_b4(repo, {})
    assert findings and findings[0].severity == "Critical"


def test_b4_allows_system(tmp_path):
    repo = make_repo(
        tmp_path,
        "jcheng-system",
        {"ros2_ws/src/x.py": "URL = '/servo_controller'\n"},
        v1_manifest(),
    )
    assert cb.rule_b4(repo, {}) == []


def test_b5_flags_legacy_manifest(tmp_path):
    repo = make_repo(tmp_path, "jcheng-benchmark", {}, {"name": "jcheng-benchmark", "version": "0.1.0"})
    findings = cb.rule_b5(repo)
    assert findings and findings[0].rule == "B5"


def test_b5_accepts_v1(tmp_path):
    repo = make_repo(tmp_path, "jcheng-scenarios", {}, v1_manifest())
    assert cb.rule_b5(repo) == []


def test_b7_requires_ownership_file(tmp_path):
    repo = make_repo(
        tmp_path,
        "jcheng-scenarios",
        {"schemas/a.v1.schema.json": "{}"},
        v1_manifest(),
    )
    findings = cb.rule_b7(repo)
    assert findings and findings[0].rule == "B7"


def test_b7_accepts_declared_schema(tmp_path):
    repo = make_repo(
        tmp_path,
        "jcheng-scenarios",
        {
            "schemas/a.v1.schema.json": "{}",
            "SCHEMA_OWNERSHIP.md": "| `schemas/a.v1.schema.json` | `repo-local` |\n",
        },
        v1_manifest(),
    )
    assert cb.rule_b7(repo) == []


def test_b8_flags_device_copy_without_reference(tmp_path):
    repo = make_repo(
        tmp_path,
        "jcheng-simulation",
        {
            "ros2_ws/src/jcheng_simulation_robots/robots/armpi_ultra/robot.yaml": "joints: []\n",
        },
        v1_manifest(),
    )
    findings = cb.rule_b8(repo)
    assert any(f.rule == "B8" for f in findings)


def test_b8_accepts_referenced_copy(tmp_path):
    repo = make_repo(
        tmp_path,
        "jcheng-simulation",
        {
            "ros2_ws/src/jcheng_simulation_robots/robots/armpi_ultra/robot.yaml": "source_device: hiwonder.armpi-ultra@0.1.0\n",
        },
        v1_manifest(),
    )
    assert cb.rule_b8(repo) == []


def test_b4_flags_cmd_vel_without_base_intake(tmp_path):
    manifest = v1_manifest()
    manifest["runtime"] = {
        "ros_domains": [42],
        "publishes": ["/cmd_vel"],
        "subscribes": ["/scan"],
    }
    repo = make_repo(tmp_path, "jcheng-mobile", {}, manifest)
    findings = cb.rule_b4(repo, {})
    assert any(f.severity == "Critical" and "/cmd_vel" in f.message for f in findings)


def test_b6_flags_deployed_tree_mismatch(tmp_path):
    repo = make_repo(
        tmp_path,
        "jcheng-system",
        {
            "configs/contract.yaml": "interfaces:\n  contract:\n    contract_hash: sha256:" + "a" * 64 + "\n",
            "deploy/armpi-ultra/evidence/20261127-r10/contract.json": '{"contract": {"contract_hash": "sha256:'
            + "b" * 64
            + '"}}',
        },
        None,
    )
    findings = cb.rule_b6(repo, None)
    assert any(f.rule == "B6" and f.severity == "High" for f in findings)


def test_b8_flags_hardcoded_gripper_range(tmp_path):
    repo = make_repo(
        tmp_path,
        "jcheng-applications",
        {"src/jcheng_applications/model.py": "if not 0.0 <= position <= 2.22: pass  # position_rad\n"},
        v1_manifest(),
    )
    findings = cb.rule_b8(repo)
    assert any("hardcoded" in f.message for f in findings)


def test_b9_flags_head_reference(tmp_path):
    repo = make_repo(
        tmp_path,
        "jcheng-system",
        {"docs/x.md": "see jcheng-manipulation HEAD for the runner\n"},
        v1_manifest(),
    )
    findings = cb.rule_b9(repo)
    assert findings and findings[0].rule == "B9"


def test_b9_accepts_tag_reference(tmp_path):
    repo = make_repo(
        tmp_path,
        "jcheng-system",
        {"docs/x.md": "see jcheng-manipulation@v1.0.0 (b3411e4)\n"},
        v1_manifest(),
    )
    assert cb.rule_b9(repo) == []


def test_report_mode_writes_outputs_and_exits_zero(tmp_path):
    make_repo(tmp_path, "jcheng-scenarios", {}, v1_manifest())
    out = tmp_path / "out"
    assert cb.main(["--root", str(tmp_path), "--out", str(out)]) == 0
    assert (out / "boundary-report.json").is_file()
    assert (out / "boundary-report.md").is_file()
