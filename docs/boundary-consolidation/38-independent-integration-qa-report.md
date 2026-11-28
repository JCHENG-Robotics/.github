# Independent Integration QA Report

> Status: **Development/Main PASS; Deployment/Physical FAIL (blocked)**.
> QA was performed by an agent independent of the implementation agents.
> Read-only: no source edits, no Git writes, no ROS/DDS, no ssh, no hardware.

## 1. Fixed-SHA verification

The integration workspace `/tmp/eib1-workspace` was built from `git archive
origin/main` for each repository. The QA agent verified 8/8 `origin/main` SHAs
and 16/16 sampled key files against `git show origin/main:<file>`:

`.github 94b4cd5`, devices `86c721c`, scenarios `6dbedad`, learning `6997825`,
interfaces `1e6ecd0`, system `72b2ce2`, studio `40c002b`, mobile `f96cfee`.
No archive/main mismatch was found.

Frozen baseline: `jcheng-manipulation` `v1.0.0^{commit}` = `b3411e4` (annotated
tag object `6436e2b`); worktree clean; no runtime dependency on it.

## 2. Tests and gates

| Repository | Result |
|---|---|
| `.github` | M1 gate OK; allowlist 8/8; checker 20 passed |
| system | **191 passed**; gate OK; 97 focused hardening tests |
| mobile | **50 passed** |
| studio | root **13 passed**; backend **222 passed** |
| devices | **57 passed**; gate OK |
| scenarios | **62 passed**; gate OK |
| interfaces | **16 passed**; schema check OK |
| learning | **68 passed** (isolated venv); gate OK |

## 3. Boundary check on main

`check_boundaries.py --root /tmp/eib1-workspace --mode report` →
**12 open + 1 waived**, 0 open Critical:

- interfaces: B5 manifest; B7 ownership.
- system: B5 manifest; B6 deployed-tree contract 0.1.0 vs 0.2.0.
- learning: B7; B8/B10 device profile copy.
- studio: B6 lock skew; B8/B10 joint_mapping/takeover copies; B4 waived
  (`legacy_motion.py`, until 2026-12-31).

## 4. Cross-repository semantics

- Mobile `to_payload()` → system `parse_base_intent()`: 10 fields match
  dynamically; schema/frame/domain align.
- Studio forwards intent only to system `/v1/motion/execute`; stop only to
  `/v1/motion/stop`; default legacy is 410.
- Cross-process lease sharing is **not implemented**: `lease_source=none`
  rejects all; a separate manager's lease is rejected; same-process
  `GatewayLeaseView` is the only shared path.
- Arm/base stop: shared latch, hold/zero, stop not blocked by lease expiry.
- Old/invalid contract, schema, seq, domain requests are rejected.
- Mock end-to-end: 17 scenarios, **15 pass / 2 expected skips**, 0 required
  failures.
- ROS: Humble is CI evidence only; no local ROS/hardware run.

## 5. Verdict

| Plane | Verdict |
|---|---|
| Development | PASS |
| Main integration | **PASS** |
| Deployment / physical | **FAIL (blocked)** |

Deployment blockers: deployed tree 0.1.0/`0b8d72…` vs dev 0.2.0/`afca22…`,
base hardware bridge absent, cross-process lease absent, watchdog not deployed,
DDS gate not certificate-based, 200/300 ms provisional, no bench/hardware
evidence.

## 6. Residual risks / debt

- B5/B7/B8/B10 open items; studio B4 waived, not resolved.
- Contract pin skew (six repos 0.1.0).
- No Humble/Gazebo/bench/hardware regression.
- Mocks are not real hardware implementations.

## 7. Independence statement

The QA agent did not implement the changes and did not edit files. The final
Board sign-off and merge remain with the Board. A green main does not authorize
real-robot motion.

## Related

- [Status model](31-status-model.md)
- [Boundary report — main](34-boundary-report-main.md)
- [Deployment readiness](36-deployment-readiness-updated.md)
