# Ecosystem architecture

> Status: **v1.0** as of 2026-11-28. English canonical.  
> This document describes the approved architecture; it does not change it. The
> binding specifications are [`repo-boundaries.md`](repo-boundaries.md) v1.0,
> [`repo-taxonomy.md`](repo-taxonomy.md) and the ADRs listed in §8. Where this
> summary and a binding source disagree, the binding source wins.

## 1. Purpose

The ecosystem exists to add robot capabilities **without creating a second path
to the actuators** or weakening the evidence chain. Three invariants follow:

1. One declarative source of truth per concept.
2. One execution point per action.
3. One contract location per cross-repository format.

This document explains how the repositories are arranged around those
invariants. It is a map, not a specification.

## 2. Layers

| Layer | Repositories | Owns | Must not |
|---|---|---|---|
| **L0 Governance** | `.github` | Policy, templates, reusable CI, ecosystem records, organization profile | Contain product code, robot configuration or secrets |
| **L1 Contracts** | `jcheng-interfaces` | ROS IDL, HTTP/WS schemas, contract hashes, error codes | Contain nodes, device access or business logic |
| **L2 System** | `jcheng-system` | Safety state machine, lease, arbitration, execution, hardware bridge, gateway, deployment profile, safety overlay | Depend on L3/L4 at runtime; read safety configuration online from declaration repositories |
| **L3 Capabilities** | `jcheng-manipulation` (frozen), `jcheng-perception`, `jcheng-teleop`, `jcheng-learning`, `jcheng-devices`, `jcheng-mobile` (dormant) | Perception, intent, learning, device declarations, the frozen baseline | Publish vendor topics, open devices outside their declared boundary, or command motion directly |
| **L4 Applications** | `jcheng-studio`, `jcheng-applications` | Operator console, task orchestration and fail-closed intent | Join DDS, hold a lease, call `/motion/dispatch` or execute motion |
| **SIM** | `jcheng-simulation` | Virtual plant, world, mock, domain 43, truth labels | Join domains 0/41/42 or send motion to the real system |
| **SCEN** | `jcheng-scenarios` | Scenario, task, constraint and evaluation declarations | Execute tasks, start nodes, open devices or publish intent |
| **BENCH** | `jcheng-benchmark` | Suite execution, aggregation, threshold evaluation and provenance reports | Generate data, invent business thresholds or treat mock as hardware |
| **OPS** | `jcheng-ops` | Deployment probes, watchdog, systemd self-healing and runbooks | Join DDS, send motion, access devices or read business data |
| **RESEARCH** | `jcheng-research` | Literature, root cause, experiment design, reports and decisions | Be imported by runtime code or make product acceptance claims |

## 3. Repository responsibilities

| Repository | Layer | Owns | Does not own | Allowed dependencies |
|---|---|---|---|---|
| `.github` | L0 | Governance, templates, reusable CI, ecosystem status and profile | Product code, device or scenario data, secrets | None (CI may read all repositories) |
| `jcheng-interfaces` | L1 | Cross-repository IDL, HTTP/WS schemas, public schemas, contract hash | Nodes, business logic, device or scenario instances | None |
| `jcheng-system` | L2 | Safety, lease, arbitration, execution, hardware bridge, gateway, deployment instance, safety overlay | Task semantics, device catalogue, scenario catalogue, ecosystem benchmark | L1 |
| `jcheng-manipulation` | L3 frozen | `v1.0.0` experimental baseline, historical evidence, reference implementation | New features, new contracts, runtime dependency | None (it is referenced, not depended on) |
| `jcheng-mobile` | L3 | Laser odometry, SLAM, map, Nav2, chassis intent | Device drivers, motor bridge, fabricated odometry, task semantics | L1 + L2 client |
| `jcheng-perception` | L3 | Capture, detection, depth/TF, fusion, scene observation, advisory poses | Motion, task-stage decisions, training | L1 + L2 client; current contract waiver recorded |
| `jcheng-learning` | L3 | Dataset contract, validation, training, offline evaluation, policy artifacts | Runtime nodes, devices, direct motion, ecosystem benchmark | L1 |
| `jcheng-teleop` | L3 | Operator input conditioning, `TeleopCommand` intent, capture/replay, supervisory authorization | Input device drivers, lease issuance, motion execution, dataset contract | L1 + L2 client |
| `jcheng-devices` | L3 DEV | Device identity, kinematics, declared limits, capabilities, provenance, offline validation | Runtime I/O, deployment configuration, safety overlay, motion | None (offline) |
| `jcheng-scenarios` | SCEN | Scenario registry, environment/semantics/task/constraint/evaluation declarations, validation | Execution, orchestration, measurement, simulation, device catalogue | None (offline) |
| `jcheng-studio` | L4 | Observation, diagnostics, session/trajectory/experiment records, intent forwarding, stop proxy | DDS, device access, lease holding, motion dispatch, device/perception/statistics algorithms | L2 HTTP/WS + L1 |
| `jcheng-applications` | L4 | Recipe validation, deterministic planning, fail-closed intent sequencing, run records | Task success semantics, measurement, device description, motion execution | L1 + L2 HTTP/WS |
| `jcheng-simulation` | SIM | Virtual plant, world, mock, domain 43, truth labels | Task success, device catalogue, real motion | L1 (read-only) |
| `jcheng-benchmark` | BENCH | Suite execution, aggregation, threshold evaluation, provenance report | Task semantics, business threshold source, data generation, live capture | Read-only datasets and specification files |
| `jcheng-ops` | OPS | Deployment, liveness, watchdog, systemd self-healing, operations records | Business logic, scenario decisions, motion, lease, devices | HTTP health endpoints + systemd |
| `jcheng-research` | RESEARCH | Literature, root cause, experiment design, reports and decisions | Runtime code, hardware, motion, a second plant | None (offline) |

`jcheng-mobile-bench` is a non-git bench sandbox. It is not a released
repository and is not in the runtime or release matrix.

**Contract state (2026-11-28).** `jcheng-interfaces` v0.3.0 is released with
robot-profile v2, `chain_id` and gripper units. The signed v0.2.0 pin
(`afca22…`) still serves the current runtime consumers, which declare
`>=0.2,<0.3`; v0.3.0 migration is in progress. A v0.3.0 consumer is not
evidence of P1 completion until the gates and the mock v2 run are recorded.

## 4. Dependency rules

```text
L4  Applications        ── HTTP/WS intent ──▶ L2 API
L3  Capabilities        ── L2 client ───────▶ L2 API
                        ── contracts ───────▶ L1
L2  System              ── contracts ───────▶ L1
L1  Contracts           ── (no runtime dependency)
L0  Governance          ── CI only ─────────▶ all repositories
```

- **L4 → L2 API.** Applications and Studio use the gateway HTTP/WS boundary.
  They do not join DDS, hold a lease or execute motion.
- **L3 → L1 + L2 client.** Capabilities consume contracts and the system client.
  They propose intent or observation; they do not publish to hardware.
- **L2 → L1.** The system consumes contracts. It does not depend on L3 or L4.
- **L0 → all (CI only).** Governance workflows may read every repository; they
  never trigger motion.
- **Declaration repositories are outside the runtime graph.** `jcheng-devices`
  and `jcheng-scenarios` are pinned by version and hash; they are never called
  at runtime. A declaration never overrides the deployed safety envelope.
- **Mismatch is a release blocker.** A declaration/contract mismatch fails the
  build or release; it is not a preference to be negotiated at runtime.

## 5. The single motion path

Every real-robot motion passes the same boundary:

```text
intent sources
  applications (recipe → plan)
  teleop (operator intent, when authorized)
  studio (stop proxy only)
        │ HTTP/WS or a declared domain-42 topic
        ▼
jcheng-system
  → gateway accepts the request
  → lease: one holder, scope, priority, TTL, deadman, revocation
  → ExecuteMotion: contract check, idempotency, scope and priority
  → safety supervisor: state freshness, joint limits, trajectory rates,
    start state, workspace and table clearance; veto and latch on violation
  → arbiter: one executor; no second controller path
  → motion executor: trajectory, in-flight stop
  → hardware bridge: the only publisher
  → bus-verified result + evidence record
        ▲
        │ measured state (bus / CAN read-back)
```

Design consequences:

- **A lease, not a UI session, grants control.** Leases carry scope, priority,
  TTL, deadman and revocation semantics; they can be audited and preempted.
- **The safety supervisor vetoes; it does not execute.** It validates and
  latches a stop on violation.
- **The hardware bridge is the only publisher.** Capability modules join an
  unprivileged DDS domain; the vendor domain is reachable only through the
  bridge.
- **MoveIt plans; the arbiter executes.** The controller execution chain is not
  exposed as a second motion entry.
- **Measured state is not command echo.** `GetBusServoState` / CAN read-back is
  the completion authority; cached `/joint_states` is labelled `commanded`.
- **Failure is fail-closed.** A missing safety heartbeat, stale measured state,
  bus-read failure or unknown outcome latches a stop; it is not retried
  automatically.
- **A software stop is not an emergency stop.** It is a hold/zero command; the
  platform has no hardware e-stop, brake, independent encoder, torque sensing or
  self-collision model.

The current platform state matters here: ArmPi Ultra is **Frozen** and its
motion-authority revocation is pending operator action. PiPER X is in **P2
read-only**; no PiPER motion authority exists today. See
[`platform-transition.md`](platform-transition.md).

## 6. Planes outside the runtime

| Repository | Why it is outside | What it may read/write |
|---|---|---|
| `jcheng-simulation` | Uses ROS domain 43 only; no path to the real system | Robot descriptions, scenarios, contracts (read-only) |
| `jcheng-scenarios` | Declarative catalogue; no nodes or DDS | Device capability vocabulary (versioned) |
| `jcheng-devices` | Declarative registry; no device I/O | None at runtime |
| `jcheng-benchmark` | Read-only harness; no live capture in the harness | Recorded JSONL, suite and evaluation declarations |
| `jcheng-research` | Reports and decisions; no runtime code | Public sources and repository evidence |
| `jcheng-ops` | HTTP health and systemd only; no motion | Health endpoints and systemd state |

`jcheng-mobile` is L3 but **dormant**: the static bring-up is retained, and P7
mobile manipulation is deferred. It is not a current runtime consumer.

## 7. Non-repository checkouts

| Path | Identity | Rule |
|---|---|---|
| `jcheng-design` | Second checkout of `jcheng-manipulation`; carries `design/ecosystem-v1` | Design record only; never a runtime source |
| `jcheng-system-r5` | Duplicate checkout of `jcheng-system` | Not a deployment source |
| `jcheng-system-v020` | Duplicate checkout of `jcheng-system` | Not a deployment source |
| `jcheng-ecosystem-bootstrap` | M1 staging and non-repository scripts | Not published; evidence is labelled local staging |

These paths must not appear in the organization repository index or be cited as
public repositories.

## 8. ADR index

| ADR | Decision |
|---|---|
| `0001-contract-first-interfaces-repo.md` | Put cross-repository formats in a dedicated contracts repository |
| `0002-single-motion-entry-and-lease.md` | One motion entry (`ExecuteMotion`) and a lease as the control authority |
| `0003-privileged-capability-planes.md` | Separate privileged execution from capability and application planes |
| `0004-fresh-history-frozen-baseline.md` | Keep the experimental baseline immutable with a fresh-history release |
| `0005-lockfile-over-submodules.md` | Pin commits and contract hashes in a lockfile rather than submodules |
| `0006-moveit-plan-only.md` | MoveIt plans; it does not become a second execution path |
| `0007-fixed-cell-piper-first.md` | Fixed cell first; PiPER X production arm; leader read-only; AR5 gated |

The ADRs are maintained in the `jcheng-manipulation` design record
(`docs/ecosystem/adr/`). They are summarized here; the ADR text is authoritative.

## 9. Boundary and source-of-truth documents

- [`repo-boundaries.md`](repo-boundaries.md) — repository ownership, source of
  truth, runtime authority, schema ownership and evaluation ownership matrices;
  ten decisions D-01…D-10 and known deviations.
- [`repo-taxonomy.md`](repo-taxonomy.md) — layer table, dependency direction,
  document requirements and admission checks.
- [`documentation-standard.md`](documentation-standard.md) — required document
  set and status vocabulary.
- `jcheng-system/docs/SAFETY.md` — safety envelope, limits and stop semantics.
- `jcheng-system/docs/OPERATIONS.md` — deployment, lock verification and runbooks.

## 10. Maintenance

Update this document when a repository is admitted, retired or changes layer;
when a contract becomes the source of truth for a new format; or when the
single motion path changes. Do not use it to record aspirational architecture:
the target state belongs in the roadmap and the design record.
