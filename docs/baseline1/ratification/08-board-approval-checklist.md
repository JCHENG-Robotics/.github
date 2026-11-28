# Board / CODEOWNER Approval Checklist

> All items below require a real human approval. The agent cannot self-approve,
> bypass branch protection, force-push or merge without approval.

## 1. Approve and merge (in order)

| # | PR | Why | Required check |
|---|---|---|---|
| 1 | jcheng-interfaces #21 | Contract Accepted/1.0.0 record; offline scope only | m1-gate, m2-contract, org checks |
| 2 | jcheng-scenarios #5 | vocabulary `contracted` after contract approval | scenarios gates; **add a second CODEOWNER first** — current CODEOWNERS names only the author, so self-approval is impossible |
| 3 | jcheng-devices #8 | AR5L/AR5R dual-arm units; 9 devices | devices-gate |
| 4 | `.github` freeze PR | manifest, acceptance, QA, release notes | m1-gate |

Order 1→2 is logical (contract then vocabulary). #8 and the docs PR are
independent but should merge before the final manifest regeneration.

## 2. After merge (required before COMPLETE)

1. Regenerate artifact hashes (scenario requirements change with vocabulary).
2. Rerun `.github/dev/baseline1-acceptance.sh` on the final main SHAs.
3. Rerun the 16-repository regression and this independent QA on the final SHAs.
4. Update the frozen manifest with merge SHAs and new artifact hashes.
5. Change the four statuses to DEVELOPMENT READY YES / OFFLINE INTEGRATION READY
   YES / BASELINE 1 COMPLETE YES / DEPLOYMENT READY NO, and commit the final
   freeze record (no self-referential hash).

## 3. Do not approve as part of this freeze

- No Baseline 2, new repository, schema family, governance programme or
  abstraction layer.
- No release/tag: release notes are a draft only; Board decides the release.
- No deployment or real-motion authorization.
- No branch deletion unless the owner separately approves the cleanup list.

## 4. Current status if approvals are not given

Baseline 1 stays **INCOMPLETE**. The technical evidence is green; only human
review/merge and the final post-merge rerun are missing.
