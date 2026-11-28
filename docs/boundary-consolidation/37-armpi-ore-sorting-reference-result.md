# ArmPi Ultra × ore_sorting Reference Integration Result

> Status: **superseded for the TD-17/18/19 outcome by [40](40-td-contract-convergence-report.md)**.
> The original negative result below remains the record of the pre-convergence
> run. On the convergence branches the real artifacts now complete with
> `matched_with_unverified`; main is unchanged until #5/#3/#19 merge. Baseline 1
> remains **INCOMPLETE** as a main-plane claim.

## 1. Component results

| Repo | Branch | HEAD | Tests | Gate |
|---|---|---|---|---|
| devices | `feat/phase2-source-of-truth-20261128` | `0e2ded1` | **118** | OK |
| scenarios | `feat/phase2-source-of-truth-20261128` | `e5c5942` | **114** | OK |
| applications | `feat/armpi-ore-sorting-reference-20261128` | `24cc1d8` | **209 + 23 integration** | OK |

Draft PRs: devices #3, scenarios #2, applications #18. Not merged.

## 2. Real artifact run

Commands:

```bash
PYTHONPATH=src python3 -m jcheng_devices snapshot hiwonder.armpi-ultra \
  --output /tmp/phase2/device-snapshot.yaml
PYTHONPATH=src python3 -m jcheng_scenarios requirements ore_sorting --root . \
  --output /tmp/phase2/scenario-requirements.json
PYTHONPATH=src:scripts python3 scripts/armpi_ore_sorting_reference.py \
  --device-snapshot /tmp/phase2/device-snapshot.yaml \
  --scenario-requirements /tmp/phase2/scenario-requirements.json \
  --out /tmp/phase2/reference \
  --benchmark-root ../jcheng-benchmark --simulation-root ../jcheng-simulation
```

Result: **fail-closed**, no reference execution. Observed mismatches, in order:

| # | Mismatch | Resolution |
|---|---|---|
| 1 | device snapshot `notes` field rejected | optional metadata tolerated |
| 2 | capability `parameters` descriptor list vs value mapping | descriptors accepted, no invented values |
| 3 | `feedback` dicts vs strings | name extracted |
| 4 | joints `{limits:{min_deg,max_deg}, role}` vs `{min_rad,max_rad}` | deg→rad normalized |
| 5 | `content_hash` is the **source profile** hash in the device snapshot, but the harness requires the **artifact self-hash** | **not weakened**; run stops at `STALE_DEVICE_HASH` |
| 6 | scenario requirements are **cell-level abstract** device capabilities (`manipulation.arm.reach_m`, payload, dof, gripper aperture, camera resolution) plus `perception.*` algorithm capabilities; the device snapshot is a **single arm** with concrete IDs (`arm.position_control`, `arm.joint_feedback`) | not resolved; needs a cell composition/vocabulary |

After fixing 1–4 and not weakening 5, the run still cannot proceed to a positive
capability match because of 5–6. No report or plan was fabricated.

## 3. What the fixture path proves

The applications integration tests use a declared fixture where the device
snapshot and scenario requirements share a vocabulary. That path proves:

- capability match and deterministic 2-step plan;
- mock gateway lease acquisition/release and stop path;
- synthetic JSONL with `data_source: synthetic`;
- benchmark CLI invoked with verified suite/dataset hashes (`inconclusive`, no
  invented threshold);
- simulation asset check optional (`not_checked` when no assets declared).

It does **not** prove that the real devices/scenarios artifacts are compatible.

## 4. Conclusion

- The component implementations are real and tested.
- The cross-repository **artifact contract is not converged**: hash semantics,
  parameter/feedback/joint representation, device-vs-algorithm requirement
  split, cell-level capability composition.
- The reference correctly refuses to run on the real artifacts; this is a
  successful rejection test, not a successful vertical integration.
- Decision 9 criteria 4, 5 and 8 remain **not met**; Baseline 1 stays
  **INCOMPLETE**.

## 5. Recommended next step

1. Define one canonical artifact schema for device snapshots and scenario
   requirements: hash semantics (`source_hash` vs `artifact_hash`), parameter
   and feedback representation, joint units/structure.
2. Decide the capability vocabulary: per-device concrete IDs plus a cell
   composition mapping, or a single cell snapshot; keep algorithm requirements
   separate and owner-assigned (perception/learning).
3. Re-run the same three commands; require a positive `matched` result or an
   explicit `UNVERIFIED` classification, with `deployable: false` until data is
   verified.
4. Do not merge the Draft PRs as Baseline-complete until this passes.

## 6. Convergence update (2026-11-28)

The three mismatches were resolved without weakening the hash check:

- `source_hash` (profile) and `content_hash` (artifact) are now distinct.
- Device snapshot `attributes` declare role and DOF; a missing fact is null.
- Scenario requirements carry `role`, `interface` and a numeric `threshold`;
  algorithm requirements carry `deferred_to`.
- The consumer composes arm + gripper + camera snapshots by role and reports
  `matched_with_unverified` for the real cell.

See [40](40-td-contract-convergence-report.md) for commands, per-requirement
outcomes, tests and the plane-by-plane readiness.

## Related

- [Phase 2 design](24-phase2-source-of-truth-design.md)
- [Phase 2 implementation status](28-phase2-implementation-status.md)
- [Technical debt](32-technical-debt-register.md)
- [Baseline manifest](35-baseline-manifest-updated.md)
