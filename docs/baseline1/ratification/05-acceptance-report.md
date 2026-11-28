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
| 1 | Necessary governance/authority/source-of-truth PRs merged | **YES** — #7/#20/#20/#37, #8/#5/#21 merged |
| 2 | Contract version/owner/approval | **YES** — Accepted 1.0.0 on main; vocabulary contracted |
| 3 | Real CLI artifacts interoperate on main | **YES** |
| 4 | Invalid/unverified inputs classified and rejected | **YES** |
| 5 | Minimal positive mock task complete | **YES on merged main** (applications #20) |
| 6 | Traceable benchmark report | **YES** — observed INCONCLUSIVE, test PASS/FAIL |
| 7 | Simulation assets validated in scope | **YES offline**; Gazebo runtime not verified |
| 8 | Final main regression + independent QA | **YES** — PASS WITH FINDINGS; P2 fixed (03) |
| 9 | Developer Handover complete | **YES** — merged handover content; guide/quickstart verified |
| 10 | Manifest fixes SHAs/versions/hashes/limits | **YES** (04), pending the freeze record merge |
| 11 | Repeatable offline entry | **YES** — `.github/dev/baseline1-acceptance.sh` |

## 3. Exact remaining human actions

1. Approve and merge this freeze PR (`.github` #38).
2. After merge, the final main SHAs are fixed; rerun the acceptance/regression
   and final QA once on those SHAs and set COMPLETE.
3. Optional: approve the branch cleanup list separately (no remote deletion by
   the agent).
4. Board decides release/tag; none was created.

The contract #21, vocabulary #5 and AR5L/R #8 are merged; the only remaining
gate is this record. Until it is merged, Baseline 1 is **INCOMPLETE**. No
approval is fabricated.

## 4. Not verified

ArmPi reach/payload/aperture/resolution; AR5L/AR5R variant kinematics; PiPER X
hardware; real perception/IK/grasp; Gazebo runtime; deployment.
