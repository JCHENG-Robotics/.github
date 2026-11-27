#!/usr/bin/env python3
"""Report-only boundary checker for the JCHENG Robotics ecosystem.

Design: .github/docs/boundary-consolidation/08-check-boundaries-design.md
Rules:  B1-B11 (report-only). The checker never imports a target repository,
never starts ROS/DDS, never opens a device and never writes outside its output
directory. It always exits 0 in report mode.

Usage:
    python3 check_boundaries.py --root /home/jerichocheng/jcheng --mode report
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError:  # pragma: no cover - environment guard
    print("check_boundaries requires PyYAML", file=sys.stderr)
    sys.exit(2)

PRODUCT_REPOS = (
    ".github",
    "jcheng-interfaces",
    "jcheng-system",
    "jcheng-manipulation",
    "jcheng-mobile",
    "jcheng-perception",
    "jcheng-learning",
    "jcheng-teleop",
    "jcheng-devices",
    "jcheng-simulation",
    "jcheng-scenarios",
    "jcheng-studio",
    "jcheng-applications",
    "jcheng-benchmark",
    "jcheng-ops",
    "jcheng-research",
)

LAYERS = {
    "jcheng-interfaces": "L1",
    "jcheng-system": "L2",
    "jcheng-manipulation": "FROZEN",
    "jcheng-mobile": "L3",
    "jcheng-perception": "L3",
    "jcheng-learning": "L3",
    "jcheng-teleop": "L3",
    "jcheng-devices": "DEV",
    "jcheng-simulation": "SIM",
    "jcheng-scenarios": "SCEN",
    "jcheng-studio": "L4",
    "jcheng-applications": "L4",
    "jcheng-benchmark": "BENCH",
    "jcheng-ops": "OPS",
    "jcheng-research": "RESEARCH",
    ".github": "L0",
}

MODULE_REPO = {
    "jcheng_interfaces": "jcheng-interfaces",
    "jcheng_contracts": "jcheng-interfaces",
    "jcheng_system_core": "jcheng-system",
    "jcheng_safety": "jcheng-system",
    "jcheng_authority": "jcheng-system",
    "jcheng_motion": "jcheng-system",
    "jcheng_gateway": "jcheng-system",
    "jcheng_guard": "jcheng-system",
    "jcheng_hardware": "jcheng-system",
    "jcheng_telemetry": "jcheng-system",
    "jcheng_runtime": "jcheng-system",
    "jcheng_vendor": "jcheng-system",
    "jcheng_moveit": "jcheng-system",
    "jcheng_bringup": "jcheng-system",
    "jcheng_testkit": "jcheng-system",
    "jcheng_mobile": "jcheng-mobile",
    "jcheng_mobile_bringup": "jcheng-mobile",
    "jcheng_perception": "jcheng-perception",
    "jcheng_perception_core": "jcheng-perception",
    "jcheng_perception_edge": "jcheng-perception",
    "jcheng_perception_gpu": "jcheng-perception",
    "jcheng_perception_msgs": "jcheng-perception",
    "jcheng_perception_scene": "jcheng-perception",
    "jcheng_learning": "jcheng-learning",
    "jcheng_teleop": "jcheng-teleop",
    "jcheng_teleop_ros": "jcheng-teleop",
    "jcheng_devices": "jcheng-devices",
    "jcheng_simulation": "jcheng-simulation",
    "jcheng_simulation_robots": "jcheng-simulation",
    "jcheng_simulation_arm": "jcheng-simulation",
    "jcheng_simulation_bringup": "jcheng-simulation",
    "jcheng_scenarios": "jcheng-scenarios",
    "jcheng_applications": "jcheng-applications",
    "jcheng_benchmark": "jcheng-benchmark",
}

EXECUTION_TOKENS = (
    "/servo_controller",
    "set_motor_speeds",
    "/motion/dispatch",
    "ExecuteMotion",
    "create_client(ExecuteMotion",
)
HARDWARE_TOKENS = (
    "/dev/tty",
    "pyserial",
    "serial.Serial",
    "socketcan",
    "cv2.VideoCapture",
    "pigpio",
    "RPi.GPIO",
)
MOTION_TOPICS = ("/cmd_vel", "/jcheng/intent/base", "/jcheng/intent/teleop")

DEVICE_COPY_FILES = (
    "jcheng-system/configs/robots/armpi_ultra/profile.yaml",
    "jcheng-simulation/ros2_ws/src/jcheng_simulation_robots/robots/armpi_ultra/robot.yaml",
    "jcheng-learning/src/jcheng_learning/profiles/armpi_ultra.yaml",
    "jcheng-studio/configs/joint_mapping.yaml",
    "jcheng-studio/configs/takeover.yaml",
    "jcheng-teleop/examples/armpi_ultra_demo/profile.yaml",
)
SCENARIO_COPY_FILES = (
    "jcheng-system/ros2_ws/src/jcheng_system_core/jcheng_system_core/scenarios.py",
    "jcheng-benchmark/benchmarks/suites/template-success-rate.yaml",
    "jcheng-simulation/ros2_ws/src/jcheng_simulation_robots/robots/armpi_ultra/worlds/jcheng_lab.sdf",
    "jcheng-applications/recipes/example-supervised-transfer.yaml",
    "jcheng-perception/ros2_ws/src/jcheng_perception_core/jcheng_perception_core/types.py",
)


@dataclass
class Finding:
    rule: str
    severity: str
    repo: str
    evidence: str
    message: str
    suggestion: str
    waiver: str | None = None

    @property
    def status(self) -> str:
        return "waived" if self.waiver else "open"

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule": self.rule,
            "severity": self.severity,
            "repo": self.repo,
            "evidence": self.evidence,
            "message": self.message,
            "suggestion": self.suggestion,
            "waiver": self.waiver,
            "status": self.status,
        }


@dataclass
class Repo:
    name: str
    path: Path
    layer: str
    manifest: dict[str, Any] | None
    manifest_error: str | None = None
    findings: list[Finding] = field(default_factory=list)

    @property
    def is_git(self) -> bool:
        return (self.path / ".git").exists()


def load_manifest(repo: Repo) -> None:
    path = repo.path / "capability.yaml"
    if not path.is_file():
        return
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as error:  # noqa: BLE001 - report, do not crash
        repo.manifest_error = str(error)
        return
    if isinstance(data, dict):
        repo.manifest = data


SKIP_DIRS = {
    ".git",
    "build",
    "install",
    "log",
    "__pycache__",
    ".venv",
    ".venv-ci",
    "node_modules",
    ".pytest_cache",
    ".worktrees",
    ".git-safety",
}


def iter_files(repo: Repo, suffix: str) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(repo.path):
        dirnames[:] = [name for name in dirnames if name not in SKIP_DIRS]
        for filename in filenames:
            if filename.endswith(suffix):
                yield Path(dirpath) / filename


def iter_python(repo: Repo) -> Iterable[Path]:
    for path in iter_files(repo, ".py"):
        if {"tests", "test"} & set(path.parts):
            continue
        yield path


def imports(path: Path) -> set[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError:
        return set()
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module.split(".")[0])
    return found


def allowed_edge(source_layer: str, target_layer: str) -> bool:
    if source_layer == "L4":
        return target_layer in {"L1", "L2"}
    if source_layer == "L3":
        return target_layer in {"L1", "L2"}
    if source_layer == "L2":
        return target_layer in {"L1"}
    if source_layer in {"OPS", "BENCH", "SCEN", "DEV", "SIM", "RESEARCH", "L0", "FROZEN"}:
        return target_layer in {"L1"}
    return False


def rule_b1(repo: Repo, all_repos: dict[str, Repo]) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_python(repo):
        for module in imports(path):
            target = MODULE_REPO.get(module)
            if not target or target == repo.name or target not in all_repos:
                continue
            target_layer = all_repos[target].layer
            if not allowed_edge(repo.layer, target_layer):
                rel = path.relative_to(repo.path)
                findings.append(
                    Finding(
                        "B1",
                        "High",
                        repo.name,
                        f"{rel}: import {module} ({target})",
                        f"{repo.layer} imports {target_layer} module {module}",
                        "Move the call to an HTTP/WS contract or a reviewed L1/L2 client",
                    )
                )
    return findings


def rule_b2(repo: Repo) -> list[Finding]:
    findings: list[Finding] = []
    access = None
    if repo.manifest and isinstance(repo.manifest.get("hardware_access"), str):
        access = repo.manifest["hardware_access"]
    elif repo.manifest and isinstance(repo.manifest.get("hardware_access"), dict):
        access = repo.manifest["hardware_access"].get("kind")
    if access not in {"none"}:
        return findings
    for path in iter_python(repo):
        text = path.read_text(encoding="utf-8", errors="replace")
        for token in HARDWARE_TOKENS:
            if token in text:
                findings.append(
                    Finding(
                        "B2",
                        "Critical",
                        repo.name,
                        f"{path.relative_to(repo.path)}: {token}",
                        f"hardware_access=none but device token {token!r} appears",
                        "Remove the device path or change the manifest with a review",
                    )
                )
    return findings


def rule_b3(repo: Repo) -> list[Finding]:
    findings: list[Finding] = []
    if not repo.manifest:
        return findings
    runtime = repo.manifest.get("runtime")
    if not isinstance(runtime, dict):
        return findings
    empty = not runtime.get("ros_domains") and not runtime.get("publishes")
    if not empty:
        return findings
    for path in iter_python(repo):
        text = path.read_text(encoding="utf-8", errors="replace")
        if "create_publisher" in text or "create_subscription" in text:
            findings.append(
                Finding(
                    "B3",
                    "High",
                    repo.name,
                    str(path.relative_to(repo.path)),
                    "manifest declares an empty runtime but code creates a ROS publisher/subscriber",
                    "Declare the runtime surface or move the publisher to a test-only harness",
                )
            )
            break
    return findings


def rule_b4(repo: Repo, all_repos: dict[str, Repo]) -> list[Finding]:
    findings: list[Finding] = []
    if repo.name in {"jcheng-system", ".github", "jcheng-manipulation"}:
        return findings
    for path in iter_python(repo):
        if {"docs", "original"} <= set(path.parts) or "tools" in path.parts and "legacy" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for token in EXECUTION_TOKENS:
            if token in text:
                findings.append(
                    Finding(
                        "B4",
                        "Critical",
                        repo.name,
                        f"{path.relative_to(repo.path)}: {token}",
                        f"execution token {token!r} appears outside jcheng-system",
                        "Remove the path or route it through the system gateway with a lease",
                    )
                )
    if repo.manifest:
        runtime = repo.manifest.get("runtime")
        if isinstance(runtime, dict):
            publishes = runtime.get("publishes") or []
            if any("/cmd_vel" in str(topic) for topic in publishes):
                findings.append(
                    Finding(
                        "B4",
                        "Critical",
                        repo.name,
                        "capability.yaml",
                        "/cmd_vel is declared as a publish surface without a system base intake",
                        "Publish /jcheng/intent/base with a lease, or remove /cmd_vel",
                    )
                )
    return findings


def rule_b5(repo: Repo) -> list[Finding]:
    if repo.name in {".github", "jcheng-research", "jcheng-manipulation"}:
        return []
    if not repo.manifest:
        return [
            Finding(
                "B5",
                "High" if repo.name in {"jcheng-system", "jcheng-interfaces"} else "Medium",
                repo.name,
                "capability.yaml",
                "no capability manifest",
                "Add capability-manifest.v1 or record the exception",
            )
        ]
    top = set(repo.manifest)
    expected = {"schema_version", "name", "version", "contract", "safety", "hardware_access", "runtime"}
    if top != expected:
        return [
            Finding(
                "B5",
                "Medium",
                repo.name,
                "capability.yaml",
                f"manifest uses a non-v1 shape (keys: {sorted(top)})",
                "Migrate to capability-manifest.v1; keep free-form notes in docs",
            )
        ]
    return []


def git(repo: Repo, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo.path), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip()


def rule_b6(repo: Repo, interfaces: Repo | None) -> list[Finding]:
    findings: list[Finding] = []

    if repo.name == "jcheng-system":
        deployed = repo.path / "deploy/armpi-ultra/evidence/20261127-r10/contract.json"
        dev = repo.path / "configs/contract.yaml"
        if deployed.is_file() and dev.is_file():
            try:
                deployed_hash = json.loads(deployed.read_text(encoding="utf-8"))["contract"]["contract_hash"]
                dev_hash = (yaml.safe_load(dev.read_text(encoding="utf-8")) or {}).get("interfaces", {}).get("contract", {}).get("contract_hash")
            except Exception:  # noqa: BLE001
                deployed_hash = dev_hash = None
            if deployed_hash and dev_hash and deployed_hash != dev_hash:
                findings.append(
                    Finding(
                        "B6",
                        "High",
                        repo.name,
                        "deploy/armpi-ultra/evidence/20261127-r10/contract.json",
                        "deployed contract hash differs from the development tree",
                        "Reconcile the deployed and development trees before any hardware claim",
                    )
                )

    if not repo.manifest or not isinstance(repo.manifest.get("contract"), dict):
        return findings
    pin = repo.manifest["contract"]
    hash_value = pin.get("contract_hash")
    if not hash_value:
        return findings
    known: set[str] = set()
    if interfaces:
        manifest_path = interfaces.path / "interface_manifest.json"
        if manifest_path.is_file():
            try:
                known.add(json.loads(manifest_path.read_text())["contract_hash"])
            except Exception:  # noqa: BLE001
                pass
        tags = git(interfaces, "tag", "--list").splitlines()
        for tag in tags:
            raw = git(interfaces, "show", f"{tag}:interface_manifest.json")
            if raw:
                try:
                    known.add(json.loads(raw)["contract_hash"])
                except Exception:  # noqa: BLE001
                    continue
    if known and hash_value not in known:
        findings.append(
            Finding(
                "B6",
                "High",
                repo.name,
                "capability.yaml",
                f"contract_hash {hash_value[:18]}… does not match a released interfaces tag",
                "Pin a released tag and update the lock together",
            )
        )

    lock_path = repo.path.parent / "jcheng-system/locks/ecosystem.lock.yaml"
    if lock_path.is_file():
        try:
            lock = yaml.safe_load(lock_path.read_text(encoding="utf-8")) or {}
        except Exception:  # noqa: BLE001
            lock = {}
        module = (lock.get("modules") or {}).get(repo.name)
        if isinstance(module, dict):
            lock_range = module.get("interfaces")
            if lock_range and pin.get("interfaces") != lock_range:
                findings.append(
                    Finding(
                        "B6",
                        "High",
                        repo.name,
                        "capability.yaml",
                        f"interfaces range {pin.get('interfaces')} differs from lock {lock_range}",
                        "Align the manifest and the lock in one release",
                    )
                )
            lock_version = module.get("version")
            if lock_version and str(repo.manifest.get("version")) != str(lock_version):
                findings.append(
                    Finding(
                        "B6",
                        "Medium",
                        repo.name,
                        "capability.yaml",
                        f"version {repo.manifest.get('version')} differs from lock {lock_version}",
                        "Update the lock when the repository releases",
                    )
                )
    return findings


def rule_b7(repo: Repo) -> list[Finding]:
    schemas = list(iter_files(repo, ".schema.json"))
    if not schemas:
        return []
    ownership = repo.path / "SCHEMA_OWNERSHIP.md"
    if not ownership.is_file():
        return [
            Finding(
                "B7",
                "Medium",
                repo.name,
                "SCHEMA_OWNERSHIP.md",
                f"{len(schemas)} schema file(s) without an ownership declaration",
                "Add SCHEMA_OWNERSHIP.md with owner, status and consumers",
            )
        ]
    text = ownership.read_text(encoding="utf-8", errors="replace")
    findings: list[Finding] = []
    for path in schemas:
        rel = str(path.relative_to(repo.path))
        if f"`{rel}`" not in text:
            findings.append(
                Finding(
                    "B7",
                    "Medium",
                    repo.name,
                    rel,
                    "schema file is not declared in SCHEMA_OWNERSHIP.md",
                    f"Declare {rel} with owner, status and consumers",
                )
            )
    return findings


def rule_b8(repo: Repo) -> list[Finding]:
    findings: list[Finding] = []
    root = repo.path.parent
    for rel in DEVICE_COPY_FILES:
        if not rel.startswith(repo.name + "/"):
            continue
        path = root / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if not re.search(r"(source_device|device_id|source_hashes|profile_version)", text):
            findings.append(
                Finding(
                    "B8",
                    "High",
                    repo.name,
                    rel,
                    "device facts are copied without a device_id/version/hash reference",
                    "Cite devices registry id@version#sha256 or generate the copy",
                )
            )
    for rel in SCENARIO_COPY_FILES:
        if not rel.startswith(repo.name + "/"):
            continue
        path = root / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if re.search(r"(success_conditions|at_least_rad|at_most_rad|class Phase)", text) and "scenario_id" not in text:
            findings.append(
                Finding(
                    "B8",
                    "High",
                    repo.name,
                    rel,
                    "task/success semantics are defined outside jcheng-scenarios without scenario_id",
                    "Reference scenario_id@version or rename to a conformance case",
                )
            )
    if repo.name == "jcheng-applications":
        model = repo.path / "src/jcheng_applications/model.py"
        if model.is_file():
            text = model.read_text(encoding="utf-8", errors="replace")
            if "2.22" in text and "position_rad" in text:
                findings.append(
                    Finding(
                        "B8",
                        "High",
                        repo.name,
                        "src/jcheng_applications/model.py",
                        "gripper range is hardcoded instead of referencing a device profile",
                        "Reference the devices gripper profile or a deployed robot profile",
                    )
                )
    return findings


def rule_b9(repo: Repo) -> list[Finding]:
    findings: list[Finding] = []
    if repo.name == ".github":
        return findings
    for path in iter_files(repo, ".md"):
        for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if "jcheng-manipulation" not in line:
                continue
            if not re.search(r"(@main|@master|\bHEAD\b|branch\s+main)", line):
                continue
            if re.search(r"\b[0-9a-f]{7,40}\b", line):
                continue
            findings.append(
                Finding(
                    "B9",
                    "Medium",
                    repo.name,
                    f"{path.relative_to(repo.path)}:{number}",
                    "frozen baseline reference uses a moving ref (HEAD/branch)",
                    "Use jcheng-manipulation@v1.0.0 (b3411e4) + evidence path",
                )
            )
    return findings


def rule_b10(repo: Repo) -> list[Finding]:
    findings: list[Finding] = []
    root = repo.path.parent
    for rel in DEVICE_COPY_FILES:
        if not rel.startswith(repo.name + "/"):
            continue
        path = root / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "source_hashes" not in text and "source_device" not in text and "provenance" not in text:
            findings.append(
                Finding(
                    "B10",
                    "Medium",
                    repo.name,
                    rel,
                    "copy has no provenance marker (source/hash/version)",
                    "Add source reference and hash, or generate the file",
                )
            )
    return findings


def rule_b11(repo: Repo, audit_file: Path) -> list[Finding]:
    if not repo.is_git:
        return []
    findings: list[Finding] = []
    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    if branch in {"main", "master"}:
        ahead = git(repo, "rev-list", "--count", "origin/main..HEAD") if git(repo, "rev-parse", "--verify", "origin/main") else "?"
        dirty = git(repo, "status", "--porcelain")
        if ahead not in {"0", "?"} or dirty:
            findings.append(
                Finding(
                    "B11",
                    "High",
                    repo.name,
                    f"branch={branch}",
                    "work is on the default branch with local commits or changes",
                    "Move to a feature branch before editing",
                )
            )
    merges = git(repo, "log", "--merges", "--oneline", "-5")
    merges = "\n".join(
        line for line in merges.splitlines()
        if "Merge origin/main" not in line and "Merge remote-tracking" not in line
    )
    if merges and branch not in {"main", "master"}:
        findings.append(
            Finding(
                "B11",
                "Low",
                repo.name,
                f"branch={branch}",
                f"merge commits on a feature branch: {merges.splitlines()[0]}",
                "Prefer rebase/cherry-pick or document the merge",
            )
        )
    upstream = git(repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    if upstream == "origin/main" and branch not in {"main", "master"}:
        findings.append(
            Finding(
                "B11",
                "Medium",
                repo.name,
                f"upstream={upstream}",
                "feature branch tracks origin/main; a bare git push would target main",
                "Set the upstream to a dedicated remote branch",
            )
        )
    if repo.name == ".github" and not audit_file.is_file():
        findings.append(
            Finding(
                "B11",
                "Low",
                repo.name,
                "docs/boundary-consolidation/09-git-operation-audit.md",
                "Git operation audit evidence is missing",
                "Record the Git operation audit before the next phase",
            )
        )
    return findings


def apply_waivers(findings: list[Finding], waiver_path: Path) -> list[dict[str, Any]]:
    """Apply unexpired waivers that match rule, repo and evidence."""
    entries: list[dict[str, Any]] = []
    if waiver_path.is_file():
        try:
            data = yaml.safe_load(waiver_path.read_text(encoding="utf-8")) or {}
        except Exception:  # noqa: BLE001
            data = {}
        for entry in data.get("waivers", []) or []:
            if not isinstance(entry, dict):
                continue
            expires = entry.get("expires")
            if expires:
                try:
                    if date.fromisoformat(str(expires)) < date.today():
                        continue
                except ValueError:
                    continue
            entries.append(entry)
    for finding in findings:
        for entry in entries:
            if entry.get("rule") != finding.rule or entry.get("repo") != finding.repo:
                continue
            evidence = entry.get("evidence")
            if evidence and str(evidence) not in finding.evidence:
                continue
            finding.waiver = entry.get("id")
            break
    return entries


def check(root: Path, mode: str) -> dict[str, Any]:
    repos: dict[str, Repo] = {}
    for name in PRODUCT_REPOS:
        path = root / name
        if not path.is_dir():
            continue
        repo = Repo(name, path, LAYERS.get(name, "?"), None)
        load_manifest(repo)
        repos[name] = repo

    audit_file = root / ".github/docs/boundary-consolidation/09-git-operation-audit.md"
    findings: list[Finding] = []
    for repo in repos.values():
        findings += rule_b1(repo, repos)
        findings += rule_b2(repo)
        findings += rule_b3(repo)
        findings += rule_b4(repo, repos)
        findings += rule_b5(repo)
        findings += rule_b6(repo, repos.get("jcheng-interfaces"))
        findings += rule_b7(repo)
        findings += rule_b8(repo)
        findings += rule_b9(repo)
        findings += rule_b10(repo)
        findings += rule_b11(repo, audit_file)

    apply_waivers(findings, root / ".github/boundary-waivers.yaml")

    summary: dict[str, int] = {}
    for finding in findings:
        key = finding.status
        summary[key] = summary.get(key, 0) + 1
    return {
        "schema_version": "check-boundaries.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "mode": mode,
        "repos": [
            {
                "name": repo.name,
                "layer": repo.layer,
                "manifest": "v1" if repo.manifest and "schema_version" in repo.manifest else ("legacy" if repo.manifest else "none"),
            }
            for repo in repos.values()
        ],
        "findings": [finding.to_dict() for finding in findings],
        "summary": summary,
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# Boundary check report",
        "",
        f"- Generated: {report['generated_at']}",
        f"- Root: `{report['root']}`",
        f"- Mode: **{report['mode']}** (report-only; this is not a runtime proof)",
        "",
        "## Summary",
        "",
        "| Status | Count |",
        "|---|---|",
    ]
    for key, value in sorted(report["summary"].items()):
        lines.append(f"| {key} | {value} |")
    lines += ["", "## Findings", "", "| Rule | Severity | Repo | Evidence | Message | Status |", "|---|---|---|---|---|---|"]
    for finding in report["findings"]:
        lines.append(
            f"| {finding['rule']} | {finding['severity']} | {finding['repo']} | "
            f"`{finding['evidence']}` | {finding['message']} | {finding['status']} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--mode", choices=("report", "gate"), default="report")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args(argv)

    report = check(args.root.resolve(), args.mode)
    out = args.out or (args.root / ".boundary-report")
    out.mkdir(parents=True, exist_ok=True)
    (out / "boundary-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    write_markdown(report, out / "boundary-report.md")
    print(f"boundary report: {out / 'boundary-report.md'}")
    print(f"findings: {report['summary']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
