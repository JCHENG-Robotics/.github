# Safety Parameter Validation Plan — 200 ms / 300 ms

> Status: **provisional experimental parameters**, approved for the next offline
> phase only. They are **not** validated real-robot safety parameters and must
> not be used to derive a stopping time or braking distance.
> No hardware was run in this round.

## 1. Parameters and applicability

| Parameter | Value | Where implemented | Applies to | Status |
|---|---|---|---|---|
| Command freshness | **200 ms** | `BaseConfig.intent_timeout_ms`; `parse_base_intent` freshness gate | Mobile base intent (`/jcheng/intent/base`) | provisional |
| Lease deadman | **300 ms** | `LeaseManager` `DEFAULT_DEADMAN_MS`; lease heartbeat | Arm and base leases; HTTP/DDS/gateway | provisional |
| Base control tick | 50 ms (20 Hz) | `jcheng_base` node timer | Base intake/zero output | implementation fact |
| Intent producer | 20 Hz | Mobile intent node | Base intent | implementation fact |
| Deadman bounds | 50–60000 ms | `LeaseManager` | Lease issuance | implementation bound |

Source: design decision recorded in
[10-authority-hardening-design.md](10-authority-hardening-design.md) and the
implementation report; values are deliberately conservative for a 20 Hz loop,
but have **no hardware measurement**.

## 2. Control cycle and timing assumptions

- Base intake tick: 50 ms; 200 ms freshness = 4 ticks; 300 ms deadman = 6 ticks.
- Intent producer: 20 Hz (50 ms); the system expects a fresh envelope each tick.
- Assumed but **unmeasured**: DDS scheduling jitter, Python GC pauses, CPU
  contention, Wi-Fi/USB latency, motor-controller input latency.
- The values assume mobile and system run on the **same host** with the same
  monotonic clock domain. They do not hold across hosts.
- The freshness check rejects an envelope older than 200 ms (and more than
  50 ms in the future). The deadman rejects a lease without a heartbeat for
  300 ms.

## 3. Clock and timestamp semantics

- Mobile sets `stamp_ns = time.monotonic_ns()` at receipt.
- System compares it with `time.monotonic_ns()` at receive time.
- No wall-clock, no cross-host comparison, no NTP/PTP assumption.
- A future timestamp beyond 50 ms is rejected (clock jump / bad producer).
- The lease deadman uses the system's monotonic heartbeat time, independent of
  the intent `stamp_ns`.

## 4. Communication-loss behavior

| Event | Behaviour |
|---|---|
| No fresh intent for 200 ms | Zero base duty; state `ARMED`; next valid fresh intent may resume |
| No lease heartbeat for 300 ms | Zero + `STOP_LATCHED`; reset required |
| DDS/link loss | Same as no fresh intent; a higher `seq` is required after recovery |
| Stop request | Accepted without a lease; zero + latch; never blocked by an expired motion lease |
| Process exit / watchdog trip | Independent watchdog zeroes the base; latch; no automatic restart |

## 5. Priority order

1. **Stop** (operator/system stop, revoke, latch) — always accepted.
2. **Lease invalid/expired/revoked or holder/scope mismatch** — reject + latch.
3. **Deadman expired** — reject + latch.
4. **Freshness/timestamp invalid** — reject; zero.
5. **Sequence/contract/shape invalid** — reject; no write.
6. **Valid intent** — clamp duty and submit.

A lower-priority condition never overrides a stop. A stop is never rejected
because a motion lease expired.

## 6. Stop behaviour

- Base: zero normalized duty frame; `STOP_LATCHED`; only an authorized reset
  clears it.
- Arm: hold position + shared stop latch; the bus read remains the completion
  authority.
- The stop is a **software stop**, not an emergency stop, brake or
  functional-safety function. There is no hardware e-stop, encoder or
  self-collision model on this platform.

## 7. Fail-closed conditions

Any of: missing/unknown lease, holder mismatch, scope mismatch, stale/future
timestamp, non-increasing/duplicate sequence, unknown state, contract/schema
mismatch, missing sink, invalid configuration, wrong domain → reject without a
hardware write; zero/latch where the state machine requires it.

## 8. Offline validation already performed

- System unit/mock tests: 190 passed, including freshness, deadman, holder,
  expiry, revoke, timeout, restart, concurrency and stop priority.
- Mobile: 50 passed, including stale/future, rate, seq, lease and domain guards.
- Studio: 13 root + 222 backend, including default 410, empty lease and stop
  routing.
- No ROS/DDS runtime, no hardware.

## 9. Bench validation method (future, separately authorized)

1. Motor disconnected / wheels free; measure intent-to-zero latency with a
   logic analyzer or controller log.
2. Inject 200 ms freshness loss and 300 ms heartbeat loss; confirm zero/latch.
3. Kill the base intake and the gateway separately; confirm independent
   watchdog zero/latch.
4. Introduce clock skew and future timestamps; confirm rejection.
5. Revoke/expire a lease during motion; confirm stop and no resume without a new
   lease.
6. Measure jitter under CPU/memory load and DDS loss; record distribution.
7. Only after these pass: supervised low-speed chassis test on blocks, then
   floor test, each with per-session operator authorization.

Acceptance criteria must be defined before the bench run; a measured stopping
distance is **not** assumed from 200/300 ms.

## 10. Non-claims

- 200 ms/300 ms are not the robot's actual stopping time.
- No braking distance, no SIL/PL, no functional-safety certification.
- A passing offline suite does not authorize real-robot motion.

## Related

- [Implementation report](17-authority-hardening-implementation-report.md)
- [Independent QA](18-independent-qa-report.md)
- [Deployment readiness](13-deployment-readiness-preliminary.md)
