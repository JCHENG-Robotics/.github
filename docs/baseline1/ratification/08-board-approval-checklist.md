# Board / CODEOWNER Approval Checklist

> All items below require a real human approval. The agent cannot self-approve,
> bypass branch protection, force-push or merge without approval.

## 1. Approve and merge (in order)

| # | PR | Why | Required check |
|---|---|---|---|
| 1 | `.github` #40 | final record (ratified-main SHAs/hashes, COMPLETE status) | m1-gate |

Already merged: interfaces #21 (`426f371`, Accepted 1.0.0), scenarios #5
(`1c21885`, vocabulary `contracted`), devices #8 (`c4be897`, AR5L/AR5R, 9
devices), freeze record #38 (`bf866d6`). Only the record correction remains.

## 2. Publication step

1. Approve/merge #40.
2. The post-merge acceptance on the ratified mains is already recorded in 02/04
   (new requirements hashes and 9-device registry); the final independent QA is
   in 03.
3. The four statuses are already recorded as DEVELOPMENT READY YES / OFFLINE
   INTEGRATION READY YES / BASELINE 1 COMPLETE YES / DEPLOYMENT READY NO. No
   artifact hash is computed over the record.

## 3. Do not approve as part of this freeze

- No Baseline 2, new repository, schema family, governance programme or
  abstraction layer.
- No release/tag: release notes are a draft only; Board decides the release.
- No deployment or real-motion authorization.
- No branch deletion unless the owner separately approves the cleanup list.

## 4. Current status if approvals are not given

No technical gate remains. Until #40 merges, main still shows #38's earlier
INCOMPLETE text; merge #40 to publish the final COMPLETE record.
