#!/usr/bin/env bash
# Baseline 1 unified offline acceptance entry.
#
# Reproduces the real-CLI vertical integration and (when available) the
# eight-case mock ore-sorting task with benchmark discrimination. Read-only
# with respect to the repositories; writes only under OUT.
#
# Usage:
#   DEVICES_ROOT=... SCENARIOS_ROOT=... APPLICATIONS_ROOT=... \
#   BENCHMARK_ROOT=... SIMULATION_ROOT=... OUT=... \
#   dev/baseline1-acceptance.sh
set -euo pipefail

WS="${JCHENG_WORKSPACE:-$HOME/jcheng}"
DEVICES_ROOT="${DEVICES_ROOT:-$WS/jcheng-devices}"
SCENARIOS_ROOT="${SCENARIOS_ROOT:-$WS/jcheng-scenarios}"
APPLICATIONS_ROOT="${APPLICATIONS_ROOT:-$WS/jcheng-applications}"
BENCHMARK_ROOT="${BENCHMARK_ROOT:-$WS/jcheng-benchmark}"
SIMULATION_ROOT="${SIMULATION_ROOT:-$WS/jcheng-simulation}"
OUT="${OUT:-$WS/dev/out/baseline1}"

mkdir -p "$OUT/artifacts" "$OUT/reference"
echo "== roots"
for pair in "devices:$DEVICES_ROOT" "scenarios:$SCENARIOS_ROOT" "applications:$APPLICATIONS_ROOT" "benchmark:$BENCHMARK_ROOT" "simulation:$SIMULATION_ROOT"; do
  name="${pair%%:*}"; path="${pair#*:}"
  sha="$(git -C "$path" rev-parse HEAD 2>/dev/null || echo no-git)"
  printf '%-13s %s %s\n' "$name" "$sha" "$path"
done

echo "== device snapshots"
(cd "$DEVICES_ROOT" && PYTHONPATH=src python3 -m jcheng_devices --root . \
  snapshot hiwonder.armpi-ultra --output "$OUT/artifacts/arm.yaml")
(cd "$DEVICES_ROOT" && PYTHONPATH=src python3 -m jcheng_devices --root . \
  snapshot hiwonder.armpi-ultra-gripper --output "$OUT/artifacts/gripper.yaml")
(cd "$DEVICES_ROOT" && PYTHONPATH=src python3 -m jcheng_devices --root . \
  snapshot intel.realsense-d435i --output "$OUT/artifacts/camera.yaml")

echo "== scenario requirements"
(cd "$SCENARIOS_ROOT" && PYTHONPATH=src python3 -m jcheng_scenarios \
  requirements ore_sorting --root . --output "$OUT/artifacts/requirements.json")

echo "== reference integration"
(cd "$APPLICATIONS_ROOT" && PYTHONPATH=src:scripts python3 \
  scripts/armpi_ore_sorting_reference.py \
  --device-snapshot "arm=$OUT/artifacts/arm.yaml" \
  --device-snapshot "gripper=$OUT/artifacts/gripper.yaml" \
  --device-snapshot "camera=$OUT/artifacts/camera.yaml" \
  --scenario-requirements "$OUT/artifacts/requirements.json" \
  --out "$OUT/reference" \
  --benchmark-root "$BENCHMARK_ROOT" \
  --simulation-root "$SIMULATION_ROOT")

if [[ -f "$APPLICATIONS_ROOT/scripts/ore_sorting_mock_task.py" ]]; then
  echo "== mock ore-sorting task"
  APP_SHA="$(git -C "$APPLICATIONS_ROOT" rev-parse HEAD 2>/dev/null || echo unknown)"
  DEV_SHA="$(git -C "$DEVICES_ROOT" rev-parse HEAD 2>/dev/null || echo unknown)"
  SCEN_SHA="$(git -C "$SCENARIOS_ROOT" rev-parse HEAD 2>/dev/null || echo unknown)"
  BENCH_SHA="$(git -C "$BENCHMARK_ROOT" rev-parse HEAD 2>/dev/null || echo unknown)"
  (cd "$APPLICATIONS_ROOT" && PYTHONPATH=src:scripts python3 \
    scripts/ore_sorting_mock_task.py \
    --device-snapshot "arm=$OUT/artifacts/arm.yaml" \
    --device-snapshot "gripper=$OUT/artifacts/gripper.yaml" \
    --device-snapshot "camera=$OUT/artifacts/camera.yaml" \
    --scenario-requirements "$OUT/artifacts/requirements.json" \
    --out "$OUT/mock-task" \
    --case all \
    --benchmark-root "$BENCHMARK_ROOT" \
    --repository-sha "applications=$APP_SHA" \
    --repository-sha "devices=$DEV_SHA" \
    --repository-sha "scenarios=$SCEN_SHA" \
    --repository-sha "benchmark=$BENCH_SHA")
else
  echo "== mock ore-sorting task: not present in this application tree"
fi

echo "== gate check"
python3 - "$OUT" <<'PY'
import json, sys
from pathlib import Path
out = Path(sys.argv[1])
reference = json.loads((out / "reference/reference_report.json").read_text())
match = reference["capability_match"]
print("reference status:", match["status"])
print("reference deployable:", match.get("deployable"))
print("reference benchmark:", reference["benchmark"].get("status"))
print("simulation:", reference["simulation_check"].get("status"))
task_summary = out / "mock-task/task_summary.json"
if task_summary.is_file():
    summary = json.loads(task_summary.read_text())
    print("mock cases:", {k: v["status"] for k, v in summary["cases"].items()})
    print("mock mismatches:", summary["mismatches"])
    print("benchmark:", {k: v.get("status") for k, v in summary.get("benchmark", {}).items()})
    assert summary["offline_execution_allowed"] is True
    assert summary["deployment_ready"] is False
    assert summary["motion_authorized"] is False
    assert summary["mismatches"] == []
PY

echo "evidence: $OUT"
