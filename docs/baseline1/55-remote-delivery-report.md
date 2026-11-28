# Remote Delivery Report

> Date: 2026-11-28. Controlled Git Operations were used throughout. No
> force-push, history rewrite, tag, release or unapproved merge.

## 1. Merged this sprint

| Repository | PR | Result |
|---|---|---|
| `.github` | #36 | TD-17/18/19 convergence report, merged via merge queue (`b1e0706`) |

Earlier convergence merges (already on main): devices #6, scenarios #4,
applications #19.

## 2. Open and awaiting real review

| Repository | PR | Head | State |
|---|---|---|---|
| devices | #7 | `dbf933b` | CI green; mergeable; `REVIEW_REQUIRED` |
| applications | #20 | `9550fdc` | CI green; mergeable; `REVIEW_REQUIRED` |
| interfaces | #20 | `bdd0e59` | all contract/security gates green; `REVIEW_REQUIRED` |
| `.github` | #37 | QA-audited `f0c3152`; final head in PR | review required |

No new approval was fabricated. The merge queue ruleset is active and
`enforce_admins` is on.

## 3. Closed as superseded/retired

| PR | Reason |
|---|---|
| devices #4 | superseded by #7 (three arms + AR5 re-verification) |
| devices #5, scenarios #3 | superseded by single-commit #6/#4 |
| `.github` #33/#34/#35 | superseded report branches |
| `.github` #31 | superseded by #32 |
| `.github` #32 | closed as superseded; handover content carried into #37 |

Closing a PR did not delete its branch.

## 4. Branch cleanup list (owner approval required)

These branches are retained because remote deletion is prohibited without an
explicit owner grant:

- recreated `feat/phase2-source-of-truth-20261128` (devices, scenarios);
- recreated `feat/armpi-ore-sorting-reference-20261128` (applications);
- merged/closed PR branches: devices #4/#5, scenarios #3,
  `.github` #31/#33/#34/#35;
- this sprint's candidate branches after merge: `feat/b1-devices-20261128`,
  `feat/b1-mock-e2e-20261128`, `docs/capability-vocabulary-proposal-20261128`,
  `docs/b1-final-acceptance-20261128`;
- temporary agent worktrees under `/tmp` and repo `.worktrees/`.

## 5. Required approvals

1. devices #7 — CODEOWNER review and merge.
2. applications #20 — CODEOWNER review and merge.
3. interfaces #20 — interface-owner review and acceptance (also closes
   contract criterion 2).
4. `.github` final acceptance PR — Board/CODEOWNER review and merge.
5. After merges: rerun fixed-main regression and independent QA, then update
   the manifest/status to COMPLETE.

## 6. Safety

No robot, real motion, DDS/ROS graph, production deployment or hardware output
was touched. All test execution was offline loopback mock.
