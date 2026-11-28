# Board / CODEOWNER Approval Checklist

> All items below require a real human approval. The agent cannot self-approve,
> bypass branch protection, force-push or merge without approval.

## 1. Approve and merge (in order)

| # | PR | Why | Required check |
|---|---|---|---|
| 1 | `.github` #38 | final freeze record: manifest, acceptance, QA, release notes | m1-gate |

Already merged: interfaces #21 (`426f371`, Accepted 1.0.0), scenarios #5
(`1c21885`, vocabulary `contracted`), devices #8 (`c4be897`, AR5L/AR5R, 9
devices). Only the freeze record remains.

## 2. After merge (required before COMPLETE)

1. Approve/merge #38.
2. The post-merge acceptance on the ratified mains is already recorded in 02/04
   (new requirements hashes and 9-device registry).
3. Confirm the final QA on the freeze record; then change the four statuses to
   DEVELOPMENT READY YES / OFFLINE INTEGRATION READY YES / BASELINE 1 COMPLETE
   YES / DEPLOYMENT READY NO. No artifact hash is computed over the record.

## 3. Do not approve as part of this freeze

- No Baseline 2, new repository, schema family, governance programme or
  abstraction layer.
- No release/tag: release notes are a draft only; Board decides the release.
- No deployment or real-motion authorization.
- No branch deletion unless the owner separately approves the cleanup list.

## 4. Current status if approvals are not given

Baseline 1 stays **INCOMPLETE**. The technical evidence is green; only human
review/merge and the final post-merge rerun are missing.
