# Contract Ratification Record — Offline Artifact Contract v1

> Status: **approval evidence exists; ratification PR #21 is unmerged**. The
> contract is not yet reflected on `main`, so the frozen manifest cannot treat
> it as the accepted main state.

## 1. Contract identity

| Item | Value |
|---|---|
| Contract | `jcheng.offline-artifact-contract.v1` |
| Contract version | 1.0.0 |
| Artifact versions | `jcheng.device_snapshot.v1`, `jcheng.scenario_requirements.v1` |
| Owner | `jcheng-interfaces` for lifecycle; producers keep content ownership |
| Proposal | `jcheng-interfaces/docs/proposals/offline-artifact-contract-v1.md` |
| Ratification PR | jcheng-interfaces #21, head `f656d69`, base `a142641` |
| Status on main | **Proposed** (ratification not merged) |
| Status in PR #21 | **Accepted**, offline artifacts only |

## 2. Real approval evidence

| Condition | Evidence |
|---|---|
| Interfaces CODEOWNER approval | `JerichoSwaine` (CODEOWNER for `/docs/`, `/schemas/`, IDL), review `APPROVED`, 2026-11-28T06:27:30Z on PR #20 |
| Merge | interfaces PR #20, merge `a142641b4fb256aa2368abe778bb6c5b010d1c23` |
| Producer/consumer confirmation | devices #7 (`a006f5f`), applications #20 (`0be306e`), `.github` #37 (`f9e77eb`) — same owner approval and merge |
| Golden vectors | `tests/test_offline_artifact_contract.py` passes; 22 interfaces tests on candidate |
| Approval record | PR #21 records it in the proposal §8 and `CONTRACT.md` §4 |

This is a real review approval, not fabricated. It covers the offline artifact
semantics only. It does **not** accept ROS IDL, DDS, HTTP/gateway schemas,
runtime robot profiles or real motion authority.

## 3. Final contract content

- `content_hash` = canonical-JSON artifact self-hash excluding `content_hash`;
- source hash separate: devices `source_hash`, scenarios
  `provenance.scenario_content_hash`;
- degrees in device profiles/snapshots, radians in runtime recipes;
- capability descriptors and requirement thresholds `{op, value, unit}`;
- cell roles and interfaces; missing required role/interface fails closed;
  missing fact is `unverified`;
- algorithm requirements deferred to their owner;
- `capability_satisfied`/`offline_execution_allowed` do not imply
  `deployment_ready` or `motion_authorized`;
- `deployable` is a deprecated capability-only alias;
- additive v1 changes allowed; field removal/rename, hash-rule or unit change
  requires v2.

## 4. Vocabulary transition

- Before: `local_draft`.
- After ratification is merged: `contracted` for the offline artifact
  vocabulary (jcheng-scenarios PR #5).
- Still not contracted: runtime/ROS interfaces.

The vocabulary PR is CI green and review-required; it is not on main yet.

## 5. Ratification gaps

1. interfaces #21 needs a real reviewer approval and merge;
2. scenarios #5 needs a real reviewer approval and merge;
3. only after both are on main can the manifest record the contract as
   accepted/contracted. Until then Baseline 1 remains **INCOMPLETE**.
