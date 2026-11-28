# Safety, limitations and governance

> Status: **v1.0** as of 2026-11-28. English canonical.  
> This document states what the platform does **not** guarantee. It does not
> replace `jcheng-system/docs/SAFETY.md`, the hardware workflow, the deployment
> runbooks or a per-session operator authorization.

## 1. Safety model

The platform has **no hardware e-stop, brake, independent encoder, torque
sensing or self-collision model**. The base is open-loop with no odometry. A
software stop is a hold/zero command, not a safety-rated stop. The ecosystem is
**not safety-certified** and claims no SIL/PL compliance.

| Protection | Present? | What it actually is |
|---|---|---|
| Hardware e-stop | **No** | No safety-rated stop channel |
| Brake | **No** | No mechanical holding brake |
| Independent encoder | **No** | Bus-servo / CAN feedback is the measurement source; `/joint_states` may be a command cache |
| Torque sensing | **No** | No force/torque feedback in the control loop |
| Self-collision model | **No** | No link/link or link/gripper collision model |
| Workspace guard | Partial | TCP-based workspace and table checks; link and gripper collision are outside the model |
| Software stop | Yes | Hold/zero command and stop latch; not safety-rated |
| Lease / deadman | Yes | Scope, TTL and revocation; not a substitute for an e-stop |

**Measured state is not command echo.** The completion authority is a bus or CAN
read-back (`GetBusServoState`, CAN feedback). A cached `/joint_states` value is
labelled `commanded`, not `measured`.

## 2. Operating rules

1. **Supervised only.** Every real-robot session requires an operator present and
   a separate, explicit authorization. Authorization does not carry over from a
   previous session.
2. **No remote motion.** Do not accept motion requests from a remote user, a CI
   job or an unattended script.
3. **Clear the workspace.** The vendor container's startup check can move the
   arm. Do not restart it as part of a routine operation.
4. **One authority.** Do not start a second vendor stack, motion gateway or
   publisher while a motion authority is active. Record the publisher set when
   switching.
5. **Fail closed.** A missing safety heartbeat, stale measured state, bus-read
   failure or unknown outcome latches a stop; do not retry automatically.
6. **Stop means stop.** A stop request latches and rejects new commands. The UI
   says "software stop" or "stop request", never "emergency stop".
7. **No fabricated state.** Do not synthesize depth, TF, odometry, joint state or
   evidence. A missing measurement is labelled missing.
8. **No unattended recovery that moves the arm.** `jcheng-ops` restarts
   processes; it does not send motion. The reboot path needs an operator because
   the vendor boot sequence moves the arm.

## 3. Platform freeze and motion authority

ArmPi Ultra was frozen on 2026-11-28. The platform is `Frozen`, not `Archived`:
the read-only demo, deployment files, image digest and rollback path are
retained.

| Surface | State |
|---|---|
| ArmPi motion authority | **Revocation pending operator action** |
| Read-only `/v1` gateway | Retained |
| Vendor container restart | **Do not** restart; startup check moves the arm |
| `jcheng-ops` ArmPi probes | `legacy`; no new installs |
| PiPER X | P2 read-only; no motion authority |
| AR5 | Planned; identity gate not passed |

The on-robot revocation is a separate, authorized action: stop the vendor motion
gateway, keep the read-only gateway, record the publisher set before and after,
and do not restart the vendor container. Physical power-down is the final state
once the read-only demo is no longer needed.

## 4. Non-claims

The following are **not claimed**:

- Functional safety, SIL/PL compliance or certification of any kind.
- A safety-rated stop, e-stop, brake or independent position verification.
- Collision-free motion for links or gripper.
- Reliable operation in an unattended cell.
- Generalisation of ArmPi results to PiPER X or AR5.
- Population-level reliability from a small number of supervised sessions.
- Production readiness of the new ecosystem. Baseline 1 is conditional and
  deployment is not ready.

## 5. Limitations

### 5.1 Evidence scope

- **One platform, one site.** Results come from one ArmPi Ultra, one table setup
  and a small number of supervised sessions.
- **Failed error-budget bound.** The 6 mm RSS bound is not met (13.325 mm). The
  3.080 mm empirical placement mean is a different statistic; it is not a pass.
- **Fast path, one direction.** The 4.0 rad/s / 20 rad/s² profile is bus-verified
  but was validated in one direction.
- **M6 not complete.** S14 and the ecosystem G8 re-run were never started. The
  platform freeze retires them, not defers them. The baseline's own G8 is a
  separate frozen result.
- **Residual unverified items.** S7 stale-state injection and S9 runtime
  publisher detection were not run on hardware.

### 5.2 Capability gaps

- **Mobile.** Only a static `/scan`, `/odom`, `/map` bring-up; motion, mount pose
  and navigation are unverified. The repository is dormant and P7 is deferred.
- **Perception.** One dual-view run; multi-pose accuracy, motion TF and
  repeatability are unverified. The wrist depth reader can still wedge (run 10).
- **Benchmark.** No suite result; one migrated read-only host/DDS snapshot
  (2026-11-17) is not a benchmark result.
- **Operations.** The watchdog has never fired in a real wedge; the reboot path
  has not been exercised because the vendor boot sequence moves the arm.
- **Learning.** M1 dataset infrastructure only; no own-robot dataset, no policy,
  no hardware learning loop.
- **Teleoperation.** M0/M1 and mock/simulation only; no hardware streaming.
- **Simulation.** Offline domain 43; Gazebo partial; no ore-sorting world asset.
- **Studio / applications.** Offline/mock verified; no hardware acceptance.

### 5.3 Deployment gaps

Baseline 1 records the blockers: no cross-process lease source, no base hardware
bridge, deployed tree 0.1.0 vs dev 0.3.0, watchdog not deployed in the target
cell, DDS authority not certificate-based, and no bench/hardware evidence for
the new ecosystem.

## 6. Known failure modes

| Failure | Effect | Handling |
|---|---|---|
| Vendor container restart | Startup check moves the arm | Do not restart without an operator; clear the workspace |
| Command cache read as state | A stale `/joint_states` value looks measured | Use bus/CAN read-back; label cache as `commanded` |
| Stale state injection | Safety may not reject stale data (S7 unverified) | Do not claim validation; keep the residual gate open |
| Second publisher | Dual authority | Publisher allowlist; stop and investigate; do not auto-retry |
| Wrist depth wedge | Dual-view window not repeatable (run 10) | Restart procedure documented; no repeatability claim |
| Base motion | Invalidates table calibration; open-loop, no odometry | Re-calibrate after any base motion; P7 only |
| OOM / half-dead host | sshd or gateway wedged; network checks look fine | Probe the application layer; `jcheng-ops` guards; power cycle needs an operator |
| Unknown motion outcome | Arm may have moved | Latch `MOTION_OUTCOME_UNKNOWN`; read the bus; do not retry blindly |

## 7. Incident and rollback pointers

- `jcheng-ops/docs/INCIDENT-2026-11-24.md` — OOM and half-dead host timeline.
- `jcheng-ops/docs/RUNBOOK.md` — probes, restart policy and escalation.
- `jcheng-system/docs/OPERATIONS.md` — deployment, lock verification and
  read-only/motion gateway operations.
- ArmPi freeze record — rollback steps: software stop and disarm, start only the
  read-only gateway, probe the application layer, read the bus, record the
  rollback. Never restart the vendor container as part of a rollback.

## 8. License status

| Repository | License | Reuse |
|---|---|---|
| `jcheng-manipulation` | **MIT** | Yes, under MIT |
| `jcheng-mobile` | **MIT**, retained pending review | Do not treat as a precedent for other repositories |
| `.github` | **No `LICENSE`** | No reuse grant until the review closes |
| `jcheng-interfaces` | **No `LICENSE`** | No reuse grant |
| `jcheng-system` | **No `LICENSE`** | No reuse grant |
| `jcheng-perception` | **No `LICENSE`** | No reuse grant |
| `jcheng-ops` | **No `LICENSE`** | No reuse grant |
| `jcheng-learning` | **No `LICENSE`** | No reuse grant |
| `jcheng-teleop` | **No `LICENSE`** | No reuse grant |
| `jcheng-devices` | **No `LICENSE`** | No reuse grant |
| `jcheng-scenarios` | **No `LICENSE`** | No reuse grant |
| `jcheng-simulation` | **No `LICENSE`** | No reuse grant |
| `jcheng-studio` | **No `LICENSE`** | No reuse grant |
| `jcheng-applications` | **No `LICENSE`** | No reuse grant |
| `jcheng-research` | **No `LICENSE`** | No reuse grant |
| `jcheng-benchmark` | **No `LICENSE`** | No reuse grant |

The third-party dependency and copyright review is pending. Vendor assets are
not redistributed. `jcheng-mobile` was initialized with MIT; the file is retained
pending review, not removed retroactively, and is not a precedent. See
[`license-review.md`](license-review.md).

## 9. Governance

- `main` is protected on every repository: pull request, independent review,
  CODEOWNERS, linear history, no force-push or deletion, and an organization
  merge queue.
- A second reviewer (`@JerichoSwaine`) holds maintain access and is a CODEOWNER
  on every repository. `main` changes require one author and one reviewer.
- Break-glass is a documented exception, not the default. The 2026-11-27 git
  authority incident is recorded in `docs/incidents/2026-11-27-git-authority.md`.
- CI and automation never trigger motion.
- Security reports follow [`SECURITY.md`](../SECURITY.md); do not disclose exploit
  details, credentials or real site IPs publicly.
- Contributions follow [`CONTRIBUTING.md`](../CONTRIBUTING.md) and the design
  change template.

## 10. Reporting a safety issue

If a safety-relevant defect is found:

1. Stop the session and latch a stop; do not attempt an automatic recovery.
2. Record the observed state, the command, the bus read-back and the time.
3. Keep the workspace clear and the operator present.
4. Report through `SECURITY.md` for security issues, or a `design` issue for a
   safety-design change. Do not open a public exploit issue.
