# Independent QA Report — Baseline 1 Candidate

> Reviewer: independent read-only QA agent, separate from the implementation
> session. Date: 2026-11-28. No tracked file was modified, no commit/push/merge
> or tag was made, and no robot/DDS/hardware was accessed.

## 1. Verdict

**PASS WITH FINDINGS** — no P1. Three P2 and six P3 findings were raised; the
P2s are fixed in this delivery and the P3s are fixed or explicitly recorded.
The technical baseline is green; Baseline 1 remains conditional because the
required PRs are not merged.

| Item | Verdict |
|---|---|
| devices PR #7 | PASS |
| applications PR #20 | PASS WITH FINDINGS (traceability fixed in `bc6dc5b`) |
| interfaces PR #20 | PASS |
| Baseline 1 readiness | PASS WITH FINDINGS — correctly INCOMPLETE / deployment NOT READY |

## 2. Findings and disposition

| ID | Finding | Disposition |
|---|---|---|
| P2-1 | `docs/baseline1/` was untracked and had no reviewable head | **Fixed**: committed on `docs/b1-final-acceptance-20261128`, PR opened; 42/55 updated |
| P2-2 | Missing deliverable 9 (`49-independent-qa-report.md`) | **Fixed**: this report |
| P2-3 | Benchmark traceability overstated: benchmark report itself has no scenario/evaluation IDs | **Fixed**: samples now carry scenario/version/evaluation IDs; task summary carries scenario requirements, hashes, repository SHAs and gate fields; 47 states the benchmark report's actual scope |
| P3-1 | Boundary run claimed non-zero exit | **Fixed**: report-only wording in 48; findings do not fail the command |
| P3-2 | `34-boundary-report-main.md` still said 12 open | **Fixed**: marked as an eight-repo snapshot superseded by the 16-repo run (25 + 1 waived) |
| P3-3 | Acceptance script was outside git and not executable | **Fixed**: tracked at `.github/dev/baseline1-acceptance.sh` (executable), workspace entry is a symlink |
| P3-4 | Mock summary omitted `artifact_valid`/`capability_satisfied` | **Fixed** in `bc6dc5b`; tests assert both |
| P3-5 | "16 repositories" wording vs frozen tag | **Fixed**: 15 main SHAs + frozen `v1.0.0` |
| P3-6 | Manipulation release check needs a missing studio venv | Recorded as an environment prerequisite; pytest portions pass (93 + 242 + 7 skipped) |

## 3. Independently verified evidence

- Tests: interfaces 16/22, devices 120/122, scenarios 116, applications
  211+5/218+5, system 191, mobile 50, studio 13+222, perception 107, learning
  68 (frozen env), teleop 218, simulation 86+2, benchmark 61, ops 9, research
  gate, `.github` 20; no count mismatch.
- Acceptance script exit 0 with candidate roots; task case files and
  `samples.jsonl` byte-identical (the summary necessarily records root-specific
  SHAs/benchmark paths).
- All 8 cases exact; only `normal` success; stop-once behaviour confirmed;
  authorization failure has zero execute requests.
- Negative tests: `STALE_DEVICE_HASH`, `NO_DEVICE_FOR_ROLE`, `INCOMPATIBLE_UNIT`.
- Boundary: 25 open + 1 classified waiver.
- AR5 official page independently confirmed 7 DOF, 5 kg, 683 mm, EtherCAT,
  torque sensors and recorded joint ranges; all five snapshot hashes match 42.
- No hardware, DDS/ROS, real motion, deployment or vendor data access.

## 4. Second re-audit (final candidate)

The same independent reviewer re-checked the fixes: **PASS, no new P1/P2**.
Residual P3 items were addressed as follows:

- committed docs now include this report and the tracked acceptance entry;
- #32 is recorded as closed/superseded in 55;
- applications documentation and changelog describe the provenance fields and
  `--repository-sha`;
- `cell_roles` is present in `task_summary.json`;
- the byte-identical claim is narrowed to case files and samples.

## 5. Residual risk

The QA could not verify GitHub PR review state because its environment had no
`gh` auth; the delivery report (55) records the actual PR/CI state from the
implementation session. Merge approval and the post-merge fixed-main rerun
remain human gates.
