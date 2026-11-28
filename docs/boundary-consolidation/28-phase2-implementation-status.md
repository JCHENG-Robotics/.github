# Phase 2 Implementation Status — component complete, integration fail-closed

> Status: **component implementation complete; real cross-repo artifact
> integration fail-closed (2026-11-28)**. Draft PRs are open. Baseline 1
> remains **INCOMPLETE**.

## 1. Gate status

| Gate | Status | Evidence |
|---|---|---|
| Approved Wave 1–4 PRs merged | ✅ | #27/#28/#29/#2/#1/#5/#19/#41/#10/#7; #6 closed superseded |
| Actual-main integration regression | ✅ PASS | 26, 34; system 191, mobile 50, studio 13+222 |
| Independent main integration QA | ✅ Development/Main PASS; Deployment FAIL | 30/31/36 |
| Phase 2 implementation | ✅ components; ❌ real artifact integration | devices 118, scenarios 114, applications 209+23; [37](37-armpi-ore-sorting-reference-result.md) |
| Contract changes | none | repo-local artifacts; proposal only |

## 2. Deliverable status

| Requested deliverable | Status |
|---|---|
| Device Source of Truth Implementation | **component complete** (devices PR #3 Draft) |
| Scenario Source of Truth Implementation | **component complete** (scenarios PR #2 Draft) |
| ArmPi Ultra × ore_sorting Reference | **harness complete on fixtures**; real CLI artifacts fail closed (applications PR #18 Draft) |
| Device/scenario compatibility validation | implemented per repo; cross-repo vocabularies not converged |
| Generated snapshot/provenance | implemented (`snapshot`, hashes, provenance) |
| Interfaces proposal for promotion | not opened; repo-local artifacts first |

## 3. Blocking integration gaps

1. **Hash semantics**: device snapshot `content_hash` is the source-profile
   hash; the applications harness requires the artifact self-hash. The harness
   refuses a stale artifact rather than weakening the check.
2. **Capability vocabulary/composition**: scenario requirements are cell-level
   abstract capabilities (reach, payload, dof, aperture, camera resolution)
   plus perception algorithm capabilities; the device snapshot is one arm with
   concrete capability IDs. No cell composition mapping exists.
3. **Representation**: parameter/feedback/joint encodings differ between the
   devices snapshot and the harness; partial tolerances were added, but the
   canonical artifact schema is not agreed.

## 4. What would unblock

1. Define one canonical artifact schema: `source_hash` vs `artifact_hash`,
   parameter/feedback/joint representation.
2. Define the capability vocabulary and cell composition; split device vs
   algorithm requirements by owner.
3. Re-run the three commands and require a positive `matched` or explicit
   `UNVERIFIED` classification with `deployable: false`.
4. Independent QA of the converged implementation; then Board merge of the
   Draft PRs.

## 5. Non-claims

- The fixture path passes; the real devices/scenarios artifacts do not.
- No hardware/DDS/device access; no deployment; no release/tag.
- Baseline 1 remains **INCOMPLETE**; real-robot use remains **NOT READY**.

## Related

- [Reference result](37-armpi-ore-sorting-reference-result.md)
- [Phase 2 design](24-phase2-source-of-truth-design.md)
- [Technical debt](32-technical-debt-register.md)
- [Baseline manifest](35-baseline-manifest-updated.md)
