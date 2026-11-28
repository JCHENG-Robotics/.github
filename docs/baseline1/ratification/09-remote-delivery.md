# Remote Delivery Report — Ratification

## 1. Merged Baseline 1 PRs

| Repository | PR | Merge SHA |
|---|---|---|
| devices | #7 | `a006f5f2a3e71522f23b8aa6af6a363d0bd57174` |
| applications | #20 | `0be306e7d7ebf7b8a7e6b47aa5fb0c518358d90c` |
| interfaces | #20 | `a142641b4fb256aa2368abe778bb6c5b010d1c23` |
| `.github` | #37 | `f9e77eb8b309ab705c20f08a34bb28be68ff8ce7` |

All were approved by `JerichoSwaine` and merged through the protected branch.

## 2. Ratification PRs awaiting approval

| Repository | PR | Head | State |
|---|---|---|---|
| interfaces | #21 | `f656d69` | CI green, `REVIEW_REQUIRED` |
| scenarios | #5 | `d73e998` | CI green, `REVIEW_REQUIRED` |
| devices | #8 | `0bbbc18` | CI green, `REVIEW_REQUIRED` |
| `.github` | freeze PR | recorded in PR | m1-gate pending/required |

## 3. Closed / superseded earlier

#4 devices (superseded by #7), #5 devices/#3 scenarios (single-commit
replacements), #31/#32/#33/#34/#35 `.github` (superseded), #36 merged. Closing
did not delete branches.

## 4. Cleanup list (owner approval only)

Recreated phase2 branches, closed PR branches, merged candidate branches and
temporary worktrees. No remote branch was deleted by the agent.

## 5. Controlled operations

No self-approval, no main push, no force-push, no history rewrite, no tag or
release. No robot, real motion, DDS/ROS graph, production deployment or hardware
output.
