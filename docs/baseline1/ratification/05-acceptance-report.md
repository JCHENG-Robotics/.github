# Baseline 1 Acceptance Report — Ratification

## 1. Four statuses

| Status | Result | Basis |
|---|---|---|
| DEVELOPMENT READY | **YES** | guide, quick start, dev entries, tests, mock/sim entries verified |
| OFFLINE INTEGRATION READY | **YES** | fixed main unified acceptance passes; 8 cases + benchmark |
| BASELINE 1 COMPLETE | **NO — INCOMPLETE** | contract/vocabulary/AR5L-R ratification PRs and this freeze PR are unmerged/unapproved |
| DEPLOYMENT READY | **NO** | deployment blockers unchanged; no real motion authorization |

## 2. Decision 10 criteria

| # | Criterion | Status |
|---|---|---|
| 1 | Necessary governance/authority/source-of-truth PRs merged | **PARTIAL** — #7/#20/#20/#37 merged; #8/#5/#21 pending |
| 2 | Contract version/owner/approval | **Approval exists; main status pending #21** |
| 3 | Real CLI artifacts interoperate on main | **YES** |
| 4 | Invalid/unverified inputs classified and rejected | **YES** |
| 5 | Minimal positive mock task complete | **YES on merged main** (applications #20) |
| 6 | Traceable benchmark report | **YES** — observed INCONCLUSIVE, test PASS/FAIL |
| 7 | Simulation assets validated in scope | **YES offline**; Gazebo runtime not verified |
| 8 | Final main regression + independent QA | **YES** — PASS WITH FINDINGS; P2 fixed (03) |
| 9 | Developer Handover complete | **YES content**; guide/quickstart/first task verified |
| 10 | Manifest fixes SHAs/versions/hashes/limits | **Conditional** (04); regenerate after merges |
| 11 | Repeatable offline entry | **YES** — `.github/dev/baseline1-acceptance.sh` |

## 3. Exact remaining human actions

1. Approve and merge devices #8 (AR5L/AR5R units).
2. Approve and merge scenarios #5 (vocabulary `contracted`). **Prerequisite:** the scenarios CODEOWNERS currently names only the author, so a second CODEOWNER (for example `@JerichoSwaine`) must be added by the owner, or the Board must use an approved admin path; self-approval is not allowed.
3. Approve and merge interfaces #21 (contract Accepted 1.0.0).
4. Approve and merge this freeze PR.
5. Rerun fixed-main acceptance/regression and the independent QA on the final
   merge SHAs; update the manifest and set COMPLETE.
6. Approve branch cleanup separately if desired (remote deletion is not done
   by the agent).

Until steps 1–5, Baseline 1 is **INCOMPLETE**. No approval is fabricated.

## 4. Not verified

ArmPi reach/payload/aperture/resolution; AR5L/AR5R variant kinematics; PiPER X
hardware; real perception/IK/grasp; Gazebo runtime; deployment.
