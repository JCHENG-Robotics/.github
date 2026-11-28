# Mobile Conflict Resolution Report — Decision 2

> Status: **port complete, QA PASS, PR #7 open; original #6 preserved and not
> closed.** No rebase, cherry-pick, reset or force-push was used.

## 1. Conflict

- Original branch `feat/authority-hardening-20261127` was based on
  `fix/m10-static-validation`; after `main` advanced, PR #6 became
  `mergeable=false` / `dirty`.
- A `Merge origin/main` commit `9cee52d` was added to the original branch
  (`parents: 64dce1e + 0972e4b`). The original PR/branch and its evidence were
  preserved; nothing was rewritten.

## 2. Port method

1. `git switch -c feat/authority-hardening-port-20261127 origin/main` at
   `0972e4b`.
2. Copy the 19-file hardening delta from `9cee52d` into the working tree
   (`git checkout 9cee52d -- <files>`), not a cherry-pick.
3. Commit one new commit `dc93f4b` on the main-based branch.
4. `git diff dc93f4b 9cee52d` is **empty**: the port tree is byte-identical to
   the audited conflict-resolved tree.
5. `git diff origin/main..dc93f4b --shortstat` = **19 files, +1229/−88**; no
   deleted files; no `deploy/` or other-repo changes.

## 3. Verification

| Check | Result |
|---|---|
| Tests | **50 passed** |
| Build | `colcon build --packages-select jcheng_mobile_bringup` OK (Jazzy) |
| Diff vs main | exactly the hardening delta; no unrelated main reversion |
| Main fixes preserved | interfaces v0.2.0 pin `afca22…`, README language switch, Nav2 `model_dt`/width/height fixes |
| Semantics | domain 42 guard; no `/cmd_vel`; lease-gated intent; no vendor motor topic; envelope matches system parser |
| Secrets/PII/absolute paths | none in the new commit |
| Independent QA | **PASS** on `dc93f4b` |

## 4. Delivery

- Branch: `feat/authority-hardening-port-20261127` (`dc93f4b`)
- PR: [#7](https://github.com/JCHENG-Robotics/jcheng-mobile/pull/7), links #6,
  explains the conflict and equivalence.
- CI: `mobile-gate`, `contract + no-hardware`, `ros build (humble)` all green.
- #6 remains open and is marked superseded in the PR text. **Close #6 only
  after #7 is merged**, with "superseded by #7"; its branch and history stay.

## 5. Residual risk

- Domain/remap/QoS are static/unit evidence; runtime behavior is unverified.
- The envelope is provisional/test-only; the interfaces proposal (merged as a
  proposal) does not publish a runtime contract.
- 200 ms freshness / 300 ms deadman remain provisional.
- #7 has no approval; merge is Board-gated. Mobile must not merge before the
  system base intake (#41), or the base would have no consumer.

## Related

- [Remote delivery](19-remote-delivery-report.md)
- [Independent QA](18-independent-qa-report.md)
- [Baseline manifest](25-ecosystem-integration-baseline-1-manifest.md)
