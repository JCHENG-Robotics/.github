# Contract Governance Record — Offline Artifact Contract v1

> Status: **Proposed, not accepted**. The capability vocabulary remains
> `local_draft`. This record is not a claim that the contract is formally
> approved.

## 1. Proposal

| Item | Value |
|---|---|
| Proposal | `jcheng-interfaces/docs/proposals/offline-artifact-contract-v1.md` |
| PR | JCHENG-Robotics/jcheng-interfaces #20 |
| Contract id | `jcheng.offline-artifact-contract.v1` |
| Proposal version | 1.0.0 |
| Artifact versions | `jcheng.device_snapshot.v1`, `jcheng.scenario_requirements.v1` |
| Status | Proposed |
| Approval | **none yet**; interface-owner review required |

No schema was moved into `jcheng-interfaces`; no IDL or runtime contract hash
changed. The artifact JSON Schemas remain repository-local to devices and
scenarios.

## 2. Ownership and consumers

| Concern | Owner | Consumers |
|---|---|---|
| Contract lifecycle / version record | interfaces | all |
| Device snapshot + native capability vocabulary | devices | applications, system, simulation, learning, studio |
| Scenario requirements + requirement vocabulary | scenarios | applications, benchmark, simulation |
| Device compatibility report | devices | applications, operations |
| Cell composition / reference report | applications | benchmark, operations |
| Runtime authority, deployment, motion authorization | system | none granted by offline artifacts |

## 3. Hash semantics (final, unique meaning)

### 3.1 Artifact self-hash

`content_hash` = `sha256:` over canonical JSON of the document **excluding the
`content_hash` field**:

- sorted object keys at every level;
- separators `,` and `:`;
- ASCII escaping;
- no NaN/Infinity.

Editing any other field without regeneration is a stale artifact and must be
rejected (`STALE_DEVICE_HASH`, `STALE_SCENARIO_HASH`, devices' `STALE_SNAPSHOT`).

### 3.2 Source hash

| Artifact | Field | Meaning |
|---|---|---|
| device snapshot | `source_hash` | canonical hash of the source device profile |
| scenario requirements | `provenance.scenario_content_hash` | canonical hash of the scenario declaration documents |

A pin compares source hash to source hash. The artifact self-hash is never used
as a source pin. The naming is retained deliberately; no destructive rename was
performed.

## 4. Units and representation

- Device profile/snapshot joint limits are degrees:
  `{name, role, limits: {min_deg, max_deg}}`.
- Runtime recipes use radians; the consumer converts explicitly.
- Capability parameters are descriptor lists
  `{name, type, required, unit?, description?}`; feedback uses
  `{name, type, unit?, description?, rate_hz?}`.
- Requirement thresholds use `{op, value, unit}` with
  `op ∈ {>=, <=, >, <, ==, !=}`.
- The consumer rejects a threshold unit that does not match the declared fact
  unit (`INCOMPATIBLE_UNIT`).
- A missing fact is `unverified`; a missing required role or interface is a
  fail-closed error. The two are never collapsed.

## 5. Capability result semantics

| Field | Meaning |
|---|---|
| `artifact_valid` | schema/identity/hash validation completed |
| `capability_match_status` | matched / matched_with_unverified / unverified / fail closed |
| `capability_satisfied` | every required declared capability matched |
| `offline_execution_allowed` | isolated mock experiment may run |
| `deployment_ready` | verified deployment conditions; false offline |
| `motion_authorized` | system runtime authorization; false offline |
| `deployable` | deprecated capability-only alias; never deployment permission |

## 6. Golden vectors

`jcheng-interfaces/tests/fixtures/offline_artifact_contract_v1.json` contains
canonical device and scenario documents plus expected self-hashes.
`tests/test_offline_artifact_contract.py` recomputes them, verifies a one-field
mutation changes the hash and checks source/artifact separation. The test passes
(22 interfaces tests total on the candidate branch).

## 7. Acceptance conditions and current gap

Acceptance requires:

1. interface-owner approval on PR #20;
2. green golden-vector CI;
3. confirmation of ownership/consumers by devices, scenarios and applications;
4. an approval record in `CONTRACT.md` or the changelog.

Only (2) exists today. Criteria 1, 3 and 4 are pending, so Baseline 1
criterion 2 is **not met**. The vocabulary must not be described as a formal
public standard until then.
