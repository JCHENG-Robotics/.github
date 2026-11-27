# File Changes, Tests and Rollback

> Status: **final for this round (2026-11-27)**. Authorized changes only:
> governance docs/scripts, admission docs, one interfaces proposal, one Learning
> regression report, and the offline authority hardening in system/mobile/studio.
> No `deploy/` change, no tag, no history rewrite, no real-robot run.

## 1. Change inventory

| Repository | Branch / HEAD | Diff (vs base) | Tests | Rollback |
|---|---|---|---|---|
| `.github` | `docs/boundary-consolidation-20261127` `f523540` | 10 files, docs | gate OK | close PR #27 |
| `.github` | `feat/controlled-git-20261127` `ce33df3` | docs + 4 scripts + reports | gate OK; allowlist 8; checker 20 | close PR #28 |
| `jcheng-devices` | `feat/admission-20261127` `9026c16` | 5 files (16 vs main) | 57 passed | close PR #2 |
| `jcheng-scenarios` | `feat/admission-20261127` `6ee7928` | 9 files | 62 passed | close PR #1 |
| `jcheng-interfaces` | `docs/base-intent-proposal-20261127` `3e17add` | 1 proposal | 16 passed; schema check | close PR #19 |
| `jcheng-learning` | `feat/regression-20261127` `2d4ea30` | 3 files (docs/evidence) | 68 passed | close PR #5 |
| `jcheng-system` | `feat/authority-hardening-20261127` `220b0ce` | 40 files, +5223/−122 | 190 passed; gate OK | close PR #41; Board may revert to `879b4b9` with a new commit |
| `jcheng-mobile` | `feat/authority-hardening-20261127` `64dce1e` | 19 files, +1229/−88 | 50 passed | close PR #6; resolve conflict per Board |
| `jcheng-studio` | `feat/authority-hardening-20261127` `ce7199b` | 29 files, +1251/−98 | 13 root + 222 backend; gate OK | close PR #10; Board may revert to `b5c99e8` with a new commit |

No files deleted in any implementation diff. No `deploy/` files changed. No
other repository's implementation changed.

## 2. Tests and evidence

| Layer | Evidence |
|---|---|
| L0 static/gates | `.github` M1 gate; system/mobile/studio/learning/ops/research gates; allowlist 8/8; checker 20 |
| L1 unit | system 190, mobile 50, studio 13+222, learning 68, devices 57, scenarios 62, interfaces 16 |
| L2 mock | system base/gateway mock tests, studio legacy 410/stop tests, mobile intent tests |
| L3 mock e2e | system S1–S17 mock suites (existing) |
| L4 replay | not run in this round |
| L5 hardware | **not run; not authorized** |

Static boundary check: 29 findings, 28 open + 1 waived Critical (studio
legacy), 0 open Critical. Mobile B4 eliminated.

## 3. Rollback principles

1. Prefer closing the PR and leaving the branch as audit evidence.
2. If code must be rolled back, the Board approves a **new reverting commit**;
   no force-push, reset, rebase or tag move.
3. Do not delete remote branches or tags without separate approval.
4. The pre-change SHAs are: devices `029991f`, scenarios `4390212`,
   interfaces `origin/main`, learning `25eb184`, system `879b4b9`,
   mobile `89a769f`, studio `b5c99e8`.

## 4. Suggested merge order (Board decision)

1. `.github` #27 (boundary baseline), then #28 (CGO/allowlist/checker).
2. `jcheng-interfaces` #19 (proposal only; no contract change).
3. `jcheng-learning` #5 (docs/evidence).
4. `jcheng-system` #41, `jcheng-studio` #10 (QA PASS, CI green).
5. `jcheng-mobile` #6 only after the `main` conflict is resolved per Board.
6. devices #2 and scenarios #1 are independent; merge when reviewed.

## 5. Known limits

- Base hardware bridge unavailable; base actuation fail-closed.
- Cross-process lease sharing not implemented; `lease_source=none` rejects all.
- DDS gate is env/domain/SROS2-marker, not certificate verification; DDS
  `ExecuteMotion` fails closed without a holder field.
- Mobile domain/remap/QoS not hardware-verified; PR #6 has a remote conflict.
- Studio legacy code remains default-disabled; waiver `W-2026-11-27-01`
  expires 2026-12-31.
- 200 ms freshness / 300 ms deadman and the mecanum mixer are provisional.
- Deployment readiness remains **NOT READY**; no real-robot motion authorized.

## Related

- [Git operation log](14-git-operation-log.md)
- [Remote delivery report](19-remote-delivery-report.md)
- [Independent QA](18-independent-qa-report.md)
- [Deployment readiness](13-deployment-readiness-preliminary.md)
