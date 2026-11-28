# Runtime Authority Implementation Report

> Status: **offline implementation complete; independent QA pending**.
> No real robot, no DDS, no device access, no production deployment change.
> Software stop is not an emergency stop; no functional-safety claim.

## 1. Scope and constraints

Implemented under Decision B, with the 10 design constraints:

1. `HardwareAuthority` is the logical single hardware exit; devices do not have
   to share a process/thread/action.
2. Watchdogs are independent of the upper execution loop.
3. Lease expiry/revoke/client exit/identity mismatch/duplicate commands/link
   recovery/System restart have explicit safe transitions.
4. 200 ms is a provisional configurable value, not a validated safety bound.
5. Domain/remap/publisher allowlist do not replace authorization.
6. The DDS entry is disabled until permission control is reliable.
7. Software stop, watchdog, revoke and a physical e-stop are distinct.
8. The deployed version is not switched to the development version.
9. Unknown state/missing config/invalid lease/version mismatch/auth failure
   default to reject.
10. Stop remains reachable and prioritized; an expired motion lease does not
    block a stop.

## 2. Per-repository result

| Repository | Branch | HEAD | Tests | Gate |
|---|---|---|---|---|
| `jcheng-system` | `feat/authority-hardening-20261127` | `220b0ce` | **190 passed** | repository gate OK (14 packages) |
| `jcheng-mobile` | `feat/authority-hardening-20261127` | `cd491c5` | **50 passed** | pytest is the gate; colcon build OK (Jazzy) |
| `jcheng-studio` | `feat/authority-hardening-20261127` | `63266a2` | **13 root + 222 backend** | repository gate OK |

The independent QA first pass required rework; the fixes are in `220b0ce`
(deadman default, DDS privileged-service gate, missing-holder rejection, base
tick safety latch), `63266a2` (empty legacy lease), and `cd491c5` (same-host
liveness docs). See the independent QA report for the re-QA verdict.

No deleted files, no `deploy/` changes, no other-repository implementation
changes, no added absolute paths or secrets in the diffs.

## 3. System implementation

### 3.1 Single logical exit

`HardwareAuthority` owns the bridge and is the only write path:

| Method | Purpose |
|---|---|
| `execute_arm` | one arm/gripper write after contract/lease/holder/scope/deadman/latch/limits |
| `submit_base` | one four-channel base duty frame after the same checks |
| `stop` | latched software stop: arm hold + base zero |
| `hold_arm` / `zero_base` | stop outputs for error paths |
| `validate_arm` | checks without a write |
| `status` | bridge/latch/last-duty/stop status |

The vendor executor is refactored to call `HardwareAuthority`; it no longer
calls `send_step`/`send_gripper`/`hold` directly.

### 3.2 Lease, holder, deadman, stop

- `renew`/`release` require the matching holder (403 otherwise).
- `note_heartbeat` rejects unknown/expired/revoked/wrong-holder leases; a
  deadman lease defaults to 300 ms (provisional).
- `check()` uses `touch=True` for accepted motion and `touch=False` for
  status/tick, so a silent stream still expires.
- `revoke()` runs a stop hook (latch + hold + zero); a failing hook does not
  undo the revocation.
- `/v1/motion/stop` is exempt from the motion rate limit and does not require a
  lease; it still requires the gateway token.
- Missing holder on DELETE/renew is now 403: a documented breaking API change.

### 3.3 DDS gate

`vendor_gate` defaults to deny. The vendor ActionServer starts only with
`JCHENG_ALLOW_DDS_EXECUTE=1`, domain 41, the SROS2 marker and an allowed topic.
This is environment-based, not certificate verification; the mock
`jcheng_runtime` ActionServer is not gated.

## 4. Motion Authority State Machine

| State | Output | Enter | Exit |
|---|---|---|---|
| `DISABLED` | zero | default / config off | enable/restart |
| `IDLE` | zero | enabled, restart, link recovery | valid intent → `ARMED`/`MOVING`; stop → `STOP_LATCHED` |
| `ARMED` | zero | valid intent/lease, not driving | fresh non-zero → `MOVING`; lease/deadman loss → `STOP_LATCHED` |
| `MOVING` | duty frame | fresh non-zero intent | timeout → `ARMED` + zero; lease/deadman loss → `STOP_LATCHED` |
| `STOP_LATCHED` | zero | stop, lease/deadman/policy failure | authorized reset → `IDLE` |
| `FAULT` | zero | unknown state/contract/output failure | authorized reset → `IDLE` |

Key events: no/wrong/expired/revoked lease → `STOP_LATCHED`; wrong holder/scope
→ `STOP_LATCHED`; deadman loss → `STOP_LATCHED`; stream timeout → zero +
`ARMED`; network loss → zero + `IDLE`, higher seq required; duplicate/stale seq
→ rejected; concurrent submits serialized; arm stop shares the safety latch;
restart → zero + `IDLE`, no replay; unknown restored state → `FAULT`;
incompatible contract → `FAULT`; malformed/legacy envelope → rejected.

`intent_timeout_ms=200` and the mecanum mixer are provisional and unverified.

## 5. Mobile implementation

- `ROS_DOMAIN_ID=42` set for every child; `domain:=` guard aborts on any other
  value before nodes start.
- Nav2 include is wrapped in `GroupAction` + `SetRemap`:
  `controller_server:cmd_vel → cmd_vel_nav`,
  `velocity_smoother:cmd_vel → cmd_vel_nav`,
  `velocity_smoother:cmd_vel_smoothed → /jcheng/nav2/cmd_vel`,
  `/cmd_vel → /jcheng/nav2/cmd_vel`.
  The smoother chain stays closed; Nav2 never publishes `/cmd_vel`.
- A new thin intent node subscribes `/jcheng/nav2/cmd_vel` and publishes
  `/jcheng/intent/base`; default lease/holder empty → no publish; wrong domain
  → no publish; QoS best-effort, depth 1.
- The ROS-free intent mapper rejects non-finite values, speed/duty over-limit,
  stale/future stamps, non-increasing seq and rate overrun; it never clamps a
  speed limit.
- The manifest publishes only `/jcheng/intent/base`; `class: motion_source` is
  retained as a documented over-claim until `intent_source` is released.

## 6. Studio implementation

- Three legacy write endpoints return **410** by default; both
  `ARMPI_MODE=legacy` and `ARMPI_ENABLE_LEGACY_MOTION=1` are required.
- `/motion/dispatch` exists only in `backend/app/legacy_motion.py`; the default
  backend path never imports it.
- The local `LeaseManager` is downgraded to a UI concurrency lock
  (`motion_authorization: false`); motion no longer checks it.
- Intent writes require `ARMPI_MODE=hardware` + `ARMPI_SYSTEM_INTENT=1`;
  mock mode rejects and clears a configured real v1 gateway.
- Stop goes only through system `/v1/motion/stop`; the legacy stop is 410.
- Capability remains `observer` / `hardware_access: none` / empty runtime;
  mock surfaces are `read_only`, not "available".

## 7. Fault-injection matrix (16/16 covered)

| # | Case | Test evidence | Result |
|---|---|---|---|
| 1 | no lease | `test_hardware_authority.py::test_no_lease_is_rejected_before_any_write`; `test_base_intake.py::test_no_lease_latches_and_zeroes` | PASS |
| 2 | wrong holder/scope | `test_lease_holder.py::test_scope_mismatch_is_rejected`; `test_base_intake.py::test_wrong_holder_latches_and_zeroes` | PASS |
| 3 | lease expired/revoked | `test_hardware_authority.py::test_expired_lease_is_rejected_before_any_write`; `test_base_intake.py::test_revoked_lease_latches_and_zeroes` | PASS |
| 4 | deadman failure | `test_lease_holder.py::test_deadman_missing_and_revived_by_heartbeat`; `test_base_intake.py::test_deadman_failure_latches_and_zeroes` | PASS |
| 5 | intent stream loss | `test_base_authority.py::test_intent_stream_loss_zeroes_and_resumes_on_a_new_intent` | PASS |
| 6 | network disconnect/recovery | `test_base_authority.py::test_network_disconnect_recovery_and_stale_replay` | PASS |
| 7 | upper thread blocked | `test_watchdog.py::test_watchdog_runs_while_the_upper_loop_is_blocked` | PASS |
| 8 | gateway exit | `test_watchdog.py::test_gateway_exit_is_a_heartbeat_loss` | PASS |
| 9 | system restart | `test_base_authority.py::test_restart_zeroes_and_does_not_replay_the_previous_intent` | PASS |
| 10 | duplicate/old command | `test_base_authority.py::test_duplicate_and_stale_sequences_do_not_write`; `test_base_intake.py::test_duplicate_and_old_seq_do_not_write` | PASS |
| 11 | concurrent motion | `test_base_authority.py::test_concurrent_submits_are_serialized` | PASS |
| 12 | arm/base stop interlock | `test_hardware_authority.py::test_stop_holds_arm_and_zeroes_base_without_a_lease`; `test_base_intake.py::test_stop_priority_blocks_later_valid_envelopes` | PASS |
| 13 | legacy entry | `backend/tests/test_legacy_motion_disabled.py` (12 tests, 410/default/no dispatch/stop to system) | PASS |
| 14 | unauthorized DDS | `test_dds_gate.py` (default deny, domain/SROS2/topic, vendor node check) | PASS |
| 15 | wrong domain/topic | `test_dds_gate.py::test_wrong_domains_are_denied`; `test_base_intake.py::test_wrong_domain_disables_the_intake`; `test_launch.py::test_domain_is_fixed_to_42_and_asserted` | PASS |
| 16 | incompatible contract | `test_hardware_authority.py::test_incompatible_contract_is_rejected_before_any_write`; `test_base_intake.py::test_unknown_schema_is_rejected` | PASS |

## 8. Cross-repository contract

- Proposal: `jcheng-interfaces` PR #19 (`docs/proposals/base-intent-and-lease-holder.md`).
  No IDL/schema/contract hash change.
- Offline implementation uses a provisional mobile JSON envelope
  `jcheng.mobile.base_intent.v1` and a repo-local system parser. It is test-only
  until the proposal is accepted.
- The field shape matches exactly: `schema`, `lease_id`, `holder`, `command_id`,
  `seq`, `stamp_ns`, `frame`, `linear{x,y}`, `angular{z}`, `duty_limit`.

## 9. Known limits

- No base hardware output exists in `VendorBridge`; `UnavailableBaseBridge`
  refuses writes. Base actuation is fail-closed and not wired for production.
- Cross-process lease sharing is not implemented. The base node defaults to
  `lease_source=none` and rejects every envelope; an in-process shared
  `GatewayLeaseView` is the only accepted path.
- DDS gate is environment-based, not SROS2 certificate verification.
- Studio legacy code remains, default-disabled; frontend still calls the 410
  endpoints.
- Mobile `class: motion_source` is an over-claim until `intent_source` is
  released.
- 200 ms timeout, 300 ms deadman and the mecanum mixer are provisional.
- No Humble/Gazebo/real-robot validation in this phase.

## Related

- [Hardening design](10-authority-hardening-design.md)
- [Runtime authority audit](02-runtime-authority-audit.md)
- [Independent QA](18-independent-qa-report.md) (pending)
- [Deployment readiness](13-deployment-readiness-preliminary.md)
