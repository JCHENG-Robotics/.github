# Independent QA Report — Authority Hardening (final)

> Status: **PASS — eligible for push/PR review, not merge**.
> QA was performed by an agent independent of the three implementation agents.
> Final Board sign-off and merge remain with the Board.
> No file was edited, no Git operation was performed, no ROS/DDS or hardware
> was started.

## 1. Test evidence (independently run)

| Repository | HEAD | Command | Result |
|---|---|---|---|
| `jcheng-system` | `220b0ce` | `python3 -m pytest` | **190 passed** |
| `jcheng-system` | `220b0ce` | `bash scripts/check_repo_gate.sh` | OK (14 packages) |
| `jcheng-mobile` | `64dce1e` | `python3 -m pytest` | **50 passed** |
| `jcheng-studio` | `ce7199b` | `python3 -m pytest -q tests` | **13 passed** |
| `jcheng-studio` | `ce7199b` | `/tmp/studio-venv/bin/python -m pytest tests` | **222 passed** |
| `jcheng-studio` | `ce7199b` | `bash scripts/check_repo_gate.sh` | OK |

Hygiene: worktrees clean; no deleted files; no `deploy/` changes; no
cross-repository implementation changes; no new secrets/PII/absolute paths.

## 2. Verdict

| Repository | Verdict |
|---|---|
| `jcheng-system` | **PASS** |
| `jcheng-mobile` | **PASS** (static/unit; runtime/QoS unverified) |
| `jcheng-studio` | **PASS** (default-disabled legacy; B4 formally waived) |

## 3. Rework closure

| ID | Finding | Closure evidence |
|---|---|---|
| R1 | deadman opt-in | Closed: default `deadman_required=True`; 300 ms default; `deadman_ms=0` rejected unless an explicit manager opt-out; tests cover expiry and opt-out |
| R2 | DDS privileged services ungated | Closed by design: 7 privileged authority/safety services are created only when the same vendor gate allows; read-only `validate_motion`/`get_state`/`capabilities` remain open and are documented |
| R3 | arm holder omission bypass | Closed: `require_holder=True` default; missing holder distinct from wrong holder; HTTP/lease/hardware tests |
| R4 | studio B4 | Closed as waiver `W-2026-11-27-01` (rule B4, repo studio, evidence `legacy_motion.py`, expires 2026-12-31); **not eliminated** |
| R5 | empty legacy lease | Closed: `""`/whitespace → 400 `BAD_REQUEST`, never dispatched; test tightened to exact 400/code |
| R6 | mobile liveness docs | Closed: 200 ms freshness / 300 ms deadman, same-host monotonic; residual docstring fixed |
| R7 | base tick shared latch | Closed: tick checks the shared safety stop/unknown state and zeroes/latches; tests |

## 4. Remaining low-risk items

1. `jcheng-runtime` mock opts out of deadman/holder for legacy interface tests;
   commented and not the production vendor path.
2. DDS `ExecuteMotion` has no holder field, so even with the gate open it fails
   closed with `NOT_LEASE_HOLDER`; HTTP `/v1/motion/*` is the usable path until
   an interfaces proposal adds holder.
3. Base intake `lease_source=none` and no cross-process shared view: every
   envelope is rejected; functional base actuation is not available.
4. Watchdog is a core library, not a deployed systemd unit.
5. Mobile domain/remap/no-`/cmd_vel` are static/unit evidence; runtime topic/QoS
   is unverified.
6. Software stop is not an emergency stop; no functional-safety claim; base
   zero-duty and arm hold are unverified on hardware.
7. Waiver expiry/evidence matching is now enforced by the checker; the studio
   waiver expires 2026-12-31 and must be renewed or the code removed.

## 5. Cross-repository contract

- Mobile `to_payload` and system `parse_base_intent` match field-by-field:
  `schema`, `lease_id`, `holder`, `command_id`, `seq`, `stamp_ns`, `frame`,
  `linear{x,y}`, `angular{z}`, `duty_limit`.
- The envelope is provisional/repo-local; the interfaces proposal (PR #19) is
  pending; no contract hash change.

## 6. Boundary check

Post-fix report: **29 findings, 28 open (14 High / 12 Medium / 2 Low), 1 waived
Critical (studio legacy)**. Open Critical = 0. Mobile B4 `/cmd_vel` eliminated.
B4 remains only in the default-disabled studio legacy module, waived until
2026-12-31.

## 7. Push/PR conclusion

The three implementation branches are **eligible for push and PR review**, not
merge. Board approval is required for merge. No real-robot motion is authorized
by this QA; deployment readiness remains **NOT READY** (see
[13-deployment-readiness-preliminary.md](13-deployment-readiness-preliminary.md)).

## 8. QA method

Read-only diff review, independent test runs, report-only boundary check, the
16/17-case fault-injection matrix, and a re-QA after Rework. The QA agent did
not implement any of the changes and did not edit files.

## Related

- [Implementation report](17-authority-hardening-implementation-report.md)
- [Hardening design](10-authority-hardening-design.md)
- [Waiver registry](../../boundary-waivers.yaml)
- [Deployment readiness](13-deployment-readiness-preliminary.md)
