# Deployment Readiness — Updated (2026-11-28)

> Status: **NOT READY**. This is the deployment-plane assessment; it does not
> repeat the main-integration PASS. A green main and a passing mock suite do not
> authorize real-robot motion.

## 1. Three-plane status

| Plane | Status | Evidence |
|---|---|---|
| Development branches | PASS (hardening/mobile port QA) | 18/27/29/30 |
| Main integration | **PASS** | 26, 34, 35; tests 191/50/13+222/57/62/68/16 |
| Deployment / physical | **FAIL (blocked)** | R10 evidence 0.1.0/`0b8d72…`; base bridge/lease/watchdog/bench absent |

## 2. Deployment blockers

| Blocker | Detail | Closure |
|---|---|---|
| Deployed tree vs dev | deployed 0.1.0; dev 0.2.0/0.3.0 | deploy aligned + evidence |
| Base hardware bridge | `UnavailableBaseBridge` fail-closed; no motor output | reviewed bridge + bench |
| Cross-process lease sharing | base `lease_source=none`; gateway view only in-process | shared lease source |
| Watchdog deployment | core only, no systemd unit | installed/verified |
| DDS authority | env/domain/SROS2 marker, not certificate verification; ExecuteMotion lacks holder | SROS2/holder contract |
| Safety parameters | 200 ms/300 ms provisional; no measured stop latency | bench validation |
| Hardware regression | no Humble/Gazebo/bench/hardware evidence in this round | container + bench plan |
| Contract skew | six repos 0.1.0 pins; system deployment tree old | contract release + re-pin |

## 3. Not authorized

- Start the robot, send motion, restore legacy motion, enable real hardware
  output.
- Modify the production deployment.
- Create a release, tag or stable version.
- Claim functional safety, measured stopping time or braking distance.

## 4. Preconditions to revisit

1. Close TD-04, TD-08, TD-09, TD-14 in the debt register.
2. Board approval of a deployment plan and per-session operator authorization.
3. Bench validation of stop/deadman/watchdog and base zero-duty.
4. Independent deployment QA (separate from main integration QA).

## Related

- [Status model](31-status-model.md)
- [Technical debt](32-technical-debt-register.md)
- [Baseline manifest](35-baseline-manifest-updated.md)
